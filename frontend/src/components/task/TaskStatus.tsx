import React from 'react';
import { CheckCircle, Circle, AlertCircle, Clock } from 'lucide-react';
import type { Task } from '../../types';

interface TaskStatusProps {
  status: Task['status'];
  className?: string;
}

export const TaskStatus: React.FC<TaskStatusProps> = ({ status, className = '' }) => {
  const getStatusConfig = () => {
    switch (status) {
      case 'created':
        return {
          icon: Circle,
          text: 'Created',
          colorClass: 'text-gray-500',
          bgClass: 'bg-gray-100',
        };
      case 'in_progress':
        return {
          icon: Clock,
          text: 'In Progress',
          colorClass: 'text-blue-600',
          bgClass: 'bg-blue-100',
        };
      case 'completed':
        return {
          icon: CheckCircle,
          text: 'Completed',
          colorClass: 'text-green-600',
          bgClass: 'bg-green-100',
        };
      case 'failed':
        return {
          icon: AlertCircle,
          text: 'Failed',
          colorClass: 'text-red-600',
          bgClass: 'bg-red-100',
        };
      default:
        return {
          icon: Circle,
          text: 'Unknown',
          colorClass: 'text-gray-500',
          bgClass: 'bg-gray-100',
        };
    }
  };

  const config = getStatusConfig();
  const Icon = config.icon;

  return (
    <div className={`inline-flex items-center space-x-1 px-2.5 py-0.5 rounded-full ${config.bgClass} ${className}`}>
      <Icon className={`h-4 w-4 ${config.colorClass}`} />
      <span className={`text-sm font-medium ${config.colorClass}`}>{config.text}</span>
    </div>
  );
};