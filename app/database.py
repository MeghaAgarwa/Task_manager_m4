
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import StaticPool
import sys



from app.config import settings
if "pytest" in sys.modules:
    DATABASE_URL = "sqlite:///:memory:"
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False},poolclass=StaticPool)

else:
    engine = create_engine(settings.DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()   # for creating ORM models

# Dependency to get db session in FastAPI routes
def get_db():
    db = SessionLocal()     # Create a new database session 
    try:
        yield db            
    finally:
        db.close()