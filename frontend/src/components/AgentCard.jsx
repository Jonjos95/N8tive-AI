import { motion } from 'framer-motion';
import { useState } from 'react';

const AgentCard = ({ agent, isSelected, onSelect, onDelete, onEdit }) => {
  const [isHovered, setIsHovered] = useState(false);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ scale: 1.02 }}
      onHoverStart={() => setIsHovered(true)}
      onHoverEnd={() => setIsHovered(false)}
      onClick={() => onSelect(agent.id)}
      className={`relative p-4 rounded-lg cursor-pointer transition-all ${
        isSelected
          ? 'bg-primary-500 text-white shadow-lg'
          : 'bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 hover:border-primary-300 dark:hover:border-primary-600'
      }`}
    >
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <h3 className="font-semibold text-lg mb-1">{agent.name}</h3>
          <p
            className={`text-sm mb-2 ${
              isSelected
                ? 'text-primary-100'
                : 'text-gray-600 dark:text-gray-400'
            }`}
          >
            {agent.role}
          </p>
          <div className="flex flex-wrap gap-2 mt-2">
            <span
              className={`px-2 py-1 rounded text-xs ${
                isSelected
                  ? 'bg-primary-400 text-white'
                  : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300'
              }`}
            >
              {agent.model}
            </span>
            <span
              className={`px-2 py-1 rounded text-xs ${
                isSelected
                  ? 'bg-primary-400 text-white'
                  : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300'
              }`}
            >
              {agent.tone}
            </span>
          </div>
        </div>
      </div>

      {isHovered && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="absolute top-2 right-2 flex gap-2"
          onClick={(e) => e.stopPropagation()}
        >
          <button
            onClick={(e) => {
              e.stopPropagation();
              onEdit(agent);
            }}
            className="p-1.5 bg-white dark:bg-gray-700 rounded hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors"
            title="Edit"
          >
            <svg
              className="w-4 h-4 text-gray-700 dark:text-gray-300"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
              />
            </svg>
          </button>
          <button
            onClick={(e) => {
              e.stopPropagation();
              if (confirm('Are you sure you want to delete this agent?')) {
                onDelete(agent.id);
              }
            }}
            className="p-1.5 bg-red-500 text-white rounded hover:bg-red-600 transition-colors"
            title="Delete"
          >
            <svg
              className="w-4 h-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
              />
            </svg>
          </button>
        </motion.div>
      )}
    </motion.div>
  );
};

export default AgentCard;







