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
            objective = data.get('objective', '')
            gemini_api_key = data.get('gemini_api_key', '')
            
            if not objective:
                self._send_error("Objective is required", 400)
                return
            
            # Try to use real AI if API key provided
            krs = []
            if gemini_api_key:
                try:
                    # Add backend to path
                    current_dir = os.path.dirname(os.path.abspath(__file__))
                    backend_dir = os.path.join(os.path.dirname(current_dir), 'backend')
                    sys.path.insert(0, backend_dir)
                    
                    from agents.kr_suggester import suggest_krs as ai_suggest_krs
                    krs = ai_suggest_krs(objective, gemini_api_key)
                except Exception as e:
                    print(f"AI suggestion failed: {e}")
                    # Fall back to default suggestions
                    pass
            
            # Fallback to default suggestions if AI failed or no API key
            if not krs:
                krs = self._get_fallback_krs(objective)
            
            # Send response
            self._send_success({
                "krs": krs,
                "objective": objective
            })
            
        except Exception as e:
            self._send_error(f"Internal server error: {str(e)}", 500)
    
    def _get_fallback_krs(self, objective):
        """Generate fallback KRs based on objective keywords"""
        if "increase" in objective.lower() or "grow" in objective.lower():
            return [
                {
                    "id": "kr1",
                    "text": "Increase primary metric by 25%",
                    "metric": "Percentage improvement",
                    "baseline": "Current baseline",
                    "target": "25% increase",
                    "rationale": "Achievable growth target"
                },
                {
                    "id": "kr2", 
                    "text": "Improve secondary metrics by 15%",
                    "metric": "Performance indicator",
                    "baseline": "Current level",
                    "target": "15% improvement",
                    "rationale": "Supporting improvement metric"
                },
                {
                    "id": "kr3",
                    "text": "Launch 3 new initiatives",
                    "metric": "Number of initiatives",
                    "baseline": "0 new initiatives",
                    "target": "3 launched initiatives", 
                    "rationale": "Drive innovation and progress"
                }
            ]
        else:
            return [
                {
                    "id": "kr1",
                    "text": f"Achieve measurable progress toward: {objective[:50]}...",
                    "metric": "Progress percentage",
                    "baseline": "0% progress",
                    "target": "100% completion",
                    "rationale": "Direct objective achievement"
                },
                {
                    "id": "kr2",
                    "text": "Establish key success metrics",
                    "metric": "Metrics defined",
                    "baseline": "No metrics",
                    "target": "5 key metrics",
                    "rationale": "Measurement framework"
                },
                {
                    "id": "kr3", 
                    "text": "Implementation milestone completion",
                    "metric": "Milestones completed",
                    "baseline": "0 milestones",
                    "target": "All key milestones",
                    "rationale": "Structured progress tracking"
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