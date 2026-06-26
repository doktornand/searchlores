from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime

class Metadata(BaseModel):
    name: str
    author: str
    version: str = "1.0"
    created: str = Field(default_factory=lambda: datetime.now().isoformat())
    tags: List[str] = []
    parent_lore: Optional[str] = None

class InvestigationSpec(BaseModel):
    assumptions: List[str] = []
    myths: List[str] = []
    vectors: List[str] = []
    questions: List[str] = []
    counter_questions: List[str] = []
    forbidden_answers: List[str] = []

class Lore(BaseModel):
    version: str = "1.0"
    metadata: Metadata
    investigation: InvestigationSpec

    def merge(self, other: 'Lore') -> 'Lore':
        return Lore(
            metadata=Metadata(
                name=f"{self.metadata.name} × {other.metadata.name}",
                author="LoreForge",
                tags=list(set(self.metadata.tags + other.metadata.tags))
            ),
            investigation=InvestigationSpec(
                assumptions=list(set(self.investigation.assumptions + other.investigation.assumptions)),
                myths=list(set(self.investigation.myths + other.investigation.myths)),
                vectors=list(set(self.investigation.vectors + other.investigation.vectors)),
                questions=list(set(self.investigation.questions + other.investigation.questions)),
                counter_questions=list(set(self.investigation.counter_questions + other.investigation.counter_questions)),
                forbidden_answers=list(set(self.investigation.forbidden_answers + other.investigation.forbidden_answers))
            )
        )