import json
from agents._llm import call_gemini

def estimator(story: dict) -> str:
    """
    For a story, return JSON:
    {"tasks":[{"id":"t1","title":"...","hours":4}, ...]}
    """
    prompt = f"""
User Story: {story.get('title', '')}
Acceptance Criteria: {', '.join(story.get('acceptance_criteria', []))}

Task: Break down this user story into 3-7 development tasks with realistic hour estimates.

Consider:
- Frontend development tasks
- Backend development tasks  
- Testing and QA tasks
- Documentation tasks
- Integration tasks

Return only valid JSON in this exact format:
{{"tasks":[{{"id":"task-1","title":"Create user interface components","hours":6}},{{"id":"task-2","title":"Implement backend API endpoints","hours":8}}]}}

No markdown formatting, just pure JSON.
"""
    resp = call_gemini(prompt, max_tokens=600)
    try:
        parsed = json.loads(resp)
        if "error" in parsed:
            raise Exception("LLM unavailable")
        return json.dumps(parsed)
    except Exception:
        # Extract JSON from markdown code blocks or plain text
        import re
        
        # Try to extract from ```json blocks first
        json_match = re.search(r'```json\s*(\{.*?\})\s*```', resp, re.S)
        if json_match:
            try:
                json_str = json_match.group(1)
                parsed = json.loads(json_str)
                if "error" not in parsed:
                    return json_str
            except:
                pass
        
        # try to find JSON object in text
        m = re.search(r'(\{{.*\}})', resp, re.S)
        if m:
            try:
                parsed = json.loads(m.group(1))
                if "error" not in parsed:
                    return m.group(1)
            except:
                pass
        fallback = {"tasks":[
            {"id":"task-1","title":"Design UI","hours":4},
            {"id":"task-2","title":"Implement backend","hours":8},
            {"id":"task-3","title":"Tests & QA","hours":3}
        ]}
        return json.dumps(fallback)