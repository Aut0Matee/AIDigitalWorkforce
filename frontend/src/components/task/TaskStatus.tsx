import React from 'react';
import { Chip } from '@mui/material';
import {
  CheckCircle as CheckCircleIcon,
  RadioButtonUnchecked as CircleIcon,
  Error as AlertCircleIcon,
  Schedule as ClockIcon
} from '@mui/icons-material';
import type { Task } from '@/types';

interface TaskStatusProps {
  status: Task['status'];
  size?: 'small' | 'medium';
}

export const TaskStatus: React.FC<TaskStatusProps> = ({ status, size = 'small' }) => {
  const getStatusConfig = () => {
    switch (status) {
      case 'created':
        return {
          icon: <CircleIcon />,
          label: 'Created',
          color: 'default' as const,
        };
      case 'in_progress':
        return {
          icon: <ClockIcon />,
          label: 'In Progress',
          color: 'primary' as const,
        };
      case 'completed':
        return {
          icon: <CheckCircleIcon />,
          label: 'Completed',
          color: 'success' as const,
        };
      case 'failed':
        return {
          icon: <AlertCircleIcon />,
          label: 'Failed',
          color: 'error' as const,
        };
      default:
        return {
          icon: <CircleIcon />,
          label: 'Unknown',
          color: 'default' as const,
        };
    }
  };

  const config = getStatusConfig();

  return (
    <Chip
      icon={config.icon}
      label={config.label}
      color={config.color}
      size={size}
      variant="outlined"
    />
  );
};