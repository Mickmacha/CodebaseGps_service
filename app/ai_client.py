from google import genai
from google.genai import types
from pydantic import BaseModel
from typing import Optional, Dict, Any
from app.config import settings

from .schemas import SearchResponse, ImpactAnalysisResponse, GraphResponse
import os

class CodebaseGPSAI:
    def __init__(self):
        # The new 2026 SDK picks up GEMINI_API_KEY automatically
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model_id = "gemini-3-flash-preview" 

    async def process_task(self, task: str, context: str, query: Optional[str] = None) -> Dict[str, Any]:
        """
        Main entry point for the 'One Endpoint' approach.
        """
        if task == "search":
            return await self._execute_search(context, query)
        elif task == "impact":
            return await self._execute_impact(context, query)
        elif task == "map":
            return await self._execute_graph(context)
        else:
            raise ValueError(f"Unknown GPS task: {task}")

    async def _execute_search(self, context: str, query: str):
        prompt = f"Find code related to: '{query}'. Context:\n{context}"
        return self._generate_structured(prompt, SearchResponse)

    async def _execute_impact(self, context: str, query: str):
        prompt = f"Analyze impact of changing: '{query}'. Context:\n{context}"
        return self._generate_structured(prompt, ImpactAnalysisResponse)

    async def _execute_graph(self, context: str):
        prompt = f"Map the dependencies (nodes/links) for this code:\n{context}"
        return self._generate_structured(prompt, GraphResponse)

    def _generate_structured(self, prompt: str, schema: type[BaseModel]):
        """Internal helper for Gemini Structured Output calls."""
        response = self.client.models.generate_content(
            model=self.model_id,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=schema,
                temperature=0.1, # Low temperature for reliable architecture work
            ),
        )
        # .parsed gives you the Pydantic object instantly
        return response.parsed.model_dump()