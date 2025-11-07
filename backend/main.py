from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError
from dotenv import load_dotenv
from services import orchestrator
from services.jira_integration import JiraIntegration
import uvicorn
import os

load_dotenv()

app = FastAPI(title="OKR Agentic App")

# Add custom validation error handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print(f"❌ Validation Error on {request.method} {request.url}")
    print(f"   Errors: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={"detail": f"Validation failed: {exc.errors()}"}
    )

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],  # Allows requests from React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ObjectiveIn(BaseModel):
    text: str

class SessionId(BaseModel):
    session_id: str

class SelectKR(BaseModel):
    session_id: str
    kr_id: str

class SelectFeature(BaseModel):
    session_id: str
    feature_id: str

class SelectStory(BaseModel):
    session_id: str
    story_id: str

class JiraConfig(BaseModel):
    base_url: str
    email: str
    api_token: str
    project_key: str

class JiraUpload(BaseModel):
    session_id: str
    jira_config: JiraConfig

@app.post("/session", tags=["session"])
def create_session(obj: ObjectiveIn):
    sid = orchestrator.create_session(obj.text)
    return {"session_id": sid}

@app.post("/suggest_krs", tags=["krs"])
def suggest_krs(s: SessionId):
    try:
        return orchestrator.suggest_krs(s.session_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/generate_epics", tags=["planner"])
def generate_epics(sel: SelectKR):
    try:
        return orchestrator.generate_epics(sel.session_id, sel.kr_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/generate_stories", tags=["planner"])
def generate_stories(sel: SelectFeature):
    try:
        return orchestrator.generate_stories(sel.session_id, sel.feature_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/generate_tasks", tags=["planner"])
def generate_tasks(sel: SelectStory):
    try:
        return orchestrator.generate_tasks(sel.session_id, sel.story_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/validate", tags=["validator"])
def validate(s: SessionId):
    try:
        return orchestrator.validate_structure(s.session_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/export/{session_id}", tags=["export"])
def export(session_id: str):
    try:
        return orchestrator.export_structure(session_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/jira/config", tags=["jira"])
def get_jira_config():
    """Get default Jira configuration from environment variables"""
    return {
        "base_url": os.getenv("JIRA_URL", ""),
        "email": os.getenv("JIRA_EMAIL", ""),
        "project_key": os.getenv("JIRA_PROJECT_KEY", ""),
        "api_token": os.getenv("JIRA_API_TOKEN", ""),  # Include the token for convenience
        "has_token": bool(os.getenv("JIRA_API_TOKEN"))
    }

@app.post("/jira/test", tags=["jira"])
async def test_jira_connection(config: JiraConfig):
    """Test Jira connection with provided credentials"""
    try:
        jira = JiraIntegration(config.base_url, config.email, config.api_token)
        result = await jira.test_connection()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/jira/upload", tags=["jira"])
async def upload_to_jira(upload_data: JiraUpload):
    """Upload OKR structure directly to Jira project"""
    try:
        print(f"🚀 Starting Jira upload for session: {upload_data.session_id}")
        print(f"📋 Request data: session_id={upload_data.session_id}, project_key={upload_data.jira_config.project_key}")
        
        # Get the structure
        structure = orchestrator.export_structure(upload_data.session_id)
        print(f"📊 Structure retrieved: {len(structure.get('epics', []))} epics found")
        
        if not structure:
            raise HTTPException(status_code=400, detail="No session data found. Please complete the workflow first.")
            
        if not structure.get('epics'):
            raise HTTPException(status_code=400, detail="No epics found. Please complete steps 1-4 of the workflow.")
        
        # Validate structure has required data
        total_stories = sum(len(epic.get('features', [])) for epic in structure.get('epics', []))
        if total_stories == 0:
            raise HTTPException(status_code=400, detail="No features selected. Please select features in step 3.")
            
        print(f"📈 Structure validation passed: {len(structure.get('epics', []))} epics, {total_stories} features")
        
        # Initialize Jira integration
        jira = JiraIntegration(
            upload_data.jira_config.base_url,
            upload_data.jira_config.email,
            upload_data.jira_config.api_token
        )
        
        print(f"🔗 Uploading to Jira project: {upload_data.jira_config.project_key}")
        
        # Upload to Jira
        result = await jira.create_project_structure(upload_data.jira_config.project_key, structure)
        
        print(f"✅ Upload completed: {result.get('summary', {})}")
        return result
        
    except HTTPException:
        raise
    except ValidationError as e:
        print(f"❌ Validation error: {str(e)}")
        raise HTTPException(status_code=422, detail=f"Validation error: {str(e)}")
    except Exception as e:
        print(f"❌ Upload error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@app.post("/jira/projects", tags=["jira"])
async def list_jira_projects(config: JiraConfig):
    """List all available Jira projects for the user"""
    try:
        jira = JiraIntegration(config.base_url, config.email, config.api_token)
        result = await jira.list_projects()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/jira/validate-project/{project_key}", tags=["jira"])
async def validate_jira_project(project_key: str, config: JiraConfig):
    """Validate if a Jira project exists and user has access"""
    try:
        jira = JiraIntegration(config.base_url, config.email, config.api_token)
        result = await jira.validate_project(project_key)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# for local dev
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)