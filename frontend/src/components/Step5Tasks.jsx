import React from "react";

export default function Step5({epics}) {
  const getTotalHours = () => {
    let total = 0;
    epics.forEach(epic => {
      epic.features.forEach(feature => {
        (feature.stories || []).forEach(story => {
          (story.tasks || []).forEach(task => {
            total += task.hours || 0;
          });
        });
      });
    });
    return total;
  };

  const getTotalTasks = () => {
    let count = 0;
    epics.forEach(epic => {
      epic.features.forEach(feature => {
        (feature.stories || []).forEach(story => {
          count += (story.tasks || []).length;
        });
      });
    });
    return count;
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-8 max-w-6xl mx-auto">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-gray-800 mb-2">⚡ Development Tasks</h2>
        <p className="text-gray-600">Detailed breakdown of actionable development tasks with time estimates</p>
        
        <div className="flex justify-center gap-6 mt-4">
          <div className="bg-blue-100 text-blue-800 px-4 py-2 rounded-lg">
            <div className="font-bold text-lg">{getTotalTasks()}</div>
            <div className="text-sm">Total Tasks</div>
          </div>
          <div className="bg-green-100 text-green-800 px-4 py-2 rounded-lg">
            <div className="font-bold text-lg">{getTotalHours()}h</div>
            <div className="text-sm">Est. Hours</div>
          </div>
        </div>
      </div>
      
      <div className="space-y-8">
        {epics.map((e, epicIndex)=>(
          <div key={e.id} className="bg-gradient-to-br from-purple-50 to-pink-50 border-2 border-purple-200 rounded-xl p-6">
            <div className="flex items-center mb-6">
              <div className="w-10 h-10 bg-purple-500 rounded-full flex items-center justify-center text-white font-bold mr-4">
                {epicIndex + 1}
              </div>
              <h3 className="text-xl font-bold text-purple-800">{e.title}</h3>
            </div>
            
            <div className="space-y-6">
              {e.features.map(f=>(
                <div key={f.id} className="bg-white border-2 border-gray-200 rounded-lg p-5">
                  <div className="flex items-center mb-4">
                    <div className="w-8 h-8 bg-indigo-500 rounded-full flex items-center justify-center text-white font-bold text-sm mr-3">
                      F
                    </div>
                    <h4 className="font-bold text-lg text-gray-800">{f.title}</h4>
                  </div>
                  
                  <div className="space-y-4">
                    {(f.stories||[]).map(s=>(
                      <div key={s.id} className="bg-gradient-to-br from-gray-50 to-blue-50 border border-gray-300 rounded-lg p-4">
                        <div className="flex items-center justify-between mb-3">
                          <h5 className="font-semibold text-gray-800 text-sm">
                            📖 {s.title}
                          </h5>
                          <div className="bg-blue-500 text-white px-2 py-1 rounded text-xs font-medium">
                            {s.story_points} pts
                          </div>
                        </div>
                        
                        {(s.tasks||[]).length > 0 ? (
                          <div className="grid gap-3 md:grid-cols-2 lg:grid-cols-3">
                            {(s.tasks||[]).map((t, taskIndex)=>(
                              <div key={t.id} className="bg-white border border-gray-200 rounded-lg p-3 hover:shadow-md transition-shadow">
                                <div className="flex items-start justify-between mb-2">
                                  <div className="w-6 h-6 bg-orange-100 rounded-full flex items-center justify-center text-orange-600 font-bold text-xs">
                                    {taskIndex + 1}
                                  </div>
                                  <div className="bg-orange-500 text-white px-2 py-1 rounded text-xs font-bold">
                                    {t.hours}h
                                  </div>
                                </div>
                                
                                <div className="text-sm font-medium text-gray-800 leading-relaxed">
                                  {t.title}
                                </div>
                              </div>
                            ))}
                          </div>
                        ) : (
                          <div className="text-center py-4 text-gray-500">
                            <div className="text-2xl mb-1">⚡</div>
                            <p className="text-xs">No tasks generated yet.</p>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
      
      <div className="mt-8 text-center">
        <div className="bg-green-50 border-l-4 border-green-400 p-4 rounded inline-block">
          <div className="text-sm text-green-700">
            <strong>🎉 Great!</strong> Your project breakdown is complete. You can now review and export the full structure.
          </div>
        </div>
      </div>
    </div>
  );
}