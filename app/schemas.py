from typing import List
from pydantic import BaseModel

class FileMetadata(BaseModel):
    path: str
    language: str
    size_bytes: int

class IndexRequest(BaseModel):
    project_name: str
    root_path: str
    files: List[FileMetadata]

class ImpactAnalysisResponse(BaseModel):
    risk_score: int  # 1-10 (How dangerous is this change?)
    explanation: str
    affected_modules: List[str]  # Paths to files that might break
    suggested_tests: List[str]  # Specific test cases to run

class Node(BaseModel):
    id: str        # e.g., "app/main.py" or "UserAuth.login()"
    label: str     # Short name for display
    type: str      # "file", "function", or "class"
    group: int     # For color-coding (e.g., 1 for backend, 2 for utils)

class Edge(BaseModel):
    source: str    # ID of the caller
    target: str    # ID of the callee
    type: str      # "import", "call", or "data_flow"

class GraphResponse(BaseModel):
    nodes: List[Node]
    links: List[Edge]
    
class AnalysisRequest(BaseModel):
    query: str
    context: str