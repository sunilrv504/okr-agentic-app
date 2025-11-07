import json
import uuid

def handler(request):
    """
    Vercel serverless function handler for session creation
    """
    # Handle OPTIONS for CORS
    if request.method == 'OPTIONS':
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": ""
        }
    
    if request.method != 'POST':
        return {
            "statusCode": 405,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": {"error": "Method not allowed"}
        }
    
    try:
        # Get request body
        if hasattr(request, 'json') and request.json:
            data = request.json
        else:
            # Fallback for different request formats
            body = request.get('body', '{}')
            if isinstance(body, str):
                data = json.loads(body)
            else:
                data = body
        
        # Extract objective
        objective = data.get('objective', '').strip()
        if not objective:
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": {"error": "Objective is required"}
            }
        
        # Create session (simplified for serverless)
        session_id = str(uuid.uuid4())
        
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": {
                "session_id": session_id,
                "objective": objective,
                "status": "created"
            }
        }
        
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": {"error": f"Internal server error: {str(e)}"}
        }