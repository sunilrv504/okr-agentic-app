# OKR Agentic Planning Application

<!-- Deployment trigger -->

A complete web application that takes an **Objective** as input, suggests relevant **Key Results**, and upon user selection generates a comprehensive project breakdown including EPICs, Features, User Stories with Acceptance Criteria, Story-Point Estimates, and Associated Tasks with Hour Estimates.

## 🧩 Functional Flow

1️⃣ **User enters Objective** → System creates session  
2️⃣ **System suggests 4–6 Key Results** (KR Suggester Agent)  
3️⃣ **User selects a KR** → System generates EPICs & Features (Planner Agent)  
4️⃣ **For each Feature** → System creates User Stories with acceptance criteria + story points (Story Generator Agent)  
5️⃣ **For each Story** → System decomposes into Tasks with hour estimates (Estimator Agent)  
6️⃣ **User can review/edit and export JSON** (ready for Jira import)  

## 🛠 Tech Stack

- **Backend:** Python 3.10 + FastAPI + LangChain + Pydantic
- **LLM:** Google Gemini API (configurable via .env)
- **Frontend:** React + Tailwind CSS (single-page wizard UI)
- **Persistence:** In-memory JSON store
- **Output:** Structured JSON mapping Objective → KR → Epic → Feature → Story → Task

## 🏗 Project Structure

```
OKRA/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── requirements.txt        # Python dependencies
│   ├── .env.example           # Environment variables template
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── _llm.py            # Gemini API wrapper
│   │   ├── kr_suggester.py    # Key Results suggestion agent
│   │   ├── planner.py         # Epic & Feature planning agent
│   │   ├── story_generator.py # User Story generation agent
│   │   ├── estimator.py       # Task estimation agent
│   │   └── validator.py       # Structure validation agent
│   ├── models/
│   │   ├── __init__.py
│   │   └── okr_schema.py      # Pydantic models
│   └── services/
│       ├── __init__.py
│       └── orchestrator.py    # Workflow orchestration
├── frontend/
│   ├── package.json           # Node.js dependencies
│   ├── tailwind.config.js     # Tailwind CSS configuration
│   ├── public/
│   │   └── index.html
│   └── src/
│       ├── index.js           # React entry point
│       ├── index.css          # Tailwind CSS imports
│       ├── App.jsx            # Main application component
│       ├── api.js             # API client functions
│       └── components/
│           ├── Step1Objective.jsx
│           ├── Step2KRs.jsx
│           ├── Step3Epics.jsx
│           ├── Step4Stories.jsx
│           ├── Step5Tasks.jsx
│           └── ReviewExport.jsx
└── README.md
```

## 🚀 Setup & Installation

### Prerequisites
- Python 3.10+
- Node.js 16+
- Google Gemini API access

### Backend Setup

1. **Navigate to backend directory:**
   ```powershell
   cd backend
   ```

2. **Create and activate virtual environment:**
   ```powershell
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```powershell
   copy .env.example .env
   ```
   
   Edit `.env` file with your Gemini API credentials:
   ```
   GEMINI_API_URL=https://your-actual-gemini-endpoint/v1/generate
   GEMINI_API_KEY=your_actual_gemini_api_key
   ```

5. **Start the backend server:**
   ```powershell
   uvicorn main:app --reload --port 8000
   ```
   
   The API will be available at `http://localhost:8000`
   API documentation: `http://localhost:8000/docs`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```powershell
   cd frontend
   ```

2. **Install dependencies:**
   ```powershell
   npm install
   ```

3. **Start the development server:**
   ```powershell
   npm start
   ```
   
   The application will open at `http://localhost:3000`

## 🤖 Agent Architecture

### KR Suggester Agent
- **Input:** Objective text
- **Output:** 4-6 measurable Key Results with metrics, baselines, targets, and rationale
- **Prompt Pattern:** Structured JSON schema with concise context

### Planner Agent
- **Input:** Objective + Selected Key Result
- **Output:** 2-4 Epics with 2-5 Features each
- **Function:** Derives high-level project structure

### Story Generator Agent
- **Input:** Feature details
- **Output:** 3-6 User Stories with acceptance criteria and story points (1-13)
- **Function:** Creates actionable development stories

### Estimator Agent
- **Input:** User Story details
- **Output:** 3-8 Tasks with hour estimates
- **Function:** Decomposes stories into implementable tasks

### Validator Agent
- **Input:** Complete OKR structure
- **Output:** Warnings and recommendations
- **Function:** Sanity checks and structural validation

## 📊 Data Model

The application uses a hierarchical structure:

```
Objective
├── KeyResult[]
└── Epic[]
    └── Feature[]
        └── Story[]
            └── Task[]
```

Each entity includes:
- **Objective:** `{id, text}`
- **KeyResult:** `{id, text, metric, baseline, target, rationale}`
- **Epic:** `{id, title, features[]}`
- **Feature:** `{id, title, description, stories[]}`
- **Story:** `{id, title, acceptance_criteria[], story_points, tasks[]}`
- **Task:** `{id, title, hours}`

## 🌐 API Endpoints

- `POST /session` - Create new session with objective
- `POST /suggest_krs` - Generate Key Results suggestions
- `POST /generate_epics` - Generate Epics & Features for selected KR
- `POST /generate_stories` - Generate User Stories for selected Feature
- `POST /generate_tasks` - Generate Tasks for selected Story
- `POST /validate` - Validate complete structure
- `GET /export/{session_id}` - Export complete JSON structure

## 🔧 Configuration

### Gemini LLM Integration
The `_llm.py` module provides a generic HTTP wrapper for Gemini API. Adjust the endpoint contract in the `call_gemini()` function to match your specific Gemini API implementation.

### Fallback Responses
Each agent includes fallback responses for offline testing or when the LLM is unavailable.

