from pydantic import BaseModel
from typing import List, Optional

class FileMetadata(BaseModel):
    path: str
    language: str
    size_bytes: int

class IndexRequest(BaseModel):
    project_name: str
    root_path: str
    files: List[FileMetadata]

class ImpactAnalysisResponse(BaseModel):
    risk_score: int  # 1-10
    explanation: str
    affected_modules: List[str]
    suggested_tests: List[str]

class Node(BaseModel):
    id: str        
    label: str     
    type: str      
    group: int     

class Edge(BaseModel):
    source: str    
    target: str    
    type: str      

class GraphResponse(BaseModel):
    nodes: List[Node]
    links: List[Edge]

# Additional schema for Feature 1 (Search)
class SearchResult(BaseModel):
    file_path: str
    explanation: str
    relevance_score: int

class SearchResponse(BaseModel):
    results: List[SearchResult]
    summary: str