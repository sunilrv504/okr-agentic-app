import React, { useState, useEffect } from 'react';

export default function ApiKeyModal({ isOpen, onClose, onSave }) {
  const [apiKey, setApiKey] = useState('');
  const [showKey, setShowKey] = useState(false);

  // Load saved API key from localStorage
  useEffect(() => {
    if (isOpen) {
      const savedKey = localStorage.getItem('gemini_api_key') || '';
      setApiKey(savedKey);
    }
  }, [isOpen]);

  const handleSave = () => {
    // Save to localStorage
    localStorage.setItem('gemini_api_key', apiKey);
    onSave(apiKey);
    onClose();
  };

  const handleClear = () => {
    localStorage.removeItem('gemini_api_key');
    setApiKey('');
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-md w-full">
        {/* Header */}
        <div className="bg-gradient-to-r from-purple-600 to-blue-600 text-white p-6 rounded-t-lg">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <div className="w-10 h-10 bg-white bg-opacity-20 rounded-full flex items-center justify-center mr-3">
                🔑
              </div>
              <div>
                <h2 className="text-xl font-bold">API Configuration</h2>
                <p className="text-purple-100">Configure your AI API key</p>
              </div>
            </div>
            <button
              onClick={onClose}
              className="text-white hover:text-gray-300 text-2xl font-bold"
            >
              ×
            </button>
          </div>
        </div>

        <div className="p-6 space-y-4">
          {/* Info Box */}
          <div className="bg-blue-50 border-l-4 border-blue-400 p-4 rounded">
            <h3 className="font-semibold text-blue-800 mb-2">🤖 Google Gemini API Key</h3>
            <p className="text-sm text-blue-700 mb-2">
              To use AI-powered suggestions, you need a Google Gemini API key.
            </p>
            <div className="text-xs text-blue-600">
              <p>1. Visit: <a href="https://ai.google.dev/" target="_blank" rel="noopener noreferrer" className="underline">Google AI Studio</a></p>
              <p>2. Create an API key</p>
              <p>3. Paste it below (stored locally in your browser)</p>
            </div>
          </div>

          {/* API Key Input */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Gemini API Key
            </label>
            <div className="relative">
              <input
                type={showKey ? 'text' : 'password'}
                placeholder="Enter your Google Gemini API key"
                className="w-full border border-gray-300 rounded-lg px-3 py-2 pr-20 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
              />
              <button
                type="button"
                onClick={() => setShowKey(!showKey)}
                className="absolute right-2 top-2 text-gray-500 hover:text-gray-700 text-sm"
              >
                {showKey ? '🙈' : '👁️'}
              </button>
            </div>
            {apiKey && (
              <p className="text-xs text-green-600 mt-1">
                ✅ API key configured ({apiKey.length} characters)
              </p>
            )}
          </div>

          {/* Fallback Notice */}
          <div className="bg-yellow-50 border-l-4 border-yellow-400 p-3 rounded">
            <p className="text-sm text-yellow-700">
              <strong>Note:</strong> Without an API key, the app will use demo responses. 
              For real AI-generated content, please provide your API key.
            </p>
          </div>

          {/* Action Buttons */}
          <div className="flex justify-between space-x-3 pt-4">
            <button
              onClick={handleClear}
              className="text-gray-600 hover:text-gray-800 font-medium"
              disabled={!apiKey}
            >
              Clear Key
            </button>
            <div className="space-x-3">
              <button
                onClick={onClose}
                className="px-4 py-2 text-gray-600 hover:text-gray-800 font-medium"
              >
                Cancel
              </button>
              <button
                onClick={handleSave}
                className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 font-medium"
              >
                Save & Continue
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}