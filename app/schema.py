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
