from datetime import timedelta,datetime, timezone
from typing import List

from fastapi import Depends, FastAPI, HTTPException, status

from fastapi.middleware.cors import CORSMiddleware
import jwt
from sqlalchemy.orm import Session
from app.models import Task, User
from app.database import Base,engine, get_db
from app.schemas import UserCreate, UserResponse, TaskResponse, TaskCreate, TaskUpdate, Token, TaskDeleteResponse


from passlib.context import CryptContext  # Pure Passlib library
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.config import settings

# hashing passwords using bcrypt algo so they are safe in storage - db security
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Token settings for JWT (JSON Web Token) authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login") # tells FastAPI where to look for authentication credentials - network security


# Intercepts requests, decodes the JWT token and returns the current user object
# Instead of passing owner_id as a query parameter, the backend will parse the token header recieved with the request, to find who is logged in, and return the user 
 
def get_current_user(token: str = Depends(oauth2_scheme), db:Session = Depends(get_db)):
    try:
        # decode and verify token signature using pyjwt
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=settings.JWT_ALGORITHM)
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid email in token")
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


Base.metadata.create_all(bind=engine)
app = FastAPI(title="Task Manager API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


@app.get("/")           # the decorator registers a route handler in FastAPI which telss it to listen for incoming network traffic. 
                        #   @app.get("/") tells FastAPI that the function immediately following is to be registered as a route for the GET method on the root path "/"
def root():
    return {"message": "Welcome to the Task Manager API!",
            "docs_url": "http://localhost:8000/docs",}


@app.post("/users/", response_model=UserResponse)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    # Create a new user
    email  = db.query(User).filter(User.email == user_in.email).first()
    if email:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = pwd_context.hash(user_in.password)
    new_user = User(email=user_in.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user) 
    return new_user



@app.post("/auth/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # OAuth2PasswordRequestForm maps credentials to form_data.username and form_data.password
    user = db.query(User).filter(User.email == form_data.username).first()
    # Check if the user exists and the password is correct
    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    # After validation, create a JWT token for the user

    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token_payload = { "sub": user.email, "exp": expire}
    encoded_jwt = jwt.encode(token_payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    
    return {"access_token": encoded_jwt, "token_type": "bearer"}

    

# to display current user 
@app.get("/users/", response_model=UserResponse)
def get_user_details(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    
    user = db.query(User).filter(User.id == current_user.id).first()
    return user



# --------------------------TASKS--------------------------------------

@app.post("/tasks/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task_in: TaskCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    
    new_task = Task(title = task_in.title, 
                    description = task_in.description, 
                    priority = task_in.priority, 
                    due_date = task_in.due_date, 
                    owner_id = current_user.id)     # assign the task to the extracted user from the token header 

    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@app.get("/tasks/", response_model=List[TaskResponse])
def get_all_tasks(page: int = 1, size: int = 10, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    #Fetches a paginated slice of tasks belonging to the logged-in user .
    if page < 1:
        page = 1
    offset_value = (page - 1) * size
    
    # Filter the query by current_user.id 
    tasks = db.query(Task).filter(Task.owner_id == current_user.id).offset(offset_value).limit(size).all()
    return tasks

# read single task by id, but only if it belongs to the logged-in user
@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task_by_id(task_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id, Task.owner_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# update task
@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_in: TaskUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id, Task.owner_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Extract only the fields explicitly sent by the user in the request body
    update_data = task_in.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(task, key, value)
    
    db.commit()
    db.refresh(task)
    return task

# Delete task
@app.delete("/tasks/{task_id}",response_model=TaskDeleteResponse)
def delete_task_record(task_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id, Task.owner_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(task)
    db.commit()
    return task


