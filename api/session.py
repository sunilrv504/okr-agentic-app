import json
import uuid

def handler(request):
    # Handle OPTIONS for CORS preflight
    if request.method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
            },
            'body': ''
        }
    
    if request.method != 'POST':
        return {
            'statusCode': 405,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps({"error": "Method not allowed"})
        }
    
    try:
        # Get request body
        body = getattr(request, 'body', '{}')
        if isinstance(body, bytes):
            body = body.decode('utf-8')
        
        data = json.loads(body) if body else {}
        
        # Extract objective
        objective = data.get('objective', '').strip()
        if not objective:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                },
                'body': json.dumps({"error": "Objective is required"})
            }
        
        # Create session
        session_id = str(uuid.uuid4())
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps({
                "session_id": session_id,
                "objective": objective,
                "status": "created"
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps({"error": f"Internal server error: {str(e)}"})
        }