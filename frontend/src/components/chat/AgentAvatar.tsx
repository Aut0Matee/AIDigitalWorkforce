import React from 'react';
import { Avatar } from '@mui/material';
import {
  Search as SearchIcon,
  Edit as PenToolIcon,
  Science as MicroscopeIcon,
  Person as UserIcon,
  SmartToy as BotIcon
} from '@mui/icons-material';
import type { Message } from '@/types';

interface AgentAvatarProps {
  role: Message['agent_role'];
}

export const AgentAvatar: React.FC<AgentAvatarProps> = ({ role }) => {
  const getAvatarConfig = () => {
    switch (role) {
      case 'researcher':
        return {
          icon: <SearchIcon />,
          bgColor: '#2196f3',
          label: 'Researcher',
        };
      case 'writer':
        return {
          icon: <PenToolIcon />,
          bgColor: '#4caf50',
          label: 'Writer',
        };
      case 'analyst':
        return {
          icon: <MicroscopeIcon />,
          bgColor: '#9c27b0',
          label: 'Analyst',
        };
      case 'human':
        return {
          icon: <UserIcon />,
          bgColor: '#757575',
          label: 'You',
        };
      case 'system':
        return {
          icon: <BotIcon />,
          bgColor: '#ff9800',
          label: 'System',
        };
      default:
        return {
          icon: <BotIcon />,
          bgColor: '#9e9e9e',
          label: 'Unknown',
        };
    }
  };

  const config = getAvatarConfig();

  return (
    <Avatar
      sx={{
        bgcolor: config.bgColor,
        width: 40,
        height: 40,
      }}
      aria-label={config.label}
    >
      {config.icon}
    </Avatar>
  );
};