import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool


from app.main import app, Base, get_db, get_current_user, User 

# Setup Isolated SQLite Database for Testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL,connect_args={"check_same_thread": False},poolclass=StaticPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function", autouse=True)
def setup_database():
    #Creates all tables before each test and drop them after."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session():
    # database session
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture
def client(db_session):         # to create a TestClient, Insert test user, and override db
    
    # insert a test user into the SQLite database
    test_user = User(
        email="testuser@example.com",
        hashed_password="testpassword",
        is_active=True,
        role="MEMBER"
    )
    db_session.add(test_user)
    db_session.commit()
    db_session.refresh(test_user)  # This populates the auto-generated id

    # Define the auth override to return this specific database user object
    def mock_get_current_user():
        return test_user

    def override_get_db():
        try:
            yield db_session
        finally:
            pass  # Session lifetime managed by the db_session fixture

    # Apply the overrides to the FastAPI app
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = mock_get_current_user
    
    with TestClient(app) as c:
        yield c
        
    app.dependency_overrides.clear()

#  Tests 

def test_create_task(client):
    response = client.post("/tasks/", json={"title": "Test Task", "description": "Linked to user model"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert "id" in data

def test_read_all_tasks(client):
    client.post("/tasks/", json={"title": "Task 1", "description": "Desc 1"})
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert len(response.json()) >= 1

def test_read_single_task_success(client):
    create_res = client.post("/tasks/", json={"title": "Task 2", "description": "Desc 2"}).json()
    task_id = create_res["id"]
    
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Task 2"

def test_read_task_not_found(client):
    response = client.get("/tasks/99999")
    assert response.status_code == 404

def test_update_task(client):
    create_res = client.post("/tasks/", json={"title": "Old Title", "description": "Old Desc"}).json()
    task_id = create_res["id"]
    
    response = client.put(f"/tasks/{task_id}", json={"title": "New Title", "description": "New Desc"})
    assert response.status_code == 200
    assert response.json()["title"] == "New Title"

def test_delete_task(client):
    create_res = client.post("/tasks/", json={"title": "To Delete", "description": "Desc"}).json()
    task_id = create_res["id"]
    
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    
    get_res = client.get(f"/tasks/{task_id}")
    assert get_res.status_code == 404
