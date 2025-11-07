import requests
import base64
import json

# Your Jira credentials
JIRA_URL = "https://sunilrv504-1762444323023.atlassian.net"
EMAIL = "sunilrv504@gmail.com"
API_TOKEN = "ATATT3xFfGF0E9sFfd3laxwLo1YsmkZC6DrZ31Pf1Nzd7dRNFfPZWK0JgNT2A3Abrs4-Za6MSdYcEAJLE4GviN3d2SzOGvH6LaCAZvtcmyhMKly7wg6ubIKNaK3hrpsRYC0lU=11A049CA"

# Create auth header
auth_string = f"{EMAIL}:{API_TOKEN}"
auth_bytes = base64.b64encode(auth_string.encode()).decode()

headers = {
    "Authorization": f"Basic {auth_bytes}",
    "Accept": "application/json"
}

print("🔍 Fetching your Jira projects...")

try:
    # Get all projects
    response = requests.get(f"{JIRA_URL}/rest/api/3/project", headers=headers)
    
    if response.status_code == 200:
        projects = response.json()
        print(f"\n📋 Found {len(projects)} projects in your Jira instance:")
        print("=" * 60)
        
        for project in projects:
            key = project.get('key', 'N/A')
            name = project.get('name', 'N/A')
            project_type = project.get('projectTypeKey', 'N/A')
            
            print(f"🔑 Project Key: {key}")
            print(f"📝 Name: {name}")
            print(f"🏷️  Type: {project_type}")
            print("-" * 40)
            
        print(f"\n✅ Use any of the Project Keys above in your .env file")
        print(f"   Current setting: JIRA_PROJECT_KEY=AI-JIRA")
        print(f"   Example: JIRA_PROJECT_KEY={projects[0]['key'] if projects else 'PROJ'}")
        
    else:
        print(f"❌ Error {response.status_code}: {response.text}")
        
except Exception as e:
    print(f"❌ Connection error: {e}")