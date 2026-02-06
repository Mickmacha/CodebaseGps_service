from google import genai
from google.genai import types
from .schemas import ImpactAnalysisResponse, GraphResponse
import os

class CodebaseGPSAI:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model_id = "gemini-2.0-flash" # or "gemini-3-flash-preview"

    async def analyze_code_impact(self, code_context: str, user_query: str) -> ImpactAnalysisResponse:
        """Uses Gemini to predict what will break if code changes."""
            
        prompt = f"""
            Context: You are the 'Codebase GPS' assistant. 
            Task: Analyze the following code and the user's proposed change.
            Proposed Change: {user_query}
            
            Codebase Snippet:
            {code_context}
        """
    
        # The NEW way: Direct structured output via Pydantic
        response = self.client.models.generate_content(
            model=self.model_id,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ImpactAnalysisResponse,
            ),
        )
            
            # The SDK automatically parses the JSON into your Pydantic model
        return response.parsed

    async def generate_dependency_map(self, file_list: list) -> GraphResponse:
        """Converts a raw list of files and imports into a Graph JSON."""
                # Implementation logic for Feature 3...
        pass