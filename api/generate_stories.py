from http.server import BaseHTTPRequestHandler
import json
import sys
import os

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_POST(self):
        try:
            # Get request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # Extract parameters
            session_id = data.get('session_id', '')
            selected_feature = data.get('selected_feature', {})
            gemini_api_key = data.get('gemini_api_key', '')
            
            if not session_id or not selected_feature:
                self._send_error("Session ID and selected feature are required", 400)
                return
            
            # Try to use real AI if API key provided
            stories = []
            if gemini_api_key:
                try:
                    # Add backend to path
                    current_dir = os.path.dirname(os.path.abspath(__file__))
                    backend_dir = os.path.join(os.path.dirname(current_dir), 'backend')
                    sys.path.insert(0, backend_dir)
                    
                    from agents.story_generator import generate_stories as ai_generate_stories
                    stories = ai_generate_stories(selected_feature, gemini_api_key)
                except Exception as e:
                    print(f"AI story generation failed: {e}")
                    # Fall back to default stories
                    pass
            
            # Fallback to default stories if AI failed or no API key
            if not stories:
                stories = self._get_fallback_stories(selected_feature)
            
            # Send response
            self._send_success({
                "stories": stories,
                "session_id": session_id,
                "selected_feature": selected_feature
            })
            
        except Exception as e:
            self._send_error(f"Internal server error: {str(e)}", 500)
    
    def _get_fallback_stories(self, selected_feature):
        """Generate fallback user stories based on feature"""
        feature_title = selected_feature.get('title', 'Feature')
        
        return [
            {
                "id": "story1",
                "title": f"As a user, I want to create an account so that I can access the application",
                "acceptance_criteria": [
                    "GIVEN I am on the signup page, WHEN I enter valid credentials, THEN my account is created",
                    "GIVEN I have an account, WHEN I log in, THEN I can access the dashboard",
                    "GIVEN I enter invalid data, WHEN I submit, THEN I see validation errors"
                ],
                "story_points": 5
            },
            {
                "id": "story2", 
                "title": f"As a registered user, I want to log in so that I can use the system securely",
                "acceptance_criteria": [
                    "GIVEN I have valid credentials, WHEN I log in, THEN I am authenticated",
                    "GIVEN I enter wrong credentials, WHEN I submit, THEN I see an error message",
                    "GIVEN I am logged in, WHEN I navigate, THEN my session is maintained"
                ],
                "story_points": 3
            },
            {
                "id": "story3",
                "title": f"As a user, I want to manage my profile so that I can keep my information up to date",
                "acceptance_criteria": [
                    "GIVEN I am logged in, WHEN I access my profile, THEN I can view my information",
                    "GIVEN I update my profile, WHEN I save, THEN changes are persisted",
                    "GIVEN invalid data, WHEN I save, THEN I see validation messages"
                ],
                "story_points": 8
            }
        ]
    
    def _send_success(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def _send_error(self, message, status_code):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        error_response = {"error": message}
        self.wfile.write(json.dumps(error_response).encode())