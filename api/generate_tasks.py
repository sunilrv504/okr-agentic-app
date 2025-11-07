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
            selected_story = data.get('selected_story', {})
            gemini_api_key = data.get('gemini_api_key', '')
            
            if not session_id or not selected_story:
                self._send_error("Session ID and selected story are required", 400)
                return
            
            # Try to use real AI if API key provided
            tasks = []
            if gemini_api_key:
                try:
                    # Add backend to path
                    current_dir = os.path.dirname(os.path.abspath(__file__))
                    backend_dir = os.path.join(os.path.dirname(current_dir), 'backend')
                    sys.path.insert(0, backend_dir)
                    
                    from agents.estimator import generate_tasks as ai_generate_tasks
                    tasks = ai_generate_tasks(selected_story, gemini_api_key)
                except Exception as e:
                    print(f"AI task generation failed: {e}")
                    # Fall back to default tasks
                    pass
            
            # Fallback to default tasks if AI failed or no API key
            if not tasks:
                tasks = self._get_fallback_tasks(selected_story)
            
            # Send response
            self._send_success({
                "tasks": tasks,
                "session_id": session_id,
                "selected_story": selected_story
            })
            
        except Exception as e:
            self._send_error(f"Internal server error: {str(e)}", 500)
    
    def _get_fallback_tasks(self, selected_story):
        """Generate fallback tasks based on story"""
        story_title = selected_story.get('title', 'Story')
        
        return [
            {
                "id": "task1",
                "title": "Design database schema and models",
                "hours": 6
            },
            {
                "id": "task2",
                "title": "Implement frontend components", 
                "hours": 12
            },
            {
                "id": "task3",
                "title": "Create backend API endpoints",
                "hours": 8
            },
            {
                "id": "task4",
                "title": "Write unit and integration tests",
                "hours": 4
            },
            {
                "id": "task5",
                "title": "Setup deployment and monitoring",
                "hours": 3
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