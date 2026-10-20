
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import StaticPool
import sys


#DATABASE_URL = os.getenv("DOCKER_DATABASE_URL", "postgresql+psycopg2://postgres:postgres@db:5432/task_manager_db")

#DATABASE_URL = os.getenv("DOCKER_DATABASE_URL","postgresql+psycopg2://DB_USER:DB_PASSWORD@db:DB_PORT/DB_NAME")

#engine = create_engine(DATABASE_URL)

from app.config import settings
if "pytest" in sys.modules:
    DATABASE_URL = "sqlite:///:memory:"
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False},poolclass=StaticPool)

else:
    engine = create_engine(settings.DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get db session in FastAPI routes
def get_db():
    db = SessionLocal()     # Create a new database session every time a request is made to the API
    try:
        yield db            
    finally:
        db.close()