import React from 'react';
import { Search, PenTool, Microscope, User, Bot } from 'lucide-react';
import { Message } from '../../types';

interface AgentAvatarProps {
  role: Message['agent_role'];
  className?: string;
}

export const AgentAvatar: React.FC<AgentAvatarProps> = ({ role, className = '' }) => {
  const getAvatarConfig = () => {
    switch (role) {
      case 'researcher':
        return {
          icon: Search,
          bgColor: 'bg-blue-500',
          label: 'Researcher',
        };
      case 'writer':
        return {
          icon: PenTool,
          bgColor: 'bg-green-500',
          label: 'Writer',
        };
      case 'analyst':
        return {
          icon: Microscope,
          bgColor: 'bg-purple-500',
          label: 'Analyst',
        };
      case 'human':
        return {
          icon: User,
          bgColor: 'bg-gray-500',
          label: 'You',
        };
      case 'system':
        return {
          icon: Bot,
          bgColor: 'bg-yellow-500',
          label: 'System',
        };
      default:
        return {
          icon: Bot,
          bgColor: 'bg-gray-400',
          label: 'Unknown',
        };
    }
  };

  const config = getAvatarConfig();
  const Icon = config.icon;

  return (
    <div className={`relative ${className}`}>
      <div className={`w-10 h-10 rounded-full ${config.bgColor} flex items-center justify-center`}>
        <Icon className="h-5 w-5 text-white" />
      </div>
      <span className="sr-only">{config.label}</span>
    </div>
  );
};