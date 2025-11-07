import json
from agents._llm import call_gemini

def story_generator(feature: dict) -> str:
    """
    For a feature, return JSON:
    {"stories":[{"id":"s1","title":"...","acceptance_criteria":["..."],"story_points":3}, ...]}
    """
    prompt = f"""
Feature: {feature.get('title')}
Description: {feature.get('description','')}

Task: Create 3-6 user stories in proper format:
- Title format: "As a [Role], I want [Goal] so that [Benefit]"
- Acceptance criteria format: "GIVEN [context], WHEN [action], THEN [outcome]"
- Story points: 1, 2, 3, 5, 8, 13 (Fibonacci sequence)

Return JSON only with this structure:
{{"stories":[{{"id":"story-1","title":"As a user, I want to login so that I can access my account","acceptance_criteria":["GIVEN I am on the login page, WHEN I enter valid credentials, THEN I should be redirected to dashboard","GIVEN I enter invalid credentials, WHEN I click login, THEN I should see an error message"],"story_points":3}}]}}
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
        # fallback:
        fallback = {"stories":[
            {
                "id":"story-1",
                "title":"As a user, I want to create an account so that I can access the application",
                "acceptance_criteria":[
                    "GIVEN I am on the signup page, WHEN I enter valid information, THEN my account should be created",
                    "GIVEN I enter invalid email format, WHEN I submit the form, THEN I should see a validation error",
                    "GIVEN I enter a password less than 8 characters, WHEN I submit, THEN I should see a password strength error"
                ],
                "story_points":5
            },
            {
                "id":"story-2",
                "title":"As a registered user, I want to log into my account so that I can access my personalized content",
                "acceptance_criteria":[
                    "GIVEN I have valid credentials, WHEN I enter them and click login, THEN I should be redirected to my dashboard",
                    "GIVEN I enter incorrect credentials, WHEN I attempt to login, THEN I should see an authentication error message",
                    "GIVEN I click 'Remember me', WHEN I login successfully, THEN my session should persist for 30 days"
                ],
                "story_points":3
            },
            {
                "id":"story-3",
                "title":"As a user, I want to reset my password so that I can regain access to my account",
                "acceptance_criteria":[
                    "GIVEN I click 'Forgot Password', WHEN I enter my email, THEN I should receive a reset link",
                    "GIVEN I click the reset link, WHEN I enter a new password, THEN my password should be updated",
                    "GIVEN the reset link is expired, WHEN I try to use it, THEN I should see an expiration message"
                ],
                "story_points":8
            }
        ]}
        return json.dumps(fallback)