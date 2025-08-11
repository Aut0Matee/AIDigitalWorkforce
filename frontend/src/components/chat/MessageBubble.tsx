import React from 'react';
import { Box, Typography, Paper } from '@mui/material';
import type { Message } from '@/types';
import { AgentAvatar } from './AgentAvatar';
import { MarkdownRenderer } from '@components/common/MarkdownRenderer';
import { formatDistanceToNow } from '@utils/date';

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

  const getBubbleColor = () => {
    switch (message.agent_role) {
      case 'researcher':
        return '#e3f2fd';
      case 'writer':
        return '#f3e5f5';
      case 'analyst':
        return '#e8f5e9';
      case 'human':
        return '#fff3e0';
      case 'system':
        return '#fafafa';
      default:
        return '#f5f5f5';
    }
  };

  return (
    <Box display="flex" gap={2}>
      <AgentAvatar role={message.agent_role} />
      
      <Box flex={1}>
        <Box display="flex" alignItems="center" gap={1} mb={0.5}>
          <Typography variant="subtitle2" fontWeight="bold">
            {getRoleName()}
          </Typography>
          <Typography variant="caption" color="text.secondary">
            {formatDistanceToNow(message.created_at)}
          </Typography>
        </Box>
        
        <Paper
          elevation={0}
          sx={{
            p: 2,
            backgroundColor: getBubbleColor(),
            borderRadius: 2,
          }}
        >
          <MarkdownRenderer content={message.content} />
        </Paper>
      </Box>
    </Box>
  );
};