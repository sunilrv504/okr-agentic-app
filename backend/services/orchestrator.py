from typing import Dict
from models.okr_schema import OKRStructure, Objective, KeyResult, Epic, Feature, Story, Task
from agents import kr_suggester, planner, story_generator, estimator, validator
import json
import uuid

# in-memory store
STORE: Dict[str, OKRStructure] = {}

def create_session(objective_text: str) -> str:
    obj = Objective(text=objective_text)
    struct = OKRStructure(objective=obj, krs=[], epics=[], warnings=[])
    sid = uuid.uuid4().hex
    STORE[sid] = struct
    return sid

def suggest_krs(session_id: str) -> dict:
    struct = STORE[session_id]
    resp = kr_suggester.kr_suggester(struct.objective.text)
    parsed = json.loads(resp)
    krs = [KeyResult(**kr) for kr in parsed.get("krs", [])]
    struct.krs = krs
    return {"krs": [kr.dict() for kr in krs]}

def generate_epics(session_id: str, kr_id: str) -> dict:
    struct = STORE[session_id]
    kr = next((k for k in struct.krs if k.id == kr_id or k.dict().get("id")==kr_id), None)
    if not kr:
        # try find by text match
        kr = next((k for k in struct.krs if k.text == kr_id), None)
    if not kr:
        raise ValueError("KR not found")
    resp = planner.planner(struct.objective.text, kr.dict())
    parsed = json.loads(resp)
    epics = []
    for e in parsed.get("epics", []):
        features = []
        for f in e.get("features", []):
            features.append(Feature(title=f.get("title"), description=f.get("description","")))
        epics.append(Epic(title=e.get("title"), features=features))
    struct.epics = epics
    return {"epics": [e.dict() for e in epics]}

def generate_stories(session_id: str, feature_id: str) -> dict:
    struct = STORE[session_id]
    feat = None
    for epic in struct.epics:
        for f in epic.features:
            if f.id == feature_id or f.title == feature_id:
                feat = f
                break
    if not feat:
        raise ValueError("Feature not found")
    resp = story_generator.story_generator(feat.dict())
    parsed = json.loads(resp)
    stories = []
    for s in parsed.get("stories", []):
        stories.append(Story(title=s.get("title"),
                             acceptance_criteria=s.get("acceptance_criteria", []),
                             story_points=int(s.get("story_points", 1))))
    feat.stories = stories
    return {"stories":[s.dict() for s in stories]}

def generate_tasks(session_id: str, story_id: str) -> dict:
    struct = STORE[session_id]
    story_obj = None
    for epic in struct.epics:
        for feat in epic.features:
            for s in feat.stories:
                if s.id == story_id or s.title == story_id:
                    story_obj = s
                    break
    if not story_obj:
        raise ValueError("Story not found")
    resp = estimator.estimator(story_obj.dict())
    parsed = json.loads(resp)
    tasks = []
    for t in parsed.get("tasks", []):
        tasks.append(Task(title=t.get("title"), hours=float(t.get("hours", 1))))
    story_obj.tasks = tasks
    return {"tasks":[t.dict() for t in tasks]}

def validate_structure(session_id: str) -> dict:
    struct = STORE[session_id]
    resp = validator.validator(struct.dict())
    parsed = json.loads(resp)
    struct.warnings = parsed.get("warnings", [])
    return {"warnings": struct.warnings}

def export_structure(session_id: str) -> dict:
    struct = STORE[session_id]
    return struct.dict()