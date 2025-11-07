import json
import sys
import os
from http.server import BaseHTTPRequestHandler

# Add backend directory to Python path for imports
backend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'backend')
sys.path.insert(0, backend_path)

# Import backend modules
from agents.kr_suggester import suggest_krs
from agents.planner import generate_epics
from agents.story_generator import generate_stories
from agents.estimator import generate_tasks
from agents.validator import validate_structure
from services.orchestrator import create_session, add_epics, add_stories, add_tasks, export_structure
from services.jira_integration import JiraIntegration

def setup_cors_headers(handler_instance):
    """Setup CORS headers for all API responses"""
    handler_instance.send_header('Access-Control-Allow-Origin', '*')
    handler_instance.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')
    handler_instance.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')

def handle_preflight(handler_instance):
    """Handle OPTIONS preflight requests"""
    handler_instance.send_response(200)
    setup_cors_headers(handler_instance)
    handler_instance.end_headers()
    return

def get_request_body(handler_instance):
    """Extract and parse JSON request body"""
    try:
        content_length = int(handler_instance.headers['Content-Length'])
        post_data = handler_instance.rfile.read(content_length)
        return json.loads(post_data.decode('utf-8'))
    except Exception as e:
        return None

def send_json_response(handler_instance, data, status_code=200):
    """Send JSON response with proper headers"""
    handler_instance.send_response(status_code)
    handler_instance.send_header('Content-type', 'application/json')
    setup_cors_headers(handler_instance)
    handler_instance.end_headers()
    handler_instance.wfile.write(json.dumps(data).encode())

def send_error_response(handler_instance, message, status_code=400):
    """Send error response"""
    error_data = {"error": message, "status_code": status_code}
    send_json_response(handler_instance, error_data, status_code)