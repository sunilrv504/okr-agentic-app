"""
🔧 Jira Configuration Helper

Follow these steps to configure Jira integration:

1. GET NEW API TOKEN:
   - Visit: https://id.atlassian.com/manage-profile/security/api-tokens
   - Create new token with label "OKR App"
   - Copy the token

2. FIND PROJECT KEY:
   - Go to: https://sunilrv504-1762444323023.atlassian.net
   - Look at existing projects OR create new one
   - Project key is usually 2-4 capital letters (like "OKR", "TEST", "PROJ")

3. UPDATE .ENV FILE:
   Create/update .env file in backend/ folder with:
   
   JIRA_URL=https://sunilrv504-1762444323023.atlassian.net
   JIRA_EMAIL=sunilrv504@gmail.com
   JIRA_API_TOKEN=YOUR_NEW_TOKEN_HERE
   JIRA_PROJECT_KEY=YOUR_PROJECT_KEY_HERE

4. TEST CONNECTION:
   Run: python test_jira_connection.py

Common Project Keys:
- OKR (for OKR projects)
- GOAL (for goal tracking)  
- PLAN (for planning)
- TEST (for testing)
- PROJ (generic project)

Need help? The project key appears in:
- Project sidebar in Jira
- URL when viewing project: /projects/PROJECTKEY/
- Project settings page
"""

def get_user_input():
    print("🔧 Jira Configuration Helper")
    print("=" * 40)
    
    # Get inputs
    api_token = input("\n📋 Enter your new API token: ").strip()
    project_key = input("🔑 Enter your project key (e.g., OKR, PROJ): ").strip().upper()
    
    # Create .env content
    env_content = f"""JIRA_URL=https://sunilrv504-1762444323023.atlassian.net
JIRA_EMAIL=sunilrv504@gmail.com
JIRA_API_TOKEN={api_token}
JIRA_PROJECT_KEY={project_key}"""
    
    # Write .env file
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print(f"\n✅ Created .env file with your settings!")
    print(f"   Project Key: {project_key}")
    print(f"   API Token: {api_token[:10]}...")
    print(f"\n🚀 Now restart your backend server and try uploading to Jira!")

if __name__ == "__main__":
    get_user_input()