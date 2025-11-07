import httpx
import json
import base64
from typing import Dict, List

class JiraIntegration:
    def __init__(self, base_url: str, email: str, api_token: str):
        """
        Initialize Jira integration for free Jira Cloud instances.
        
        Args:
            base_url: Your Jira site URL (e.g., https://yourcompany.atlassian.net)
            email: Your Atlassian account email
            api_token: API token from Atlassian account settings
        """
        self.base_url = base_url.rstrip('/')
        self.auth = base64.b64encode(f"{email}:{api_token}".encode()).decode()
        self.headers = {
            "Authorization": f"Basic {self.auth}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
    
    async def create_project_structure(self, project_key: str, structure: Dict) -> Dict:
        """
        Create complete project structure in Jira from OKR breakdown.
        
        Args:
            project_key: Jira project key (e.g., 'PROJ')
            structure: OKR structure from orchestrator
            
        Returns:
            Dictionary with creation results and issue IDs
        """
        results = {
            "success": True,
            "created_issues": [],
            "errors": [],
            "summary": {}
        }
        
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                # Create Epics first
                for epic in structure.get("epics", []):
                    epic_key = await self._create_epic(client, project_key, epic, structure.get("objective", {}))
                    if epic_key:
                        results["created_issues"].append({"type": "Epic", "key": epic_key, "title": epic["title"]})
                        
                        # Create Stories for each Feature in the Epic
                        for feature in epic.get("features", []):
                            for story in feature.get("stories", []):
                                story_key = await self._create_story(client, project_key, story, epic_key, feature)
                                if story_key:
                                    results["created_issues"].append({"type": "Story", "key": story_key, "title": story["title"]})
                                    
                                    # Create Sub-tasks for each Task in the Story
                                    for task in story.get("tasks", []):
                                        task_key = await self._create_subtask(client, project_key, task, story_key)
                                        if task_key:
                                            results["created_issues"].append({"type": "Sub-task", "key": task_key, "title": task["title"]})
                
                results["summary"] = {
                    "epics": len([i for i in results["created_issues"] if i["type"] == "Epic"]),
                    "stories": len([i for i in results["created_issues"] if i["type"] == "Story"]),
                    "subtasks": len([i for i in results["created_issues"] if i["type"] == "Sub-task"])
                }
                
        except Exception as e:
            results["success"] = False
            results["errors"].append(f"Integration error: {str(e)}")
        
        return results
    
    async def _create_epic(self, client: httpx.AsyncClient, project_key: str, epic: Dict, objective: Dict) -> str:
        """Create Epic in Jira"""
        try:
            # Format description in Atlassian Document Format
            description_adf = {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {"type": "text", "text": f"Epic: {epic['title']}"}
                        ]
                    },
                    {
                        "type": "paragraph",
                        "content": [
                            {"type": "text", "text": f"Objective: {objective.get('text', 'N/A')}"}
                        ]
                    },
                    {
                        "type": "paragraph",
                        "content": [
                            {"type": "text", "text": f"Features: {len(epic.get('features', []))}"}
                        ]
                    }
                ]
            }
            
            payload = {
                "fields": {
                    "project": {"key": project_key},
                    "summary": epic["title"],
                    "description": description_adf,
                    "issuetype": {"name": "Epic"}
                }
            }
            
            response = await client.post(
                f"{self.base_url}/rest/api/3/issue",
                headers=self.headers,
                json=payload
            )
            
            if response.status_code == 201:
                epic_key = response.json()["key"]
                print(f"✅ Created Epic: {epic_key} - {epic['title']}")
                return epic_key
            else:
                print(f"❌ Epic creation failed ({response.status_code}): {response.text}")
                return None
                
        except Exception as e:
            print(f"Error creating epic: {e}")
            return None
    
    async def _create_story(self, client: httpx.AsyncClient, project_key: str, story: Dict, epic_key: str, feature: Dict) -> str:
        """Create Story in Jira linked to Epic"""
        try:
            # Format description in Atlassian Document Format
            description_content = [
                {
                    "type": "paragraph",
                    "content": [
                        {"type": "text", "text": f"Feature: {feature.get('title', 'N/A')}"}
                    ]
                },
                {
                    "type": "paragraph",
                    "content": [
                        {"type": "text", "text": story['title']}
                    ]
                }
            ]
            
            # Add acceptance criteria
            if story.get("acceptance_criteria"):
                description_content.append({
                    "type": "paragraph",
                    "content": [
                        {"type": "text", "text": "Acceptance Criteria:", "marks": [{"type": "strong"}]}
                    ]
                })
                for criteria in story.get("acceptance_criteria", []):
                    description_content.append({
                        "type": "bulletList",
                        "content": [{
                            "type": "listItem",
                            "content": [{
                                "type": "paragraph",
                                "content": [{"type": "text", "text": criteria}]
                            }]
                        }]
                    })
            
            # Add story points if available
            if story.get("story_points"):
                description_content.append({
                    "type": "paragraph",
                    "content": [
                        {"type": "text", "text": f"Story Points: {story['story_points']}", "marks": [{"type": "strong"}]}
                    ]
                })
            
            description_adf = {
                "type": "doc",
                "version": 1,
                "content": description_content
            }
            
            payload = {
                "fields": {
                    "project": {"key": project_key},
                    "summary": story["title"],
                    "description": description_adf,
                    "issuetype": {"name": "Story"}
                }
            }
            
            response = await client.post(
                f"{self.base_url}/rest/api/3/issue",
                headers=self.headers,
                json=payload
            )
            
            if response.status_code == 201:
                story_key = response.json()["key"]
                print(f"✅ Created Story: {story_key} - {story['title']}")
                # Try to create issue link between story and epic
                await self._create_epic_link(client, story_key, epic_key)
                return story_key
            else:
                print(f"❌ Story creation failed ({response.status_code}): {response.text}")
                return None
                
        except Exception as e:
            print(f"Error creating story: {e}")
            return None
    
    async def _create_subtask(self, client: httpx.AsyncClient, project_key: str, task: Dict, parent_key: str) -> str:
        """Create Sub-task in Jira linked to Story"""
        try:
            # Format description in Atlassian Document Format
            description_adf = {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {"type": "text", "text": f"Development task: {task['title']}"}
                        ]
                    },
                    {
                        "type": "paragraph",
                        "content": [
                            {"type": "text", "text": f"Estimated effort: {task.get('hours', 0)} hours"}
                        ]
                    }
                ]
            }
            
            # Try different common sub-task issue type names
            subtask_types = ["Sub-task", "Subtask", "Task", "Development", "Technical Task"]
            
            for issue_type in subtask_types:
                payload = {
                    "fields": {
                        "project": {"key": project_key},
                        "parent": {"key": parent_key},
                        "summary": task["title"],
                        "description": description_adf,
                        "issuetype": {"name": issue_type},
                    }
                }
            
                # Add time estimate if available
                if task.get("hours"):
                    payload["fields"]["timetracking"] = {
                        "originalEstimate": f"{task['hours']}h"
                    }
                
                response = await client.post(
                    f"{self.base_url}/rest/api/3/issue",
                    headers=self.headers,
                    json=payload
                )
                
                if response.status_code == 201:
                    task_key = response.json()["key"]
                    print(f"✅ Created Sub-task: {task_key} - {task['title']} (type: {issue_type})")
                    return task_key
                elif "valid issue type" not in response.text.lower():
                    # If it's not an issue type error, stop trying other types
                    print(f"❌ Sub-task creation failed ({response.status_code}): {response.text}")
                    return None
            
            # If all issue types failed, create as a regular Task instead
            print(f"⚠️  All sub-task types failed, creating as regular Task instead")
            payload["fields"]["issuetype"] = {"name": "Task"}
            payload["fields"].pop("parent", None)  # Remove parent field for regular tasks
            
            response = await client.post(
                f"{self.base_url}/rest/api/3/issue",
                headers=self.headers,
                json=payload
            )
            
            if response.status_code == 201:
                task_key = response.json()["key"]
                print(f"✅ Created Task (fallback): {task_key} - {task['title']}")
                return task_key
            else:
                print(f"❌ Task creation failed ({response.status_code}): {response.text}")
                return None
                
        except Exception as e:
            print(f"Error creating sub-task: {e}")
            return None
    
    async def _create_epic_link(self, client: httpx.AsyncClient, story_key: str, epic_key: str) -> bool:
        """Create link between story and epic using issue links"""
        try:
            # Try different common link types
            link_types = ["Blocks", "Relates", "Cloners", "Epic-Story Link"]
            
            for link_type in link_types:
                payload = {
                    "type": {
                        "name": link_type
                    },
                    "inwardIssue": {
                        "key": story_key
                    },
                    "outwardIssue": {
                        "key": epic_key
                    }
                }
            
                response = await client.post(
                    f"{self.base_url}/rest/api/3/issueLink",
                    headers=self.headers,
                    json=payload
                )
                
                if response.status_code == 201:
                    print(f"✅ Linked story {story_key} to epic {epic_key} using '{link_type}'")
                    return True
                elif "system link type" not in response.text.lower():
                    # If it's not a system link type error, stop trying
                    break
            
            print(f"⚠️  Epic link failed (non-critical) - will add to description instead")
            return False
                
        except Exception as e:
            print(f"⚠️  Epic link error (non-critical): {e}")
            return False
    
    async def test_connection(self) -> Dict:
        """Test Jira connection and get project info"""
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(
                    f"{self.base_url}/rest/api/3/myself",
                    headers=self.headers
                )
                
                if response.status_code == 200:
                    user_info = response.json()
                    return {
                        "success": True,
                        "user": user_info.get("displayName"),
                        "email": user_info.get("emailAddress")
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Authentication failed: {response.text}"
                    }
                    
        except Exception as e:
            return {
                "success": False,
                "error": f"Connection failed: {str(e)}"
            }
    
    async def list_projects(self) -> Dict:
        """List all available projects the user has access to"""
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(
                    f"{self.base_url}/rest/api/3/project",
                    headers=self.headers
                )
                
                if response.status_code == 200:
                    projects = response.json()
                    project_list = [
                        {
                            "key": project.get("key"),
                            "name": project.get("name"),
                            "id": project.get("id")
                        }
                        for project in projects
                    ]
                    return {
                        "success": True,
                        "projects": project_list
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to fetch projects: {response.text}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to list projects: {str(e)}"
            }
    
    async def validate_project(self, project_key: str) -> Dict:
        """Validate if a project key exists and user has access"""
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(
                    f"{self.base_url}/rest/api/3/project/{project_key}",
                    headers=self.headers
                )
                
                if response.status_code == 200:
                    project = response.json()
                    return {
                        "success": True,
                        "project": {
                            "key": project.get("key"),
                            "name": project.get("name"),
                            "id": project.get("id"),
                            "projectTypeKey": project.get("projectTypeKey")
                        }
                    }
                elif response.status_code == 404:
                    return {
                        "success": False,
                        "error": f"Project '{project_key}' not found"
                    }
                elif response.status_code == 403:
                    return {
                        "success": False,
                        "error": f"No permission to access project '{project_key}'"
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Project validation failed: {response.text}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Project validation error: {str(e)}"
            }