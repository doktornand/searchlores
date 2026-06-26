from pydantic import BaseModel
from typing import List

class Metadata(BaseModel):
    name: str
    author: str
    version: str

class Investigation(BaseModel):
    assumptions: List[str] = []
    myths: List[str] = []
    vectors: List[str] = []
    questions: List[str] = []

class Lore(BaseModel):
    version: str
    metadata: Metadata
    investigation: Investigation