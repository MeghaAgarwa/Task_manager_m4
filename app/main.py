from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
from pydantic import BaseModel 
from fastapi.middleware.cors import CORSMiddleware
from app.models import Base
from app.database import engine

Base.metadata.create_all(bind=engine)
app = FastAPI()

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