### In-Memory Storage
The current implementation uses in-memory storage. For persistence, replace the `STORE` dictionary in `orchestrator.py` with a database solution.

## 🎯 Usage Examples

1. **Enter Objective:** "Increase user engagement in our mobile app"
2. **Select KR:** "Increase daily active users from 10,000 to 15,000"
3. **Review Generated Structure:**
   - Epic: "User Experience Enhancement"
     - Feature: "Personalized Dashboard"
       - Story: "As a user, I want to see personalized content"
         - Task: "Design personalization algorithm (8h)"
         - Task: "Implement content filtering (12h)"

## 🔍 Troubleshooting

### Backend Issues
- **LLM Connection:** Verify `GEMINI_API_URL` and `GEMINI_API_KEY` in `.env`
- **Dependencies:** Ensure all packages in `requirements.txt` are installed
- **Port Conflicts:** Change port in `uvicorn` command if 8000 is occupied

### Frontend Issues
- **API Connection:** Ensure backend is running on `http://localhost:8000`
- **Tailwind CSS:** Lint errors for `@tailwind` directives are expected during development
- **Dependencies:** Run `npm install` if components fail to load

### Agent Responses
- **JSON Parsing:** Agents include fallback responses for invalid JSON
- **Timeout Issues:** Increase timeout in `_llm.py` if requests fail
- **Rate Limits:** Implement request throttling for production use

## � Jira Integration & Import Guide

### 🎯 **Jira Import Methods**

#### **Method 1: CSV Import (Recommended)**
1. **Export Structure**: Use the "Download JSON" feature
2. **Convert to CSV**: Transform JSON structure to Jira CSV format
3. **Jira Import**: Use Jira's built-in CSV importer

#### **Method 2: Jira REST API**
1. **API Integration**: Use Jira's REST API to programmatically create issues
2. **Bulk Creation**: Create Epics → Features → Stories → Sub-tasks
3. **Automated Import**: Direct integration without manual steps

#### **Method 3: Third-Party Tools**
- **Structure Exporter for Jira**: Import hierarchical project structures
- **Xray Test Management**: For acceptance criteria and test cases
- **BigPicture/Portfolio**: For epic and roadmap visualization

### 📋 **JSON to Jira Mapping**

```json
{
  "objective": "Jira Project Description",
  "krs": "Custom Field: Key Results",
  "epics": [
    {
      "title": "Epic Summary",
      "features": [
        {
          "title": "Story Summary (Epic Link)",
          "stories": [
            {
              "title": "Story Summary",
              "acceptance_criteria": "Story Description",
              "story_points": "Story Points Field",
              "tasks": [
                {
                  "title": "Sub-task Summary",
                  "hours": "Original Estimate"
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

### 🔧 **Step-by-Step Jira Import Process**

#### **Step 1: Prepare CSV Format**
```csv
Issue Type,Summary,Description,Epic Link,Story Points,Original Estimate,Parent
Epic,User Management & Authentication,"Epic for managing user accounts and authentication",,,,
Story,As a user I want to create an account,"GIVEN I am on signup page, WHEN I enter valid info, THEN account is created",User Management & Authentication,5,,
Sub-task,Design signup form UI,"Create responsive signup form with validation",,,4h,Story-123
Sub-task,Implement backend validation,"Add email and password validation logic",,,8h,Story-123
```

#### **Step 2: Jira Project Setup**
1. **Create New Project**: Scrum/Kanban template
2. **Configure Issue Types**: Epic, Story, Sub-task
3. **Enable Story Points**: In project settings
4. **Custom Fields**: Add "Key Results" field if needed

#### **Step 3: Import Process**
1. **System Settings** → **External System Import** → **CSV**
2. **Map Fields**: 
   - Issue Type → Issue Type
   - Summary → Summary
   - Description → Description
   - Epic Link → Epic Link
   - Story Points → Story Points
   - Original Estimate → Original Estimate
   - Parent → Parent Issue
3. **Import & Validate**: Review imported structure

### 🛠 **Enhanced Export Features (Future)**

#### **Direct Jira Export Button**
```javascript
// Future enhancement: Direct Jira API integration
async function exportToJira(projectKey, credentials) {
  const structure = await api.exportJSON(session);
  
  // Create Epics first
  for (const epic of structure.epics) {
    const epicId = await createJiraEpic(epic, projectKey);
    
    // Create Stories under Epic
    for (const feature of epic.features) {
      for (const story of feature.stories) {
        const storyId = await createJiraStory(story, epicId);
        
        // Create Sub-tasks under Story
        for (const task of story.tasks) {
          await createJiraSubtask(task, storyId);
        }
      }
    }
  }
}
```

#### **CSV Export Utility**
```python
# Backend enhancement: CSV export endpoint
@app.get("/export/csv/{session_id}")
def export_csv(session_id: str):
    structure = orchestrator.export_structure(session_id)
    csv_data = convert_to_jira_csv(structure)
    return Response(csv_data, media_type="text/csv")
```

## 🚀 Next Steps

- **Jira Direct Integration:** API-based direct export to Jira projects
- **CSV Export Feature:** One-click CSV generation for Jira import
- **Database Integration:** Replace in-memory storage with PostgreSQL/MongoDB
- **User Authentication:** Add user management and session persistence
- **Advanced Validation:** Enhanced business rules and constraints
- **Collaborative Features:** Multi-user planning sessions
- **Analytics Dashboard:** Progress tracking and metrics visualization

## 📝 License

This project is provided as a development scaffold. Adjust licensing as needed for your use case.

---

**Note:** This scaffold provides a complete foundation for the OKR Agentic App. Configure the Gemini API credentials and start both servers to begin using the application.#   F r e s h   d e p l o y m e n t   t r i g g e r 
 
 