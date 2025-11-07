from typing import List, Optional
from pydantic import BaseModel, Field
from uuid import uuid4

def genid(prefix: str):
    return f"{prefix}-{uuid4().hex[:8]}"

class Objective(BaseModel):
    id: str = Field(default_factory=lambda: genid("obj"))
    text: str

class KeyResult(BaseModel):
    id: str = Field(default_factory=lambda: genid("kr"))
    text: str
    metric: Optional[str] = None
    baseline: Optional[str] = None
    target: Optional[str] = None
    rationale: Optional[str] = None

class Task(BaseModel):
    id: str = Field(default_factory=lambda: genid("task"))
    title: str
    hours: float

class Story(BaseModel):
    id: str = Field(default_factory=lambda: genid("story"))
    title: str
    acceptance_criteria: List[str]
    story_points: int
    tasks: List[Task] = []

class Feature(BaseModel):
    id: str = Field(default_factory=lambda: genid("feat"))
    title: str
    description: Optional[str] = None
    stories: List[Story] = []

class Epic(BaseModel):
    id: str = Field(default_factory=lambda: genid("epic"))
    title: str
    features: List[Feature] = []

class OKRStructure(BaseModel):
    objective: Objective
    krs: List[KeyResult] = []
    epics: List[Epic] = []
    warnings: List[str] = []