import React from "react";

export default function Step3({epics, onGenerateStories}) {
  return (
    <div className="bg-white rounded-lg shadow-lg p-8 max-w-6xl mx-auto">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-gray-800 mb-2">🏗️ Epics & Features</h2>
        <p className="text-gray-600">High-level project structure broken down into manageable features</p>
      </div>
      
      <div className="space-y-8">
        {epics.map((epic, epicIndex)=>(
          <div key={epic.id} className="bg-gradient-to-br from-purple-50 to-indigo-50 border-2 border-purple-200 rounded-xl p-6">
            <div className="flex items-center mb-6">
              <div className="w-12 h-12 bg-purple-500 rounded-full flex items-center justify-center text-white font-bold text-lg mr-4">
                {epicIndex + 1}
              </div>
              <div>
                <h3 className="text-2xl font-bold text-purple-800">{epic.title}</h3>
                <div className="text-purple-600 text-sm">Epic • {epic.features.length} Features</div>
              </div>
            </div>
            
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
              {epic.features.map((f, featureIndex)=>(
                <div key={f.id} className="bg-white border-2 border-gray-200 hover:border-indigo-300 rounded-lg p-5 transition-all duration-200 hover:shadow-md group">
                  <div className="flex items-start justify-between mb-3">
                    <div className="w-8 h-8 bg-indigo-100 rounded-full flex items-center justify-center text-indigo-600 font-bold text-sm">
                      {featureIndex + 1}
                    </div>
                    <div className="bg-indigo-100 text-indigo-800 px-2 py-1 rounded text-xs font-medium">
                      Feature
                    </div>
                  </div>
                  
                  <h4 className="font-bold text-lg text-gray-800 mb-2 group-hover:text-indigo-600 transition-colors">
                    {f.title}
                  </h4>
                  
                  <p className="text-gray-600 text-sm mb-4 line-clamp-3">
                    {f.description}
                  </p>
                  
                  <button 
                    className="w-full bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 text-white font-semibold px-4 py-2 rounded-lg transition-all duration-200 transform hover:scale-105"
                    onClick={()=>onGenerateStories(f.id)}
                  >
                    📝 Generate Stories
                  </button>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
      
      <div className="mt-8 text-center">
        <div className="bg-indigo-50 border-l-4 border-indigo-400 p-4 rounded inline-block">
          <div className="text-sm text-indigo-700">
            <strong>🎯 Next Step:</strong> Click "Generate Stories" on any feature to create detailed user stories with acceptance criteria.
          </div>
        </div>
      </div>
    </div>
  );
}