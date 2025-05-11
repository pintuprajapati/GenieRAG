from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
from fastapi import Query

class DocumentType(str, Enum):
    PDF = "pdf"