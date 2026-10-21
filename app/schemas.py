from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import Optional, Literal

# --- AUTHENTICATION SCHEMAS ---

class UserBase(BaseModel):
    email: EmailStr
   

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, description="Password must be at least 6 characters long")

class UserResponse(UserBase):
    id: int

    model_config = ConfigDict(from_attributes = True)


# Task 

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    priority: Optional[Literal["low", "medium", "high"]] = Field(default="medium", description="Must be low, medium, or high")
    due_date: Optional[datetime] = None

class TaskCreate(TaskBase):
    pass

class TaskResponse(TaskBase):
    id: int
    is_completed: bool
    created_at: datetime
    owner_id: int

    model_config = ConfigDict(from_attributes = True)


  
class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] =None
    priority: Optional[Literal["low", "medium", "high"]] = Field(default=None,description="Must be low, medium, or high")
    due_date: Optional[datetime] =None
    is_completed: Optional[bool] =None


class TaskDeleteResponse(TaskResponse):
     detail: str = "Task deleted."
     
class Token(BaseModel):
    access_token: str
    token_type: str
  

