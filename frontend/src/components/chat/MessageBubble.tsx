import React from 'react';
import { Message } from '../../types';
import { AgentAvatar } from './AgentAvatar';
import { formatDistanceToNow } from '../../utils/date';

interface MessageBubbleProps {
  message: Message;
}

export const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
  const getRoleName = () => {
    switch (message.agent_role) {
      case 'researcher':
        return 'Research Agent';
      case 'writer':
        return 'Content Writer';
      case 'analyst':
        return 'Quality Analyst';
      case 'human':
        return 'You';
      case 'system':
        return 'System';
      default:
        return 'Unknown';
    }
  };

  const getBubbleClass = () => {
    const baseClass = 'rounded-lg p-4 max-w-3xl';
    const roleClass = `message-bubble-${message.agent_role}`;
    return `${baseClass} ${roleClass}`;
  };

  return (
    <div className="flex space-x-3">
      <AgentAvatar role={message.agent_role} className="flex-shrink-0" />
      
      <div className="flex-1 space-y-1">
        <div className="flex items-center space-x-2">
          <span className="text-sm font-semibold text-gray-900">{getRoleName()}</span>
          <span className="text-xs text-gray-500">
            {formatDistanceToNow(message.created_at)}
          </span>
        </div>
        
        <div className={getBubbleClass()}>
          <div className="prose prose-sm max-w-none">
            {message.content.split('\n').map((line, index) => (
              <React.Fragment key={index}>
                {line}
                {index < message.content.split('\n').length - 1 && <br />}
              </React.Fragment>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};