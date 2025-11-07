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

print("🔍 Testing Jira connection and permissions...")

# Test 1: Check connection
try:
    response = requests.get(f"{JIRA_URL}/rest/api/3/myself", headers=headers)
    if response.status_code == 200:
        user_info = response.json()
        print(f"✅ Connection successful!")
        print(f"   User: {user_info.get('displayName', 'N/A')} ({user_info.get('emailAddress', 'N/A')})")
    else:
        print(f"❌ Connection failed: {response.status_code} - {response.text}")
        exit()
except Exception as e:
    print(f"❌ Connection error: {e}")
    exit()

# Test 2: Check permissions on projects
try:
    response = requests.get(f"{JIRA_URL}/rest/api/3/project", headers=headers)
    print(f"\n📋 Project permissions check:")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        projects = response.json()
        print(f"   Found {len(projects)} projects")
        for p in projects[:3]:  # Show first 3
            print(f"   - {p.get('key')}: {p.get('name')}")
    else:
        print(f"   Error: {response.text}")
except Exception as e:
    print(f"   Error: {e}")

# Test 3: Check if we can create a project
print(f"\n🏗️ Testing project creation...")
project_data = {
    "key": "OKRTEST",
    "name": "OKR Test Project",
    "projectTypeKey": "software",
    "projectTemplateKey": "com.pyxis.greenhopper.jira:gh-simplified-agility-kanban",
    "description": "Test project for OKR application",
    "lead": EMAIL,
    "assigneeType": "PROJECT_LEAD"
}

headers_create = headers.copy()
headers_create["Content-Type"] = "application/json"

try:
    response = requests.post(
        f"{JIRA_URL}/rest/api/3/project",
        headers=headers_create,
        data=json.dumps(project_data)
    )
    
    print(f"   Create Status: {response.status_code}")
    if response.status_code in [200, 201]:
        result = response.json()
        print(f"   ✅ Project created successfully!")
        print(f"   🔑 Project Key: {result.get('key')}")
        print(f"   📝 Project Name: {result.get('name')}")
        print(f"   🌐 Project URL: {result.get('self')}")
        print(f"\n🎉 You can now use JIRA_PROJECT_KEY=OKRTEST in your .env file!")
    else:
        print(f"   ❌ Create failed: {response.text}")
        
        # Show available project types if creation failed
        print(f"\n🔍 Checking available project types...")
        response = requests.get(f"{JIRA_URL}/rest/api/3/project/type", headers=headers)
        if response.status_code == 200:
            types = response.json()
            print("   Available project types:")
            for t in types:
                print(f"   - {t.get('key')}: {t.get('formattedKey', 'N/A')}")
        
except Exception as e:
    print(f"   ❌ Error: {e}")

print(f"\n💡 Alternative solutions:")
print(f"   1. Use Jira web interface to create a project manually")
print(f"   2. Contact your Jira admin for project creation permissions")
print(f"   3. Use an existing project key if available")