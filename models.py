from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime, timezone

# Authentication Models
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if len(v.encode('utf-8')) > 72:
            raise ValueError('Password is too long (max 72 characters)')
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v

class UserLogin(BaseModel):
    email: EmailStr  
    password: str
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if len(v.encode('utf-8')) > 72:
            raise ValueError('Password is too long (max 72 characters)')
        return v

class User(BaseModel):
    id: str
    email: str
    full_name: Optional[str]
    created_at: datetime
    is_active: bool = True

from datetime import datetime, timezone
from typing import Optional

class UserUsage(BaseModel):
    user_id: str
    messages_used_this_month: int = 0
    current_period_start: datetime
    current_period_end: datetime
    last_reset_date: datetime
    
class UsageResponse(BaseModel):
    messages_used: int
    messages_limit: int
    period_ends: datetime
    days_remaining: int

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
