#step 1: Setup FastAPI backend
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

from ai_agent import graph, SYSTEM_PROMPT, parse_response

app = FastAPI()

#step2: Receive and Validate requests from frontend
class Query(BaseModel):
    message: str

@app.post("/ask")
async def ask(query: Query):
    #Ai agent
    
    inputs = {"messages": [("system", SYSTEM_PROMPT), ("user", query.message)]}
    stream = graph.stream(inputs, stream_mode="updates")
    tool_called_name, final_response = parse_response(stream)

    # Debugging print
    print("DEBUG >> tool_called_name:", tool_called_name)
    print("DEBUG >> final_response:", final_response)
    
    return {"response": final_response, "tool_used": tool_called_name}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)