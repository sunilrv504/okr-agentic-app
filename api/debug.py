from http.server import BaseHTTPRequestHandler
import json
import os
import sys

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        debug_info = {
            "status": "debug endpoint working",
            "python_version": sys.version,
            "current_directory": os.getcwd(),
            "environment_vars": dict(os.environ),
            "files_in_current_dir": os.listdir('.') if os.path.exists('.') else "no current dir"
        }
        
        self.wfile.write(json.dumps(debug_info, indent=2).encode())