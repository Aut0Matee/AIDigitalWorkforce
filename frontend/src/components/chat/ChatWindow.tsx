import React, { useState, useEffect, useRef } from 'react';
import { Send, Loader2 } from 'lucide-react';
import { Message } from '../../types';
import { MessageBubble } from './MessageBubble';
import { messageApi } from '../../services/api';
import { socketService } from '../../services/socket';

interface ChatWindowProps {
  taskId: string;
  initialMessages: Message[];
}

export const ChatWindow: React.FC<ChatWindowProps> = ({ taskId, initialMessages }) => {
  const [messages, setMessages] = useState<Message[]>(initialMessages);
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
        const newMessage: Message = {
          id: Date.now().toString(),
          task_id: data.task_id,
          agent_role: data.agent_role,
          content: data.message,
          created_at: data.timestamp,
        };
        setMessages(prev => [...prev, newMessage]);
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
    <div className="flex flex-col h-full bg-white rounded-lg shadow">
      <div className="flex-1 overflow-y-auto p-4 space-y-4 custom-scrollbar">
        {messages.length === 0 ? (
          <div className="text-center text-gray-500 py-8">
            <p>Waiting for agents to start working...</p>
          </div>
        ) : (
          messages.map((message) => (
            <MessageBubble key={message.id} message={message} />
          ))
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="border-t p-4">
        <div className="flex space-x-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
            placeholder="Type your message to guide the agents..."
            className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            disabled={sending}
          />
          <button
            onClick={handleSend}
            disabled={!input.trim() || sending}
            className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {sending ? (
              <Loader2 className="h-5 w-5 animate-spin" />
            ) : (
              <Send className="h-5 w-5" />
            )}
          </button>
        </div>
      </div>
    </div>
  );
};