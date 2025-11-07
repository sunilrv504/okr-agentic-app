import React, { useState } from "react";
import JiraIntegrationModal from "./JiraIntegrationModal";

export default function ReviewExport({onExport, structure, sessionId}) {
  const [showJson, setShowJson] = useState(false);
  const [showJiraModal, setShowJiraModal] = useState(false);
  
  const getProjectStats = () => {
    if (!structure) return { epics: 0, features: 0, stories: 0, tasks: 0, hours: 0 };
    
    let epics = (structure.epics || []).length;
    let features = 0;
    let stories = 0;
    let tasks = 0;
    let hours = 0;
    
    (structure.epics || []).forEach(epic => {
      features += (epic.features || []).length;
      (epic.features || []).forEach(feature => {
        stories += (feature.stories || []).length;
        (feature.stories || []).forEach(story => {
          tasks += (story.tasks || []).length;
          (story.tasks || []).forEach(task => {
            hours += task.hours || 0;
          });
        });
      });
    });
    
    return { epics, features, stories, tasks, hours };
  };

  const stats = getProjectStats();

  return (
    <div className="bg-white rounded-lg shadow-lg p-8 max-w-4xl mx-auto">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-gray-800 mb-2">📋 Project Review & Export</h2>
        <p className="text-gray-600">Review your complete OKR breakdown and export for implementation</p>
      </div>
      
      {/* Project Summary */}
      <div className="bg-gradient-to-br from-blue-50 to-indigo-50 border-2 border-blue-200 rounded-xl p-6 mb-8">
        <h3 className="text-xl font-bold text-blue-800 mb-4">📊 Project Summary</h3>
        
        {structure?.objective && (
          <div className="bg-white rounded-lg p-4 mb-4">
            <h4 className="font-semibold text-gray-800 mb-2">🎯 Objective</h4>
            <p className="text-gray-600">{structure.objective.text}</p>
          </div>
        )}
        
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
          <div className="bg-white rounded-lg p-3 text-center">
            <div className="text-2xl font-bold text-purple-600">{stats.epics}</div>
            <div className="text-xs text-gray-600">Epics</div>
          </div>
          <div className="bg-white rounded-lg p-3 text-center">
            <div className="text-2xl font-bold text-indigo-600">{stats.features}</div>
            <div className="text-xs text-gray-600">Features</div>
          </div>
          <div className="bg-white rounded-lg p-3 text-center">
            <div className="text-2xl font-bold text-blue-600">{stats.stories}</div>
            <div className="text-xs text-gray-600">Stories</div>
          </div>
          <div className="bg-white rounded-lg p-3 text-center">
            <div className="text-2xl font-bold text-orange-600">{stats.tasks}</div>
            <div className="text-xs text-gray-600">Tasks</div>
          </div>
          <div className="bg-white rounded-lg p-3 text-center">
            <div className="text-2xl font-bold text-green-600">{stats.hours}h</div>
            <div className="text-xs text-gray-600">Est. Time</div>
          </div>
        </div>
      </div>

      {/* Warnings */}
      {structure?.warnings && structure.warnings.length > 0 && (
        <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 rounded mb-6">
          <h4 className="font-semibold text-yellow-800 mb-2">⚠️ Validation Warnings</h4>
          <ul className="space-y-1">
            {structure.warnings.map((warning, idx) => (
              <li key={idx} className="text-sm text-yellow-700">• {warning}</li>
            ))}
          </ul>
        </div>
      )}

      {/* JSON Preview Toggle */}
      <div className="mb-6">
        <button
          className="flex items-center text-gray-600 hover:text-gray-800 font-medium"
          onClick={() => setShowJson(!showJson)}
        >
          <span className="mr-2">{showJson ? '🔽' : '▶️'}</span>
          {showJson ? 'Hide' : 'Show'} JSON Structure
        </button>
        
        {showJson && (
          <div className="mt-3 bg-gray-900 text-gray-100 rounded-lg overflow-hidden">
            <div className="bg-gray-800 px-4 py-2 text-sm font-medium">
              📄 okr-structure.json
            </div>
            <pre className="p-4 max-h-96 overflow-auto text-xs">
              {JSON.stringify(structure, null, 2)}
            </pre>
          </div>
        )}
      </div>

      {/* Export Actions */}
      <div className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <button 
            className="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-bold px-6 py-4 rounded-lg transition-all duration-200 transform hover:scale-105 shadow-lg text-lg"
            onClick={() => setShowJiraModal(true)}
          >
            🚀 Upload to Jira
          </button>
          
          <button 
            className="bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 text-white font-bold px-6 py-4 rounded-lg transition-all duration-200 transform hover:scale-105 shadow-lg text-lg"
            onClick={onExport}
          >
            📥 Download JSON
          </button>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-gray-100 rounded-lg p-4 text-center">
            <div className="text-2xl mb-2">🎯</div>
            <div className="font-semibold text-gray-800">Jira Import</div>
            <div className="text-xs text-gray-600">Ready for Jira project import</div>
          </div>
          <div className="bg-gray-100 rounded-lg p-4 text-center">
            <div className="text-2xl mb-2">📋</div>
            <div className="font-semibold text-gray-800">Sprint Planning</div>
            <div className="text-xs text-gray-600">Organized by story points</div>
          </div>
          <div className="bg-gray-100 rounded-lg p-4 text-center">
            <div className="text-2xl mb-2">⏱️</div>
            <div className="font-semibold text-gray-800">Time Estimation</div>
            <div className="text-xs text-gray-600">Task-level hour estimates</div>
          </div>
        </div>
      </div>
      
      <div className="mt-8 text-center">
        <div className="bg-green-50 border-l-4 border-green-400 p-4 rounded inline-block">
          <div className="text-sm text-green-700">
            <strong>🎉 Success!</strong> Your OKR breakdown is complete and ready for implementation. The JSON file can be imported into your project management tools.
          </div>
        </div>
      </div>
      
      {/* Jira Integration Modal */}
      <JiraIntegrationModal 
        isOpen={showJiraModal}
        sessionId={sessionId}
        onClose={() => setShowJiraModal(false)}
        onSuccess={() => {
          setShowJiraModal(false);
          // Could add success notification here
        }}
      />
    </div>
  );
}