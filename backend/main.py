#step 1: Setup FastAPI backend
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

#step2: Receive and Validate requests from frontend
class Query(BaseModel):
    message: str

@app.post("/ask")
async def ask(query: Query):
    #Ai agent
    return "This is a dummy response from the AI agent."