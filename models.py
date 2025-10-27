from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime, timezone

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
