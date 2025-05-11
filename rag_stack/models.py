from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
from fastapi import Query

class ChatRequest(BaseModel):
    query: str = Query(..., description="Query text")
    top_k: int = Query(5, description="Number of results to return")
    llm: str = "openai"

class DocumentType(str, Enum):
    PDF = "pdf"