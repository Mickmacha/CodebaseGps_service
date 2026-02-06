from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .ai_client import CodebaseGPSAI

app = FastAPI()

ai_engine = CodebaseGPSAI()

class GPSRequest(BaseModel):
    task: str  # "search", "impact", or "map"
    context: str  # The code or file tree
    query: str = None


@app.post("/gps/query")
async def handle_query(request: GPSRequest):
    data = await ai_engine.process_task(
        task=request.task, context=request.context, query=request.query
    )
    return {"status": "success", "task": request.task, "data": data}
