import json

def handler(request):
    # CORS headers
    cors_headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Content-Type': 'application/json'
    }
    
    # Handle OPTIONS request
    if request.method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': cors_headers,
            'body': ''
        }
    
    # Handle GET request
    if request.method == 'GET':
        return {
            'statusCode': 200,
            'headers': cors_headers,
            'body': json.dumps({"status": "ok", "message": "Test endpoint working"})
        }
    
    # Handle POST request
    if request.method == 'POST':
        try:
            return {
                'statusCode': 200,
                'headers': cors_headers,
                'body': json.dumps({
                    "session_id": "test-123",
                    "message": "POST request successful",
                    "status": "ok"
                })
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'headers': cors_headers,
                'body': json.dumps({"error": str(e)})
            }
    
    # Method not allowed
    return {
        'statusCode': 405,
        'headers': cors_headers,
        'body': json.dumps({"error": "Method not allowed"})
    }