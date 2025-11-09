def handler(request):
    import json
    
    # Simple health check
    response_data = {
        "status": "healthy",
        "service": "OKR Agentic Planning API",
        "version": "1.0.0"
    }
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
        },
        'body': json.dumps(response_data)
    }