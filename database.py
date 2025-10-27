import uuid
import os
from datetime import datetime, timezone
from typing import Dict, List, Optional
import calendar
from sqlalchemy import create_engine, Column, String, Integer, Boolean, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from models import User, UserCreate
from auth import hash_password, verify_password


# Get database URL from environment variable (PostgreSQL on Render, SQLite locally)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./safespace.db")

# Fix for Render PostgreSQL URL (postgres:// -> postgresql://)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Create engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
    pool_pre_ping=True  # Verify connections before using
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


# Database Models
class UserDB(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)


class ChatHistoryDB(Base):
    __tablename__ = "chat_history"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=False)
    message = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    tool_used = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False)


class UserUsageDB(Base):
    __tablename__ = "user_usage"
    
    user_id = Column(String, primary_key=True, index=True)
    messages_used_this_month = Column(Integer, default=0)
    current_period_start = Column(DateTime, nullable=False)
    current_period_end = Column(DateTime, nullable=False)
    last_reset_date = Column(DateTime, nullable=False)


# Create all tables
Base.metadata.create_all(bind=engine)


def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_user(user_data: UserCreate) -> User:
    """Create new user account"""
    db = SessionLocal()
    
    try:
        # Check if user already exists
        existing_user = db.query(UserDB).filter(UserDB.email == user_data.email).first()
        if existing_user:
            raise ValueError("User with this email already exists")
        
        # Create new user
        user_id = str(uuid.uuid4())
        created_at = datetime.utcnow()
        password_hash = hash_password(user_data.password)
        
        db_user = UserDB(
            id=user_id,
            email=user_data.email,
            full_name=user_data.full_name,
            password_hash=password_hash,
            created_at=created_at,
            is_active=True
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        # Initialize usage tracking
        initialize_user_usage(user_id)
        
        return User(
            id=user_id,
            email=user_data.email,
            full_name=user_data.full_name,
            created_at=created_at,
            is_active=True
        )
    finally:
        db.close()


def authenticate_user(email: str, password: str) -> Optional[User]:
    """Authenticate user login"""
    db = SessionLocal()
    
    try:
        db_user = db.query(UserDB).filter(UserDB.email == email).first()
        
        if db_user and verify_password(password, db_user.password_hash):
            return User(
                id=db_user.id,
                email=db_user.email,
                full_name=db_user.full_name,
                created_at=db_user.created_at,
                is_active=db_user.is_active
            )
        return None
    finally:
        db.close()


def get_user_by_id(user_id: str) -> Optional[User]:
    """Get user by ID"""
    db = SessionLocal()
    
    try:
        db_user = db.query(UserDB).filter(UserDB.id == user_id).first()
        
        if db_user:
            return User(
                id=db_user.id,
                email=db_user.email,
                full_name=db_user.full_name,
                created_at=db_user.created_at,
                is_active=db_user.is_active
            )
        return None
    finally:
        db.close()


def save_chat_message(user_id: str, message: str, response: str, tool_used: str):
    """Save chat message to user's history"""
    db = SessionLocal()
    
    try:
        chat_entry = ChatHistoryDB(
            id=str(uuid.uuid4()),
            user_id=user_id,
            message=message,
            response=response,
            tool_used=tool_used,
            created_at=datetime.utcnow()
        )
        
        db.add(chat_entry)
        db.commit()
    finally:
        db.close()


def get_user_chat_history(user_id: str) -> List[dict]:
    """Get user's chat history"""
    db = SessionLocal()
    
    try:
        chat_entries = db.query(ChatHistoryDB).filter(
            ChatHistoryDB.user_id == user_id
        ).order_by(ChatHistoryDB.created_at.desc()).all()
        
        history = []
        for entry in chat_entries:
            history.append({
                "id": entry.id,
                "message": entry.message,
                "response": entry.response,
                "tool_used": entry.tool_used,
                "created_at": entry.created_at.isoformat()
            })
        
        return history
    finally:
        db.close()


def initialize_user_usage(user_id: str) -> None:
    """Create initial usage tracking for a new user"""
    db = SessionLocal()
    
    try:
        now = datetime.now(timezone.utc)
        last_day = calendar.monthrange(now.year, now.month)[1]
        period_end = now.replace(day=last_day, hour=23, minute=59, second=59)
        period_start = now.replace(day=1, hour=0, minute=0, second=0)
        
        usage = UserUsageDB(
            user_id=user_id,
            messages_used_this_month=0,
            current_period_start=period_start,
            current_period_end=period_end,
            last_reset_date=now
        )
        
        db.add(usage)
        db.commit()
    finally:
        db.close()


def get_user_usage(user_id: str) -> dict:
    """Get current usage for a user"""
    db = SessionLocal()
    
    try:
        usage = db.query(UserUsageDB).filter(UserUsageDB.user_id == user_id).first()
        
        if not usage:
            initialize_user_usage(user_id)
            usage = db.query(UserUsageDB).filter(UserUsageDB.user_id == user_id).first()
        
        return {
            "user_id": usage.user_id,
            "messages_used_this_month": usage.messages_used_this_month,
            "current_period_start": usage.current_period_start.isoformat(),
            "current_period_end": usage.current_period_end.isoformat(),
            "last_reset_date": usage.last_reset_date.isoformat()
        }
    finally:
        db.close()


def increment_user_usage(user_id: str) -> dict:
    """Increment user's message count"""
    db = SessionLocal()
    
    try:
        usage = db.query(UserUsageDB).filter(UserUsageDB.user_id == user_id).first()
        
        if not usage:
            db.close()
            initialize_user_usage(user_id)
            db = SessionLocal()
            usage = db.query(UserUsageDB).filter(UserUsageDB.user_id == user_id).first()
        
        # Check if we need to reset monthly counter
        now = datetime.now(timezone.utc)
        
        if now > usage.current_period_end:
            reset_monthly_usage(user_id)
            db.close()
            db = SessionLocal()
            usage = db.query(UserUsageDB).filter(UserUsageDB.user_id == user_id).first()
        
        # Increment message count
        usage.messages_used_this_month += 1
        db.commit()
        db.refresh(usage)
        
        return {
            "user_id": usage.user_id,
            "messages_used_this_month": usage.messages_used_this_month,
            "current_period_start": usage.current_period_start.isoformat(),
            "current_period_end": usage.current_period_end.isoformat(),
            "last_reset_date": usage.last_reset_date.isoformat()
        }
    finally:
        db.close()


def reset_monthly_usage(user_id: str) -> None:
    """Reset user's monthly message count"""
    db = SessionLocal()
    
    try:
        now = datetime.now(timezone.utc)
        last_day = calendar.monthrange(now.year, now.month)[1]
        period_end = now.replace(day=last_day, hour=23, minute=59, second=59)
        period_start = now.replace(day=1, hour=0, minute=0, second=0)
        
        usage = db.query(UserUsageDB).filter(UserUsageDB.user_id == user_id).first()
        
        if usage:
            usage.messages_used_this_month = 0
            usage.current_period_start = period_start
            usage.current_period_end = period_end
            usage.last_reset_date = now
            db.commit()
    finally:
        db.close()


def get_user_chat_history(user_id: str, limit: int = None) -> List[dict]:
    """Get user's chat history with optional limit"""
    db = SessionLocal()
    
    try:
        query = db.query(ChatHistoryDB).filter(
            ChatHistoryDB.user_id == user_id
        ).order_by(ChatHistoryDB.created_at.desc())
        
        # Apply limit if specified
        if limit:
            query = query.limit(limit)
        
        chat_entries = query.all()
        
        history = []
        for entry in chat_entries:
            history.append({
                "id": entry.id,
                "message": entry.message,
                "response": entry.response,
                "tool_used": entry.tool_used,
                "created_at": entry.created_at.isoformat()
            })
        
        return history
    finally:
        db.close()


def clear_user_chat_history(user_id: str) -> bool:
    """Delete all chat history for a user"""
    db = SessionLocal()
    
    try:
        db.query(ChatHistoryDB).filter(ChatHistoryDB.user_id == user_id).delete()
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        return False
    finally:
        db.close()
