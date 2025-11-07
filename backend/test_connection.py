import requests
import base64
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

JIRA_URL = os.getenv('JIRA_URL')
EMAIL = os.getenv('JIRA_EMAIL') 
API_TOKEN = os.getenv('JIRA_API_TOKEN')
PROJECT_KEY = os.getenv('JIRA_PROJECT_KEY')

print(f"🔍 Testing Jira connection...")
print(f"   URL: {JIRA_URL}")
print(f"   Email: {EMAIL}")
print(f"   Project Key: {PROJECT_KEY}")

# Create auth header
auth_string = f"{EMAIL}:{API_TOKEN}"
auth_bytes = base64.b64encode(auth_string.encode()).decode()

headers = {
    "Authorization": f"Basic {auth_bytes}",
    "Accept": "application/json"
}

try:
    # Test connection
    response = requests.get(f"{JIRA_URL}/rest/api/3/myself", headers=headers)
    if response.status_code == 200:
        user_info = response.json()
        print(f"✅ Connection successful!")
        print(f"   User: {user_info.get('displayName', 'N/A')}")
    else:
        print(f"❌ Connection failed: {response.status_code}")
        print(f"   Response: {response.text}")
        exit()

    # Test project access
    response = requests.get(f"{JIRA_URL}/rest/api/3/project/{PROJECT_KEY}", headers=headers)
    if response.status_code == 200:
        project = response.json()
        print(f"✅ Project '{PROJECT_KEY}' found!")
        print(f"   Name: {project.get('name')}")
        print(f"   Type: {project.get('projectTypeKey')}")
        print(f"\n🎉 Jira integration is ready! You can now upload your OKRs to Jira.")
    else:
        print(f"❌ Project '{PROJECT_KEY}' not found: {response.status_code}")
        print(f"   Response: {response.text}")
        
        # Show available projects
        print(f"\n🔍 Available projects:")
        response = requests.get(f"{JIRA_URL}/rest/api/3/project", headers=headers)
        if response.status_code == 200:
            projects = response.json()
            for p in projects:
                print(f"   - {p.get('key')}: {p.get('name')}")
        
except Exception as e:
    print(f"❌ Error: {e}")