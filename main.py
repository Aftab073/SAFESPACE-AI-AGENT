from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Import our modules
from ai_agent import graph, SYSTEM_PROMPT, parse_response
from models import UserCreate, UserLogin, Token, User
from auth import create_access_token, get_current_user
from database import create_user, authenticate_user, get_user_by_id, save_chat_message, get_user_chat_history

app = FastAPI(title="SafeSpace AI Mental Health API")

# Add CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],  # Streamlit default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Existing Query model
class Query(BaseModel):
    message: str

# Authentication endpoints
@app.post("/auth/register", response_model=Token)
async def register(user_data: UserCreate):
    """Register new user account"""
    try:
        user = create_user(user_data)
        access_token = create_access_token(user.id, user.email)
        return Token(access_token=access_token, user=user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/auth/login", response_model=Token)  
async def login(user_credentials: UserLogin):
    """Login user and return JWT token"""
    user = authenticate_user(user_credentials.email, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    access_token = create_access_token(user.id, user.email)
    return Token(access_token=access_token, user=user)

@app.get("/auth/me", response_model=User)
async def get_me(current_user: dict = Depends(get_current_user)):
    """Get current user profile"""
    user = get_user_by_id(current_user["user_id"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Protected chat endpoint
@app.post("/ask")
async def ask(query: Query, current_user: dict = Depends(get_current_user)):
    """Chat with AI agent (requires authentication)"""
    # AI agent processing
    inputs = {"messages": [("system", SYSTEM_PROMPT), ("user", query.message)]}
    stream = graph.stream(inputs, stream_mode="updates")
    tool_called_name, final_response = parse_response(stream)
    
    # Save to user's chat history
    save_chat_message(
        user_id=current_user["user_id"],
        message=query.message,
        response=final_response, 
        tool_used=tool_called_name
    )
    
    return {"response": final_response, "tool_used": tool_called_name}

@app.get("/chat/history")
async def get_chat_history(current_user: dict = Depends(get_current_user)):
    """Get user's chat history"""
    history = get_user_chat_history(current_user["user_id"])
    return {"history": history}

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
