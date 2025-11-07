import React from "react";

export default function Step2({krs, onSelect}) {
  return (
    <div className="bg-white rounded-lg shadow-lg p-8 max-w-4xl mx-auto">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-gray-800 mb-2">🎯 Choose Your Key Result</h2>
        <p className="text-gray-600">Select the Key Result that best aligns with your objective</p>
      </div>
      
      <div className="grid gap-6 md:grid-cols-1 lg:grid-cols-2">
        {krs.map((kr, index)=>(
          <div key={kr.id} className="group bg-gradient-to-br from-gray-50 to-gray-100 border-2 border-gray-200 hover:border-blue-300 rounded-xl p-6 transition-all duration-200 hover:shadow-lg cursor-pointer"
               onClick={()=>onSelect(kr.id)}>
            <div className="flex items-start justify-between mb-4">
              <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center text-blue-600 font-bold">
                {index + 1}
              </div>
              <div className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-xs font-medium">
                📊 {kr.metric}
              </div>
            </div>
            
            <h3 className="font-bold text-lg text-gray-800 mb-3 group-hover:text-blue-600 transition-colors">
              {kr.text}
            </h3>
            
            <div className="space-y-2 mb-4">
              <div className="flex justify-between items-center bg-white rounded p-2 text-sm">
                <span className="text-gray-600">Baseline:</span>
                <span className="font-medium text-red-600">{kr.baseline}</span>
              </div>
              <div className="flex justify-between items-center bg-white rounded p-2 text-sm">
                <span className="text-gray-600">Target:</span>
                <span className="font-medium text-green-600">{kr.target}</span>
              </div>
            </div>
            
            <div className="bg-blue-50 rounded-lg p-3 mb-4">
              <div className="text-sm text-blue-700">
                <strong>💡 Rationale:</strong> {kr.rationale}
              </div>
            </div>
            
            <button className="w-full bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 text-white font-semibold px-4 py-2 rounded-lg transition-all duration-200 transform group-hover:scale-105">
              ✅ Select This KR
            </button>
          </div>
        ))}
      </div>
      
      <div className="mt-8 text-center">
        <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 rounded inline-block">
          <div className="text-sm text-yellow-700">
            <strong>🎯 Next Step:</strong> After selecting a Key Result, we'll generate Epic and Feature breakdowns to achieve your goal.
          </div>
        </div>
      </div>
    </div>
  );
}