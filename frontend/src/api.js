const API_BASE = "http://localhost:8000";

export async function createSession(objective) {
  const r = await fetch(`${API_BASE}/session`, {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({text: objective})
  });
  return r.json();
}

export async function suggestKRs(session_id){
  const r = await fetch(`${API_BASE}/suggest_krs`, {
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body: JSON.stringify({session_id})
  });
  return r.json();
}

export async function generateEpics(session_id, kr_id){
  const r = await fetch(`${API_BASE}/generate_epics`, {
    method:"POST", headers:{"Content-Type":"application/json"},
    body: JSON.stringify({session_id, kr_id})
  });
  return r.json();
}

export async function generateStories(session_id, feature_id){
  const r = await fetch(`${API_BASE}/generate_stories`, {
    method:"POST", headers:{"Content-Type":"application/json"},
    body: JSON.stringify({session_id, feature_id})
  });
  return r.json();
}

export async function generateTasks(session_id, story_id){
  const r = await fetch(`${API_BASE}/generate_tasks`, {
    method:"POST", headers:{"Content-Type":"application/json"},
    body: JSON.stringify({session_id, story_id})
  });
  return r.json();
}

export async function validate(session_id){
  const r = await fetch(`${API_BASE}/validate`, {
    method:"POST", headers:{"Content-Type":"application/json"},
    body: JSON.stringify({session_id})
  });
  return r.json();
}

export async function exportJSON(session_id){
  const r = await fetch(`${API_BASE}/export/${session_id}`);
  return r.json();
}

export async function testJiraConnection(jiraConfig){
  const r = await fetch(`${API_BASE}/jira/test`, {
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body: JSON.stringify(jiraConfig)
  });
  return r.json();
}

export async function getJiraConfig(){
  const r = await fetch(`${API_BASE}/jira/config`);
  return r.json();
}

export async function uploadToJira(session_id, jiraConfig){
  const r = await fetch(`${API_BASE}/jira/upload`, {
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body: JSON.stringify({session_id, jira_config: jiraConfig})
  });
  return r.json();
}