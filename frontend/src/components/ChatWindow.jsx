import { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import ChatBubble from './ChatBubble';
import { api } from '../utils/api';

const ChatWindow = ({ agentId, agent }) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [streamingMessage, setStreamingMessage] = useState('');
  const messagesEndRef = useRef(null);
  const chatContainerRef = useRef(null);

  useEffect(() => {
    if (agentId) {
      loadChatHistory();
    }
  }, [agentId]);

  useEffect(() => {
    scrollToBottom();
  }, [messages, streamingMessage]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const loadChatHistory = async () => {
    try {
      const history = await api.getChatHistory(agentId);
      setMessages(history);
    } catch (error) {
      console.error('Failed to load chat history:', error);
    }
  };

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = input.trim();
    setInput('');
    setIsLoading(true);
    setStreamingMessage('');

    // Add user message immediately
    const newUserMessage = { role: 'user', content: userMessage };
    setMessages((prev) => [...prev, newUserMessage]);

    try {
      const response = await api.sendMessage(agentId, userMessage, true);

      if (!response.body) {
        throw new Error('No response body');
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let fullResponse = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split('\n');

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6));
              if (data.content) {
                fullResponse += data.content;
                setStreamingMessage(fullResponse);
              }
              if (data.done) {
                setMessages((prev) => [...prev, { role: 'assistant', content: fullResponse }]);
                setStreamingMessage('');
                setIsLoading(false);
              }
            } catch (e) {
              // Ignore JSON parse errors
            }
          }
        }
      }
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: 'Sorry, I encountered an error. Please try again.' },
      ]);
      setIsLoading(false);
      setStreamingMessage('');
    }
  };

  const handleExport = async (format = 'txt') => {
    try {
      const allMessages = [...messages];
      if (streamingMessage) {
        allMessages.push({ role: 'assistant', content: streamingMessage });
      }

      let content = '';
      let filename = '';

      if (format === 'json') {
        content = JSON.stringify(
          {
            agent: agent?.name || 'Unknown',
            timestamp: new Date().toISOString(),
            messages: allMessages,
          },
          null,
          2
        );
        filename = `chat-${agent?.name || 'export'}-${Date.now()}.json`;
      } else {
        content = allMessages
          .map((msg) => {
            const role = msg.role === 'user' ? 'You' : agent?.name || 'Assistant';
            return `[${role}]: ${msg.content}`;
          })
          .join('\n\n');
        filename = `chat-${agent?.name || 'export'}-${Date.now()}.txt`;
      }

      const blob = new Blob([content], { type: format === 'json' ? 'application/json' : 'text/plain' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Error exporting chat:', error);
      alert('Failed to export chat');
    }
  };

  if (!agent) {
    return (
      <div className="flex items-center justify-center h-full text-gray-500 dark:text-gray-400">
        <p>Select an agent to start chatting</p>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="border-b border-gray-200 dark:border-gray-700 px-6 py-4 bg-white dark:bg-gray-800">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xl font-semibold">{agent.name}</h2>
            <p className="text-sm text-gray-500 dark:text-gray-400">{agent.role}</p>
          </div>
          <div className="flex gap-2">
            <button
              onClick={() => handleExport('txt')}
              className="px-3 py-2 text-sm bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 rounded-lg transition-colors"
            >
              Export TXT
            </button>
            <button
              onClick={() => handleExport('json')}
              className="px-3 py-2 text-sm bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 rounded-lg transition-colors"
            >
              Export JSON
            </button>
          </div>
        </div>
      </div>

      {/* Messages */}
      <div
        ref={chatContainerRef}
        className="flex-1 overflow-y-auto px-6 py-4 bg-gray-50 dark:bg-gray-900"
      >
        <AnimatePresence>
          {messages.map((msg, index) => (
            <ChatBubble
              key={index}
              message={msg.content}
              role={msg.role}
              timestamp={msg.timestamp}
            />
          ))}
          {streamingMessage && (
            <ChatBubble message={streamingMessage} role="assistant" />
          )}
        </AnimatePresence>
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="border-t border-gray-200 dark:border-gray-700 px-6 py-4 bg-white dark:bg-gray-800">
        <form onSubmit={handleSend} className="flex gap-3">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message..."
            className="flex-1 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-primary-500"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={isLoading || !input.trim()}
            className="px-6 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {isLoading ? 'Sending...' : 'Send'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default ChatWindow;







