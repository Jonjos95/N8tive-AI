import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import AgentCard from './AgentCard';
import SettingsModal from './SettingsModal';
import { api } from '../utils/api';

const Sidebar = ({ selectedAgentId, onSelectAgent }) => {
  const [agents, setAgents] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [editingAgent, setEditingAgent] = useState(null);

  useEffect(() => {
    loadAgents();
  }, []);

  const loadAgents = async () => {
    try {
      setIsLoading(true);
      const agentsList = await api.getAgents();
      setAgents(agentsList);
    } catch (error) {
      console.error('Failed to load agents:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleCreateAgent = async (agentData) => {
    try {
      await api.createAgent(agentData);
      await loadAgents();
      setIsCreateModalOpen(false);
    } catch (error) {
      console.error('Failed to create agent:', error);
      alert('Failed to create agent');
    }
  };

  const handleUpdateAgent = async (agentId, agentData) => {
    try {
      await api.updateAgent(agentId, agentData);
      await loadAgents();
      setEditingAgent(null);
    } catch (error) {
      console.error('Failed to update agent:', error);
      alert('Failed to update agent');
    }
  };

  const handleDeleteAgent = async (agentId) => {
    try {
      await api.deleteAgent(agentId);
      await loadAgents();
      if (selectedAgentId === agentId) {
        onSelectAgent(null);
      }
    } catch (error) {
      console.error('Failed to delete agent:', error);
      alert('Failed to delete agent');
    }
  };

  return (
    <div className="w-80 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 flex flex-col h-full">
      {/* Header */}
      <div className="p-4 border-b border-gray-200 dark:border-gray-700">
        <div className="flex items-center justify-between mb-4">
          <h1 className="text-2xl font-bold">N8tive AI</h1>
        </div>
        <button
          onClick={() => setIsCreateModalOpen(true)}
          className="w-full px-4 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition-colors flex items-center justify-center gap-2"
        >
          <svg
            className="w-5 h-5"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 4v16m8-8H4"
            />
          </svg>
          New Agent
        </button>
      </div>

      {/* Agents List */}
      <div className="flex-1 overflow-y-auto p-4">
        {isLoading ? (
          <div className="text-center text-gray-500 dark:text-gray-400 py-8">
            Loading agents...
          </div>
        ) : agents.length === 0 ? (
          <div className="text-center text-gray-500 dark:text-gray-400 py-8">
            <p className="mb-2">No agents yet</p>
            <p className="text-sm">Create your first agent to get started</p>
          </div>
        ) : (
          <div className="space-y-3">
            {agents.map((agent) => (
              <AgentCard
                key={agent.id}
                agent={agent}
                isSelected={selectedAgentId === agent.id}
                onSelect={onSelectAgent}
                onDelete={handleDeleteAgent}
                onEdit={setEditingAgent}
              />
            ))}
          </div>
        )}
      </div>

      {/* Modals */}
      {isCreateModalOpen && (
        <SettingsModal
          onClose={() => setIsCreateModalOpen(false)}
          onSave={handleCreateAgent}
          title="Create New Agent"
        />
      )}

      {editingAgent && (
        <SettingsModal
          agent={editingAgent}
          onClose={() => setEditingAgent(null)}
          onSave={(data) => handleUpdateAgent(editingAgent.id, data)}
          title="Edit Agent"
        />
      )}
    </div>
  );
};

export default Sidebar;







