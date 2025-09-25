from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# Authentication Models
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr  
    password: str

class User(BaseModel):
    id: str
    email: str
    full_name: Optional[str]
    created_at: datetime
    is_active: bool = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: User

# Chat Models  
class ChatMessage(BaseModel):
    id: str
    user_id: str
    message: str
    response: str
    tool_used: Optional[str]
    created_at: datetime
