import json
from agents._llm import call_gemini

def kr_suggester(objective: str) -> str:
    """
    Returns strict JSON:
    {"krs":[{"id":"kr1","text":"...","metric":"...","baseline":"...","target":"...","rationale":"..."}]}
    """
    prompt = f"""
Objective: {objective}
Task: Suggest 4-6 measurable Key Results for this objective. Return JSON in this exact format:
{{"krs":[{{"id":"kr1","text":"Key result description","metric":"measurement unit","baseline":"current value","target":"target value","rationale":"why this KR matters"}}]}}

Return only valid JSON, no markdown formatting.
"""
    resp = call_gemini(prompt, max_tokens=600)
    # If model returns plain JSON, return it. Otherwise, attempt to extract JSON.
    try:
        parsed = json.loads(resp)
        # Check if it's an error response from LLM wrapper
        if "error" in parsed:
            raise Exception("LLM unavailable")
        return json.dumps(parsed)
    except Exception:
        # Extract JSON from markdown code blocks or plain text
        import re
        
        # Try to extract from ```json blocks first
        json_match = re.search(r'```json\s*(\[.*?\]|\{.*?\})\s*```', resp, re.S)
        if json_match:
            try:
                json_str = json_match.group(1)
                parsed = json.loads(json_str)
                # If it's an array, wrap it in the expected format
                if isinstance(parsed, list):
                    wrapped = {"krs": parsed}
                    return json.dumps(wrapped)
                # Handle different key names from LLM
                elif isinstance(parsed, dict):
                    if "key_results" in parsed:
                        parsed["krs"] = parsed.pop("key_results")
                    if "krs" in parsed and "error" not in parsed:
                        return json.dumps(parsed)
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
        # fallback: create objective-specific suggestions
        import hashlib
        obj_hash = hashlib.md5(objective.lower().encode()).hexdigest()[:4]
        
        fallback = {"krs": [
            {"id":f"kr-{obj_hash}-1","text":f"Achieve measurable progress toward: {objective[:50]}...","metric":"Progress %","baseline":"0%","target":"100%","rationale":"Direct objective measurement"},
            {"id":f"kr-{obj_hash}-2","text":"Improve user engagement metrics","metric":"User satisfaction","baseline":"70%","target":"85%","rationale":"User-focused outcome"},
            {"id":f"kr-{obj_hash}-3","text":"Increase operational efficiency","metric":"Process efficiency","baseline":"Current","target":"20% improvement","rationale":"Operational excellence"},
            {"id":f"kr-{obj_hash}-4","text":"Enhance quality metrics","metric":"Quality score","baseline":"Current","target":"Improved","rationale":"Quality assurance"}
        ]}
        return json.dumps(fallback)