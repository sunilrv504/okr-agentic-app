import React from "react";

export default function Step4({epics, onGenerateTasks}) {
  return (
    <div className="bg-white rounded-lg shadow-lg p-8 max-w-6xl mx-auto">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-gray-800 mb-2">📖 User Stories</h2>
        <p className="text-gray-600">Detailed user stories with acceptance criteria and story points</p>
      </div>
      
      <div className="space-y-8">
        {epics.map((epic, epicIndex)=>(
          <div key={epic.id} className="bg-gradient-to-br from-green-50 to-emerald-50 border-2 border-green-200 rounded-xl p-6">
            <div className="flex items-center mb-6">
              <div className="w-10 h-10 bg-green-500 rounded-full flex items-center justify-center text-white font-bold mr-4">
                {epicIndex + 1}
              </div>
              <h3 className="text-xl font-bold text-green-800">{epic.title}</h3>
            </div>
            
            <div className="space-y-6">
              {epic.features.map(f=>(
                <div key={f.id} className="bg-white border-2 border-gray-200 rounded-lg p-5">
                  <div className="flex items-center mb-4">
                    <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center text-white font-bold text-sm mr-3">
                      F
                    </div>
                    <h4 className="font-bold text-lg text-gray-800">{f.title}</h4>
                  </div>
                  
                  {(f.stories||[]).length > 0 ? (
                    <div className="grid gap-4 md:grid-cols-1 lg:grid-cols-2">
                      {(f.stories||[]).map((s, storyIndex)=>(
                        <div key={s.id} className="bg-gradient-to-br from-gray-50 to-blue-50 border border-gray-300 rounded-lg p-4 hover:shadow-md transition-shadow">
                          <div className="flex items-start justify-between mb-3">
                            <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center text-blue-600 font-bold text-sm">
                              {storyIndex + 1}
                            </div>
                            <div className="bg-blue-500 text-white px-3 py-1 rounded-full text-xs font-medium">
                              {s.story_points} pts
                            </div>
                          </div>
                          
                          <div className="mb-3">
                            <div className="text-xs text-blue-600 mb-1 font-medium">📖 User Story</div>
                            <h5 className="font-semibold text-gray-800 text-sm leading-relaxed bg-blue-50 p-2 rounded border-l-4 border-blue-400">
                              {s.title}
                            </h5>
                          </div>
                          
                          {s.acceptance_criteria && s.acceptance_criteria.length > 0 && (
                            <div className="mb-4">
                              <div className="text-xs font-semibold text-gray-600 mb-2">✅ Acceptance Criteria:</div>
                              <ul className="space-y-2">
                                {s.acceptance_criteria.map((criteria, idx) => (
                                  <li key={idx} className="text-xs text-gray-600 bg-white rounded p-2 border-l-2 border-green-400">
                                    <div className="font-mono">{criteria}</div>
                                  </li>
                                ))}
                              </ul>
                            </div>
                          )}
                          
                          <button 
                            className="w-full bg-gradient-to-r from-yellow-500 to-orange-500 hover:from-yellow-600 hover:to-orange-600 text-white font-semibold px-3 py-2 rounded-lg text-sm transition-all duration-200 transform hover:scale-105"
                            onClick={()=>onGenerateTasks(s.id)}
                          >
                            ⚡ Decompose to Tasks
                          </button>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="text-center py-8 text-gray-500">
                      <div className="text-4xl mb-2">📝</div>
                      <p>No stories generated yet for this feature.</p>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
      
      <div className="mt-8 space-y-4">
        <div className="text-center">
          <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 rounded inline-block">
            <div className="text-sm text-yellow-700">
              <strong>⚡ Next Step:</strong> Click "Decompose to Tasks" on any story to break it down into actionable development tasks.
            </div>
          </div>
        </div>
        
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 max-w-2xl mx-auto">
          <h4 className="font-semibold text-blue-800 mb-2">📋 User Story Format Guide</h4>
          <div className="text-sm text-blue-700 space-y-2">
            <div>
              <strong>Story Format:</strong> "As a [Role], I want [Goal] so that [Benefit]"
            </div>
            <div>
              <strong>Acceptance Criteria:</strong> "GIVEN [context], WHEN [action], THEN [outcome]"
            </div>
            <div>
              <strong>Story Points:</strong> Fibonacci sequence (1, 2, 3, 5, 8, 13) for complexity estimation
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}