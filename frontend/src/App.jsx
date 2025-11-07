import React, {useState, useEffect} from "react";
import Step1 from "./components/Step1Objective";
import Step2 from "./components/Step2KRs";
import Step3 from "./components/Step3Epics";
import Step4 from "./components/Step4Stories";
import Step5 from "./components/Step5Tasks";
import ReviewExport from "./components/ReviewExport";
import ApiKeyModal from "./components/ApiKeyModal";
import * as api from "./api";

export default function App(){
  const [step, setStep] = useState(1);
  const [session, setSession] = useState(null);
  const [krs, setKrs] = useState([]);
  const [epics, setEpics] = useState([]);
  const [structure, setStructure] = useState(null);
  const [loading, setLoading] = useState(false);
  const [apiKeyModalOpen, setApiKeyModalOpen] = useState(false);
  const [geminiApiKey, setGeminiApiKey] = useState('');

  const stepTitles = [
    "", "Define Objective", "Select Key Result", "Plan Epics", "Create Stories", "Generate Tasks", "Review & Export"
  ];

  // Load API key from localStorage on startup
  useEffect(() => {
    const savedKey = localStorage.getItem('gemini_api_key') || '';
    setGeminiApiKey(savedKey);
  }, []);

  async function createSession(text){
    setLoading(true);
    try {
      const res = await api.createSession(text);
      setSession(res.session_id);
      const k = await api.suggestKRs(text, geminiApiKey);
      setKrs(k.krs || []);
      setStep(2);
    } catch (error) {
      console.error('Error creating session:', error);
    } finally {
      setLoading(false);
    }
  }

  async function selectKR(selected_kr){
    setLoading(true);
    try {
      const e = await api.generateEpics(session, selected_kr, geminiApiKey);
      setEpics(e.epics || []);
      setStep(3);
    } catch (error) {
      console.error('Error generating epics:', error);
    } finally {
      setLoading(false);
    }
  }

  async function generateStories(selected_feature){
    setLoading(true);
    try {
      await api.generateStories(session, selected_feature, geminiApiKey);
      const s = await api.exportJSON(session);
      setEpics(s.epics || []);
      setStructure(s);
      setStep(4);
    } catch (error) {
      console.error('Error generating stories:', error);
    } finally {
      setLoading(false);
    }
  }

  async function generateTasks(selected_story){
    setLoading(true);
    try {
      await api.generateTasks(session, selected_story, geminiApiKey);
      const s = await api.exportJSON(session);
      setEpics(s.epics || []);
      setStructure(s);
      setStep(5);
    } catch (error) {
      console.error('Error generating tasks:', error);
    } finally {
      setLoading(false);
    }
  }

  async function exportJSON(){
    try {
      const s = await api.exportJSON(session);
      const blob = new Blob([JSON.stringify(s, null, 2)], {type:"application/json"});
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url; a.download = "okr-structure.json"; a.click();
    } catch (error) {
      console.error('Error exporting JSON:', error);
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      {/* Header */}
      <div className="bg-white shadow-lg border-b border-gray-200">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <div className="w-10 h-10 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center text-white font-bold text-lg mr-4">
                O
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-800">OKR Agentic Planner</h1>
                <p className="text-sm text-gray-600">AI-powered project breakdown & planning</p>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              {/* API Key Status */}
              <button
                onClick={() => setApiKeyModalOpen(true)}
                className={`flex items-center space-x-2 px-3 py-2 rounded-lg text-sm font-medium transition-all ${
                  geminiApiKey 
                    ? 'bg-green-100 text-green-700 hover:bg-green-200' 
                    : 'bg-yellow-100 text-yellow-700 hover:bg-yellow-200'
                }`}
              >
                <span>{geminiApiKey ? '🔑' : '⚠️'}</span>
                <span>{geminiApiKey ? 'API Configured' : 'Configure API'}</span>
              </button>

              {session && (
                <div className="text-right">
                  <div className="text-sm text-gray-500">Session ID</div>
                  <div className="text-xs font-mono text-gray-400">{session.substring(0, 8)}...</div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Progress Bar */}
      {step > 1 && (
        <div className="bg-white border-b border-gray-200">
          <div className="max-w-6xl mx-auto px-6 py-4">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-gray-700">Progress</span>
              <span className="text-sm font-medium text-gray-700">Step {step} of 6</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div 
                className="bg-gradient-to-r from-blue-600 to-purple-600 h-2 rounded-full transition-all duration-500"
                style={{ width: `${(step / 6) * 100}%` }}
              ></div>
            </div>
            <div className="mt-2 text-center">
              <span className="text-sm text-gray-600">{stepTitles[step]}</span>
            </div>
          </div>
        </div>
      )}

      {/* Loading Overlay */}
      {loading && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-8 text-center">
            <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <div className="text-lg font-semibold text-gray-800">Processing...</div>
            <div className="text-sm text-gray-600">AI agents are working on your request</div>
          </div>
        </div>
      )}

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-6 py-8">
        {step===1 && <Step1 onCreate={createSession} />}
        {step===2 && <Step2 krs={krs} onSelect={selectKR} />}
        {step===3 && <Step3 epics={epics} onGenerateStories={generateStories} />}
        {step===4 && <Step4 epics={epics} onGenerateTasks={generateTasks} />}
        {step===5 && <Step5 epics={epics} />}
        {step===6 && <ReviewExport onExport={exportJSON} structure={structure} sessionId={session} />}
      </div>

      {/* Navigation Footer */}
      {step > 1 && (
        <div className="bg-white border-t border-gray-200 shadow-lg">
          <div className="max-w-6xl mx-auto px-6 py-4">
            <div className="flex justify-between items-center">
              <button 
                className="flex items-center px-4 py-2 text-gray-600 hover:text-gray-800 font-medium transition-colors"
                onClick={()=>setStep(Math.max(1, step-1))}
                disabled={loading}
              >
                <span className="mr-2">←</span>
                Back
              </button>
              
              <div className="flex space-x-2">
                {[2,3,4,5,6].map(s => (
                  <div 
                    key={s}
                    className={`w-3 h-3 rounded-full transition-colors ${
                      s === step ? 'bg-blue-600' : s < step ? 'bg-green-500' : 'bg-gray-300'
                    }`}
                  />
                ))}
              </div>
              
              {step < 6 && (
                <button 
                  className="flex items-center px-4 py-2 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                  onClick={async ()=>{
                    const s = await api.exportJSON(session);
                    setStructure(s);
                    setStep(6);
                  }}
                  disabled={loading}
                >
                  Review
                  <span className="ml-2">→</span>
                </button>
              )}
            </div>
          </div>
        </div>
      )}

      {/* API Key Configuration Modal */}
      <ApiKeyModal 
        isOpen={apiKeyModalOpen}
        onClose={() => setApiKeyModalOpen(false)}
        onSave={(key) => setGeminiApiKey(key)}
      />
    </div>
  );
}