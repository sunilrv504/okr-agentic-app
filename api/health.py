def handler(request):
    """
    Vercel serverless function handler
    """
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type"
        },
        "body": {
            "status": "healthy",
            "service": "OKR Agentic Planning API",
            "version": "1.0.0"
        }
    }