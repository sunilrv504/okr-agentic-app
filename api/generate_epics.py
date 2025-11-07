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
            selected_kr = data.get('selected_kr', {})
            gemini_api_key = data.get('gemini_api_key', '')
            
            if not session_id or not selected_kr:
                self._send_error("Session ID and selected KR are required", 400)
                return
            
            # Try to use real AI if API key provided
            epics = []
            if gemini_api_key:
                try:
                    # Add backend to path
                    current_dir = os.path.dirname(os.path.abspath(__file__))
                    backend_dir = os.path.join(os.path.dirname(current_dir), 'backend')
                    sys.path.insert(0, backend_dir)
                    
                    from agents.planner import generate_epics as ai_generate_epics
                    epics = ai_generate_epics(selected_kr, gemini_api_key)
                except Exception as e:
                    print(f"AI epic generation failed: {e}")
                    # Fall back to default epics
                    pass
            
            # Fallback to default epics if AI failed or no API key
            if not epics:
                epics = self._get_fallback_epics(selected_kr)
            
            # Send response
            self._send_success({
                "epics": epics,
                "session_id": session_id,
                "selected_kr": selected_kr
            })
            
        except Exception as e:
            self._send_error(f"Internal server error: {str(e)}", 500)
    
    def _get_fallback_epics(self, selected_kr):
        """Generate fallback epics based on KR"""
        kr_text = selected_kr.get('text', '')
        
        return [
            {
                "id": "epic1",
                "title": f"Foundation for {kr_text[:30]}...",
                "features": [
                    {
                        "id": "feature1",
                        "title": "Core Infrastructure",
                        "description": "Establish the foundational systems and processes"
                    },
                    {
                        "id": "feature2", 
                        "title": "Initial Implementation",
                        "description": "Begin core development and setup"
                    }
                ]
            },
            {
                "id": "epic2",
                "title": f"Optimization for {selected_kr.get('metric', 'Progress')}",
                "features": [
                    {
                        "id": "feature3",
                        "title": "Performance Enhancement",
                        "description": "Improve efficiency and effectiveness"
                    },
                    {
                        "id": "feature4",
                        "title": "Quality Assurance",
                        "description": "Ensure high quality standards"
                    }
                ]
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