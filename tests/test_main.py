""" import pytest
from fastapi.testclient import TestClient
from app.database import get_db,SessionLocal,engine
from app.main import app,get_current_user
from app.models import Base, User, Task
from fastapi import Depends
from logging import Logger

# Initialize the test client
client = TestClient(app)

#Override db connection method
def for_test_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




@pytest.fixture()
def setup_database():
    # 2. Tell FastAPI to swap the real DB with the Test DB
    app.dependency_overrides[get_db] = for_test_get_db
    # build schema tables before every single test run execution
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    # 3. Clean up overrides after tests finish
    app.dependency_overrides.clear()


@pytest.fixture()
def generate_token_and_login_user():

    payload = {"email": "test@email.com","password": "password"}
    client.post("/users/", json=payload)

    login_data = {"username": "test@email.com", "password":"password"}
    login_response = client.post("/auth/login", data= login_data)
    token = login_response.json()["access_token"]
  
    return {"Authorization": f"Bearer {token}"}

 def test_create_task(generate_token_and_login_user):
    task_payload = {"title" : "Test Task creation", 
                    "description" : "test task description", 
                    "priority" : "medium", 
                    "due_date" : None}
    
    response = client.post("/tasks/",json = task_payload, headers = generate_token_and_login_user)

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task creation" """
