import json
from agents._llm import call_gemini

def planner(objective: str, kr: dict) -> str:
    """
    Returns JSON:
    {"epics":[{"id":"epic1","title":"...","features":[{"id":"feat1","title":"...","description":"..."}]}]}
    """
    prompt = f"""
Objective: {objective}
Key Result: {kr.get('text', '')} 
Metric: {kr.get('metric', '')}
Target: {kr.get('target', '')}

Task: Generate 2-4 Epics and 2-4 Features per Epic that will help achieve this specific Key Result.

Requirements:
- Epics must be directly related to achieving the Key Result above
- Features should be specific capabilities that support the Epic
- Make it relevant to the objective and measurable outcome
- Include id, title, and description for each feature
- Use meaningful titles that relate to the business goal

Return only valid JSON in this exact format:
{{"epics":[{{"id":"epic-1","title":"Epic Title Here","features":[{{"id":"feat-1","title":"Feature Title","description":"Detailed description of what this feature does and why it helps achieve the KR"}}]}}]}}

No markdown formatting, just pure JSON.
"""
    resp = call_gemini(prompt, max_tokens=800)
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
        # Dynamic fallback based on objective and KR
        import hashlib
        kr_hash = hashlib.md5(f"{objective}-{kr.get('text', '')}".encode()).hexdigest()[:4]
        
        kr_text = kr.get('text', 'Achieve objective goals')
        objective_words = objective.lower().split()[:3]
        
        # Generate contextual epics based on the KR and objective
        fallback = {"epics":[
            {
                "id": f"epic-{kr_hash}-1",
                "title": f"Foundation for {kr_text[:40]}...",
                "features":[
                    {"id": f"feat-{kr_hash}-1", "title": f"Core Infrastructure for {' '.join(objective_words)}", "description": f"Build essential infrastructure to support {kr.get('text', 'the key result')}"},
                    {"id": f"feat-{kr_hash}-2", "title": f"User Interface for {objective_words[0] if objective_words else 'System'}", "description": f"Create user-friendly interface elements that enable {kr.get('metric', 'progress tracking')}"},
                    {"id": f"feat-{kr_hash}-3", "title": f"Data Management for {kr.get('metric', 'Metrics')}", "description": f"Implement data collection and processing to measure {kr.get('metric', 'progress')} from {kr.get('baseline', 'current')} to {kr.get('target', 'target')}"}
                ]
            },
            {
                "id": f"epic-{kr_hash}-2", 
                "title": f"Optimization for {kr.get('metric', 'Performance')}",
                "features":[
                    {"id": f"feat-{kr_hash}-4", "title": f"Analytics & Reporting for {kr.get('metric', 'KR Tracking')}", "description": f"Provide insights and reporting to track progress toward {kr.get('target', 'the target')}"},
                    {"id": f"feat-{kr_hash}-5", "title": f"Automation for {' '.join(objective_words[:2])}", "description": f"Automate processes that directly contribute to achieving {kr.get('text', 'the key result')}"}
                ]
            }
        ]}
        return json.dumps(fallback)