import React, { useState, useEffect } from "react";
import * as api from "../api";

export default function JiraIntegrationModal({ isOpen, onClose, sessionId, onSuccess }) {
  const [step, setStep] = useState(1); // 1: Setup, 2: Testing, 3: Uploading, 4: Success
  const [loading, setLoading] = useState(false);
  const [jiraConfig, setJiraConfig] = useState({
    base_url: '',
    email: '',
    api_token: '',
    project_key: ''
  });
  const [testResult, setTestResult] = useState(null);
  const [uploadResult, setUploadResult] = useState(null);
  const [error, setError] = useState('');

  // Load default config when modal opens
  useEffect(() => {
    if (isOpen) {
      loadDefaultConfig();
    }
  }, [isOpen]);

  const loadDefaultConfig = async () => {
    try {
      const defaultConfig = await api.getJiraConfig();
      setJiraConfig(prev => ({
        ...prev,
        base_url: defaultConfig.base_url || '',
        email: defaultConfig.email || '',
        project_key: defaultConfig.project_key || '',
        api_token: defaultConfig.api_token || '', // Pre-fill for convenience
      }));
    } catch (err) {
      console.log('No default config available');
    }
  };

  if (!isOpen) return null;

  const handleInputChange = (field, value) => {
    setJiraConfig(prev => ({ ...prev, [field]: value }));
    setError('');
  };

  const testConnection = async () => {
    setLoading(true);
    setError('');
    try {
      const result = await api.testJiraConnection(jiraConfig);
      setTestResult(result);
      if (result.success) {
        setStep(2);
      } else {
        setError(result.error || 'Connection test failed');
      }
    } catch (err) {
      setError('Failed to connect to Jira. Please check your credentials.');
    } finally {
      setLoading(false);
    }
  };

  const uploadToJira = async () => {
    console.log('🚀 Starting Jira upload with sessionId:', sessionId);
    console.log('📋 Jira config:', jiraConfig);
    
    if (!sessionId) {
      setError('No session ID available. Please complete the workflow first.');
      return;
    }
    
    setLoading(true);
    setError('');
    setStep(3);
    try {
      const result = await api.uploadToJira(sessionId, jiraConfig);
      setUploadResult(result);
      if (result.success) {
        setStep(4);
        setTimeout(() => {
          onSuccess(result);
          onClose();
        }, 3000);
      } else {
        setError(result.errors?.join(', ') || 'Upload failed');
        setStep(2);
      }
    } catch (err) {
      setError('Failed to upload to Jira. Please try again.');
      setStep(2);
    } finally {
      setLoading(false);
    }
  };

  const resetModal = () => {
    setStep(1);
    setTestResult(null);
    setUploadResult(null);
    setError('');
    setJiraConfig({
      base_url: '',
      email: '',
      api_token: '',
      project_key: ''
    });
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white p-6 rounded-t-lg">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <div className="w-10 h-10 bg-white bg-opacity-20 rounded-full flex items-center justify-center mr-3">
                🎯
              </div>
              <div>
                <h2 className="text-2xl font-bold">Upload to Jira</h2>
                <p className="text-blue-100">Direct integration with your Jira project</p>
              </div>
            </div>
            <button
              onClick={() => { onClose(); resetModal(); }}
              className="text-white hover:text-gray-300 text-2xl font-bold"
            >
              ×
            </button>
          </div>
        </div>

        <div className="p-6">
          {/* Step 1: Configuration */}
          {step === 1 && (
            <div className="space-y-6">
              <div className="bg-blue-50 border-l-4 border-blue-400 p-4 rounded">
                <h3 className="font-semibold text-blue-800 mb-2">🔧 Jira Configuration</h3>
                <p className="text-sm text-blue-700">
                  Enter your Jira Cloud credentials to upload your OKR structure directly to your project.
                </p>
              </div>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Jira Site URL
                  </label>
                  <input
                    type="url"
                    placeholder="https://yourcompany.atlassian.net"
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    value={jiraConfig.base_url}
                    onChange={(e) => handleInputChange('base_url', e.target.value)}
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Email Address
                  </label>
                  <input
                    type="email"
                    placeholder="your.email@company.com"
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    value={jiraConfig.email}
                    onChange={(e) => handleInputChange('email', e.target.value)}
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    API Token
                  </label>
                  <input
                    type="password"
                    placeholder="Your Jira API token"
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    value={jiraConfig.api_token}
                    onChange={(e) => handleInputChange('api_token', e.target.value)}
                  />
                  <p className="text-xs text-gray-500 mt-1">
                    Create at: <a href="https://id.atlassian.com/manage-profile/security/api-tokens" target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">Atlassian API Tokens</a>
                  </p>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Project Key
                  </label>
                  <input
                    type="text"
                    placeholder="PROJ (uppercase)"
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    value={jiraConfig.project_key}
                    onChange={(e) => handleInputChange('project_key', e.target.value.toUpperCase())}
                  />
                </div>
              </div>

              {error && (
                <div className="bg-red-50 border-l-4 border-red-400 p-4 rounded">
                  <div className="text-sm text-red-700">{error}</div>
                </div>
              )}

              <div className="flex justify-end space-x-3">
                <button
                  onClick={() => { onClose(); resetModal(); }}
                  className="px-4 py-2 text-gray-600 hover:text-gray-800 font-medium"
                >
                  Cancel
                </button>
                <button
                  onClick={testConnection}
                  disabled={!jiraConfig.base_url || !jiraConfig.email || !jiraConfig.api_token || !jiraConfig.project_key || loading}
                  className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed font-medium"
                >
                  {loading ? 'Testing...' : 'Test Connection'}
                </button>
              </div>
            </div>
          )}

          {/* Step 2: Connection Success */}
          {step === 2 && testResult?.success && (
            <div className="space-y-6">
              <div className="bg-green-50 border-l-4 border-green-400 p-4 rounded">
                <h3 className="font-semibold text-green-800 mb-2">✅ Connection Successful</h3>
                <p className="text-sm text-green-700">
                  Connected as: <strong>{testResult.user}</strong> ({testResult.email})
                </p>
              </div>

              <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 rounded">
                <h4 className="font-semibold text-yellow-800 mb-2">⚠️ Important Notes</h4>
                <ul className="text-sm text-yellow-700 space-y-1">
                  <li>• This will create Epics, Stories, and Sub-tasks in project <strong>{jiraConfig.project_key}</strong></li>
                  <li>• Make sure you have permission to create issues in this project</li>
                  <li>• The upload process may take a few minutes depending on project size</li>
                  <li>• Created issues will follow your Jira project's workflow</li>
                </ul>
              </div>

              {uploadResult && !uploadResult.success && (
                <div className="bg-red-50 border-l-4 border-red-400 p-4 rounded">
                  <div className="text-sm text-red-700">
                    <strong>Upload Failed:</strong> {uploadResult.errors?.join(', ') || 'Unknown error'}
                  </div>
                </div>
              )}

              <div className="flex justify-end space-x-3">
                <button
                  onClick={() => setStep(1)}
                  className="px-4 py-2 text-gray-600 hover:text-gray-800 font-medium"
                >
                  Back
                </button>
                <button
                  onClick={uploadToJira}
                  disabled={loading}
                  className="bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed font-medium"
                >
                  {loading ? 'Uploading...' : '🚀 Upload to Jira'}
                </button>
              </div>
            </div>
          )}

          {/* Step 3: Uploading */}
          {step === 3 && (
            <div className="text-center py-8">
              <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto mb-4"></div>
              <h3 className="text-lg font-semibold text-gray-800 mb-2">Uploading to Jira...</h3>
              <p className="text-gray-600">Creating your project structure. Please wait...</p>
            </div>
          )}

          {/* Step 4: Success */}
          {step === 4 && uploadResult?.success && (
            <div className="text-center py-8">
              <div className="text-6xl mb-4">🎉</div>
              <h3 className="text-2xl font-bold text-green-600 mb-4">Upload Successful!</h3>
              
              <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-6">
                <h4 className="font-semibold text-green-800 mb-2">Created Issues:</h4>
                <div className="grid grid-cols-3 gap-4 text-sm">
                  <div>
                    <div className="text-2xl font-bold text-purple-600">{uploadResult.summary?.epics || 0}</div>
                    <div className="text-gray-600">Epics</div>
                  </div>
                  <div>
                    <div className="text-2xl font-bold text-blue-600">{uploadResult.summary?.stories || 0}</div>
                    <div className="text-gray-600">Stories</div>
                  </div>
                  <div>
                    <div className="text-2xl font-bold text-orange-600">{uploadResult.summary?.subtasks || 0}</div>
                    <div className="text-gray-600">Sub-tasks</div>
                  </div>
                </div>
              </div>

              <p className="text-gray-600 mb-4">
                Your OKR structure has been successfully uploaded to Jira project <strong>{jiraConfig.project_key}</strong>.
              </p>
              
              <button
                onClick={() => window.open(`${jiraConfig.base_url}/projects/${jiraConfig.project_key}`, '_blank')}
                className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 font-medium"
              >
                🔗 View in Jira
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}