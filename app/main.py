from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .ai_client import CodebaseGPSAI

app = FastAPI()
# allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ai_engine = CodebaseGPSAI()


class GPSRequest(BaseModel):
    task: str  # "search", "impact", or "map"
    context: str  # The code or file tree
    query: str = None


@app.get("/")
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Codebase GPS Service"}


@app.post("/gps/query")
async def handle_query(request: GPSRequest):
    data = await ai_engine.process_task(
        task=request.task, context=request.context, query=request.query
    )
    return {"status": "success", "task": request.task, "data": data}
