import React, {useState} from "react";

export default function Step1({onCreate}) {
  const [text, setText] = useState("");
  return (
    <div className="bg-white rounded-lg shadow-lg p-8 max-w-2xl mx-auto">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-gray-800 mb-2">🎯 Define Your Objective</h2>
        <p className="text-gray-600">Start by entering a clear, actionable objective for your project</p>
      </div>
      
      <div className="space-y-4">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Objective Description
        </label>
        <textarea 
          className="w-full border-2 border-gray-200 rounded-lg p-4 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-colors min-h-[120px] resize-none" 
          rows={4} 
          value={text} 
          onChange={e=>setText(e.target.value)}
          placeholder="e.g., Increase user engagement in our mobile app by 25% within Q1 2024..."
        />
        
        <div className="bg-blue-50 border-l-4 border-blue-400 p-4 rounded">
          <div className="text-sm text-blue-700">
            <strong>💡 Tip:</strong> A good objective should be specific, inspiring, and achievable. Think about what success looks like for your project.
          </div>
        </div>
        
        <div className="pt-4">
          <button 
            className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-semibold px-6 py-3 rounded-lg transition-all duration-200 transform hover:scale-105 shadow-lg disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
            onClick={()=>onCreate(text)}
            disabled={!text.trim()}
          >
            🚀 Generate Key Results
          </button>
        </div>
      </div>
    </div>
  );
}