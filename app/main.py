from fastapi import FastAPI, HTTPException
from .ai_client import CodebaseGPSAI
from .schemas import AnalysisRequest
from app.config import settings
app = FastAPI()

gps_ai = CodebaseGPSAI(settings.GEMINI_API_KEY)

@app.post("/api/gps/impact")
async def get_impact(request: AnalysisRequest):
    try:
        # Pass the context and query to our AI client
        analysis = await gps_ai.analyze_code_impact(
            code_context=request.context, 
            user_query=request.query
        )
        return {"status": "success", "data": analysis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/gps/health")
def health():
    return {"status": "online", "engine": "Gemini-GenAI-SDK"}