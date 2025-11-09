import json

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
        
        # Extract parameters
        objective = data.get('objective', '').strip()
        gemini_api_key = data.get('gemini_api_key', '')
        
        if not objective:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                },
                'body': json.dumps({"error": "Objective is required"})
            }
        
        # Generate fallback KRs (simplified for now)
        krs = get_fallback_krs(objective)
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps({
                "krs": krs,
                "objective": objective
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

def get_fallback_krs(objective):
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