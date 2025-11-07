import os
import json
import httpx
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_URL = os.getenv("GEMINI_API_URL")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def call_gemini(prompt: str, max_tokens: int = 800) -> str:
    """
    Google Gemini API wrapper. Works with Google AI Studio API.
    Expects GEMINI_API_URL and GEMINI_API_KEY in .env.
    Returns raw text (string) from the LLM.
    Falls back to error response if API is unavailable.
    """
    if not GEMINI_API_URL or not GEMINI_API_KEY:
        return '{"error": "GEMINI_API_URL and GEMINI_API_KEY must be set in .env"}'
    
    try:
        # Google AI Studio API format
        if "generativelanguage.googleapis.com" in GEMINI_API_URL:
            payload = {
                "contents": [{
                    "parts": [{"text": prompt}]
                }],
                "generationConfig": {
                    "maxOutputTokens": max_tokens,
                    "temperature": 0.7
                }
            }
            headers = {"x-goog-api-key": GEMINI_API_KEY, "Content-Type": "application/json"}
        else:
            # Generic endpoint format (fallback)
            payload = {"prompt": prompt, "max_output_tokens": max_tokens}
            headers = {"Authorization": f"Bearer {GEMINI_API_KEY}", "Content-Type": "application/json"}
        
        with httpx.Client(timeout=30) as client:
            r = client.post(GEMINI_API_URL, json=payload, headers=headers)
            r.raise_for_status()
            data = r.json()
            
            # Parse Google AI Studio response format
            if "candidates" in data and isinstance(data["candidates"], list) and data["candidates"]:
                candidate = data["candidates"][0]
                if "content" in candidate and "parts" in candidate["content"]:
                    parts = candidate["content"]["parts"]
                    if parts and "text" in parts[0]:
                        return parts[0]["text"]
            
            # Try other common response shapes
            if isinstance(data, dict):
                if "output" in data and isinstance(data["output"], str):
                    return data["output"]
                if "text" in data and isinstance(data["text"], str):
                    return data["text"]
            
            # fallback to raw text
            return json.dumps(data)
            
    except Exception as e:
        # Return error response that will trigger fallback in agents
        return f'{{"error": "API connection failed: {str(e)}"}}'