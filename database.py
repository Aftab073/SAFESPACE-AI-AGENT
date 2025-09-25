import uuid
from datetime import datetime
from typing import Dict, List, Optional
from models import User, UserCreate, ChatMessage
from auth import hash_password, verify_password

# Simple in-memory database (replace with real DB later)
users_db: Dict[str, dict] = {}
chat_history_db: Dict[str, List[dict]] = {}

def create_user(user_data: UserCreate) -> User:
    """Create new user account"""
    # Check if user already exists
    for user in users_db.values():
        if user["email"] == user_data.email:
            raise ValueError("User with this email already exists")
    
    # Create new user
    user_id = str(uuid.uuid4())
    user_dict = {
        "id": user_id,
        "email": user_data.email,
        "full_name": user_data.full_name,
        "password_hash": hash_password(user_data.password),
        "created_at": datetime.utcnow(),
        "is_active": True
    }
    
    users_db[user_id] = user_dict
    chat_history_db[user_id] = []  # Initialize empty chat history
    
    return User(
        id=user_id,
        email=user_dict["email"], 
        full_name=user_dict["full_name"],
        created_at=user_dict["created_at"],
        is_active=user_dict["is_active"]
    )

def authenticate_user(email: str, password: str) -> Optional[User]:
    """Authenticate user login"""
    for user_dict in users_db.values():
        if user_dict["email"] == email:
            if verify_password(password, user_dict["password_hash"]):
                return User(
                    id=user_dict["id"],
                    email=user_dict["email"],
                    full_name=user_dict["full_name"], 
                    created_at=user_dict["created_at"],
                    is_active=user_dict["is_active"]
                )
    return None

def get_user_by_id(user_id: str) -> Optional[User]:
    """Get user by ID"""
    user_dict = users_db.get(user_id)
    if user_dict:
        return User(
            id=user_dict["id"],
            email=user_dict["email"],
            full_name=user_dict["full_name"],
            created_at=user_dict["created_at"],
            is_active=user_dict["is_active"]
        )
    return None

def save_chat_message(user_id: str, message: str, response: str, tool_used: str):
    """Save chat message to user's history"""
    chat_entry = {
        "id": str(uuid.uuid4()),
        "message": message,
        "response": response, 
        "tool_used": tool_used,
        "created_at": datetime.utcnow()
    }
    
    if user_id not in chat_history_db:
        chat_history_db[user_id] = []
    
    chat_history_db[user_id].append(chat_entry)

def get_user_chat_history(user_id: str) -> List[dict]:
    """Get user's chat history"""
    return chat_history_db.get(user_id, [])
