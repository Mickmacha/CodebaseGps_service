import os
from typing import List, Optional, Dict, Any
from google import genai
from google.genai import types
from pydantic import BaseModel
from app.config import settings

# Import the schemas you provided
from .schemas import (
    GraphResponse, 
    ImpactAnalysisResponse, 
    SearchResponse, 
    SearchResult
)

class CodebaseGPSAI:
    def __init__(self):
        # Using the 2026 google-genai SDK
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model_id = "gemini-2.0-flash" # Optimized for speed & structure

    async def process_task(
        self, task: str, context: str, query: Optional[str] = None
    ) -> Dict[str, Any]:
        if task == "search":
            return await self._execute_search(context, query)
        elif task == "impact":
            return await self._execute_impact(context, query)
        elif task == "map":
            return await self._execute_graph(context)
        else:
            raise ValueError(f"Unknown GPS task: {task}")

    async def _execute_search(self, context: str, query: str):
        prompt = f"""
        ROLE: Expert Code Navigator (Semantic Search Engine).
        USER INTENT: "{query}"
        CODE CONTEXT:
        {context}

        TASK:
        Identify the most relevant files for the user's intent. Do not just look for keyword matches; look for the actual implementation of logic. 
        Example: If the user asks for "how users pay," find Stripe handlers or wallet logic even if they don't use the word "pay."

        OUTPUT REQUIREMENTS:
        - Rank results by 'relevance_score' (1-10).
        - Provide a 'summary' that explains the overall architectural flow related to this query.
        """
        return self._generate_structured(prompt, SearchResponse)

    async def _execute_impact(self, context: str, query: str):
        prompt = f"""
        ROLE: Senior System Architect (Risk & Impact Analysis).
        PROPOSED CHANGE: "{query}"
        CODE CONTEXT:
        {context}

        TASK:
        Perform a 'Blast Radius' analysis. If the user modifies the logic specified in the query, what else will break? 
        Trace dependencies and shared interfaces.

        SCORING CRITERIA (risk_score):
        - 1-3: Localized change (e.g., CSS, documentation).
        - 4-6: Logic change in a single module.
        - 7-10: Critical architectural change (e.g., Database schema, Auth middleware, Shared Types).

        OUTPUT REQUIREMENTS:
        - List specific modules that must be audited.
        - Suggest specific test cases (e.g., "Test the token refresh logic in auth.py").
        """
        return self._generate_structured(prompt, ImpactAnalysisResponse)

    async def _execute_graph(self, context: str):
        prompt = f"""
        ROLE: Software Cartographer (Architectural Visualization).
        CODE CONTEXT:
        {context}

        TASK:
        Convert this codebase into a high-level architectural map. 

        GROUPING RULES (For the 'group' field):
        - Group 1 (Entry Points): API Routes, Controllers, CLI commands, Main functions.
        - Group 2 (Core Logic): Services, Business logic, Hooks, Managers.
        - Group 3 (Infrastructure): Models, Database schemas, Utility functions, API Clients.

        LINKING RULES:
        - Source/Target must be file paths or function IDs.
        - Type should be 'import' for static structure or 'call' for execution flow.

        GOAL:
        Create a clean, non-cluttered graph that shows how data moves from the 'Entry' (Group 1) to the 'Infrastructure' (Group 3).
        """
        return self._generate_structured(prompt, GraphResponse)

    def _generate_structured(self, prompt: str, schema: type[BaseModel]):
        """Executes the Gemini call with forced Pydantic schema validation."""
        response = self.client.models.generate_content(
            model=self.model_id,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=schema,
                temperature=0.1,
            ),
        )
        return response.parsed.model_dump()