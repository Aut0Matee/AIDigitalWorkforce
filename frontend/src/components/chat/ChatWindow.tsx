import React, { useState, useEffect, useRef } from 'react';
import {
  Paper,
  Box,
  TextField,
  IconButton,
  Typography,
  InputAdornment,
  CircularProgress
} from '@mui/material';
import { Send as SendIcon } from '@mui/icons-material';
import type { Message } from '@/types';
import { MessageBubble } from './MessageBubble';
import { messageApi } from '@services/api';
import { socketService } from '@services/socket';

interface ChatWindowProps {
  taskId: string;
  initialMessages: Message[];
}

export const ChatWindow: React.FC<ChatWindowProps> = ({ taskId, initialMessages }) => {
  // Filter out any empty messages from initial load
  const [messages, setMessages] = useState<Message[]>(
    initialMessages.filter(msg => msg.content && msg.content.trim())
  );
  const [input, setInput] = useState('');
  const [sending, setSending] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Subscribe to real-time updates
    const handleAgentMessage = (data: any) => {
      if (data.task_id === taskId) {
        // Handle both 'message' and 'content' fields for compatibility
        const messageContent = data.message || data.content || '';
        
        // Only add non-empty messages
        if (messageContent.trim()) {
          const newMessage: Message = {
            id: Date.now().toString(),
            task_id: data.task_id,
            agent_role: data.agent_role,
            content: messageContent,
            created_at: data.timestamp,
          };
          setMessages(prev => [...prev, newMessage]);
        }
      }
    };

    socketService.on('agent_message', handleAgentMessage);

    return () => {
      socketService.off('agent_message', handleAgentMessage);
    };
  }, [taskId]);

  const handleSend = async () => {
    if (!input.trim() || sending) return;

    const content = input.trim();
    setInput('');
    setSending(true);

    // Add optimistic message
    const optimisticMessage: Message = {
      id: `temp-${Date.now()}`,
      task_id: taskId,
      agent_role: 'human',
      content,
      created_at: new Date().toISOString(),
    };
    setMessages(prev => [...prev, optimisticMessage]);

    try {
      // Send via WebSocket for real-time intervention
      socketService.sendHumanIntervention(taskId, content);
      
      // Also save to database
      const savedMessage = await messageApi.create(taskId, content, 'human');
      
      // Replace optimistic message with saved one
      setMessages(prev => 
        prev.map(msg => msg.id === optimisticMessage.id ? savedMessage : msg)
      );
    } catch (error) {
      console.error('Failed to send message:', error);
      // Remove optimistic message on error
      setMessages(prev => prev.filter(msg => msg.id !== optimisticMessage.id));
    } finally {
      setSending(false);
    }
  };

  return (
    <Paper elevation={2} sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <Box
        sx={{
          flexGrow: 1,
          overflowY: 'auto',
          p: 2,
          display: 'flex',
          flexDirection: 'column',
          gap: 2,
        }}
      >
        {messages.length === 0 ? (
          <Box sx={{ textAlign: 'center', py: 4 }}>
            <Typography color="text.secondary">
              Waiting for agents to start working...
            </Typography>
          </Box>
        ) : (
          messages.map((message) => (
            <MessageBubble key={message.id} message={message} />
          ))
        )}
        <div ref={messagesEndRef} />
      </Box>

      <Box sx={{ borderTop: 1, borderColor: 'divider', p: 2 }}>
        <TextField
          fullWidth
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          placeholder="Type your message to guide the agents..."
          disabled={sending}
          InputProps={{
            endAdornment: (
              <InputAdornment position="end">
                <IconButton
                  onClick={handleSend}
                  disabled={!input.trim() || sending}
                  color="primary"
                >
                  {sending ? <CircularProgress size={24} /> : <SendIcon />}
                </IconButton>
              </InputAdornment>
            ),
          }}
        />
      </Box>
    </Paper>
  );
};