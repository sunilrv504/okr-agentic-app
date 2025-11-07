from http.server import BaseHTTPRequestHandler
import json
import sys
import os

# Add the backend directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(os.path.dirname(current_dir), 'backend')
sys.path.insert(0, backend_dir)

try:
    from _utils import setup_cors_headers, handle_preflight, get_request_body, send_json_response, send_error_response
    from services.orchestrator import create_session
except ImportError as e:
    # Fallback imports for local development
    def setup_cors_headers(handler_instance):
        handler_instance.send_header('Access-Control-Allow-Origin', '*')
        handler_instance.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        handler_instance.send_header('Access-Control-Allow-Headers', 'Content-Type')

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        setup_cors_headers(self)
        self.end_headers()
    
    def do_POST(self):
        try:
            # Get request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # Extract objective
            objective = data.get('objective', '').strip()
            if not objective:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                setup_cors_headers(self)
                self.end_headers()
                error_response = {"error": "Objective is required"}
                self.wfile.write(json.dumps(error_response).encode())
                return
            
            # Create session
            try:
                # Import here to avoid import issues in serverless
                sys.path.insert(0, backend_dir)
                from services.orchestrator import create_session
                session_id = create_session(objective)
            except ImportError:
                # Fallback for when backend modules aren't available
                import uuid
                session_id = str(uuid.uuid4())
            
            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            setup_cors_headers(self)
            self.end_headers()
            
            response = {
                "session_id": session_id,
                "objective": objective,
                "status": "created"
            }
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            setup_cors_headers(self)
            self.end_headers()
            error_response = {"error": f"Internal server error: {str(e)}"}
            self.wfile.write(json.dumps(error_response).encode())