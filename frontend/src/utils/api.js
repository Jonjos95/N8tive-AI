/**
 * API utility for backend communication
 */

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const api = {
  // Chat endpoints
  async sendMessage(agentId, message, stream = true) {
    if (stream) {
      const response = await fetch(`${API_URL}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ agent_id: agentId, message, stream: true }),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return response;
    } else {
      const response = await fetch(`${API_URL}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ agent_id: agentId, message, stream: false }),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return response.json();
    }
  },

  // Agent endpoints
  async getAgents() {
    const response = await fetch(`${API_URL}/api/agents`);
    if (!response.ok) throw new Error('Failed to fetch agents');
    const data = await response.json();
    return data.agents;
  },

  async getAgent(agentId) {
    const response = await fetch(`${API_URL}/api/agents/${agentId}`);
    if (!response.ok) throw new Error('Failed to fetch agent');
    return response.json();
  },

  async createAgent(agentData) {
    const response = await fetch(`${API_URL}/api/agents`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(agentData),
    });
    if (!response.ok) throw new Error('Failed to create agent');
    return response.json();
  },

  async updateAgent(agentId, agentData) {
    const response = await fetch(`${API_URL}/api/agents/${agentId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(agentData),
    });
    if (!response.ok) throw new Error('Failed to update agent');
    return response.json();
  },

  async deleteAgent(agentId) {
    const response = await fetch(`${API_URL}/api/agents/${agentId}`, {
      method: 'DELETE',
    });
    if (!response.ok) throw new Error('Failed to delete agent');
    return response.json();
  },

  async getChatHistory(agentId) {
    const response = await fetch(`${API_URL}/api/agents/${agentId}/history`);
    if (!response.ok) throw new Error('Failed to fetch chat history');
    const data = await response.json();
    return data.history;
  },

  async clearChatHistory(agentId) {
    const response = await fetch(`${API_URL}/api/agents/${agentId}/history`, {
      method: 'DELETE',
    });
    if (!response.ok) throw new Error('Failed to clear chat history');
    return response.json();
  },

  // Config endpoint
  async getConfig() {
    const response = await fetch(`${API_URL}/api/config`);
    if (!response.ok) throw new Error('Failed to fetch config');
    return response.json();
  },
};







