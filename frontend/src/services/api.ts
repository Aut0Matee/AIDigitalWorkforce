import axios from 'axios';
import type { Task, TaskCreate, TaskListResponse, Message, MessageListResponse } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Task API
export const taskApi = {
  create: async (data: TaskCreate): Promise<Task> => {
    const response = await api.post<Task>('/tasks/', data);
    return response.data;
  },

  list: async (page = 1, size = 10, status?: string): Promise<TaskListResponse> => {
    const params = new URLSearchParams({
      page: page.toString(),
      size: size.toString(),
    });
    if (status) params.append('status', status);
    
    const response = await api.get<TaskListResponse>(`/tasks/?${params}`);
    return response.data;
  },

  get: async (id: string): Promise<Task> => {
    const response = await api.get<Task>(`/tasks/${id}`);
    return response.data;
  },

  delete: async (id: string): Promise<void> => {
    await api.delete(`/tasks/${id}`);
  },
};

// Message API
export const messageApi = {
  getTaskMessages: async (taskId: string): Promise<MessageListResponse> => {
    const response = await api.get<MessageListResponse>(`/messages/task/${taskId}`);
    return response.data;
  },

  create: async (taskId: string, content: string, agentRole = 'human'): Promise<Message> => {
    const response = await api.post<Message>('/messages/', {
      task_id: taskId,
      content,
      agent_role: agentRole,
    });
    return response.data;
  },
};

// Health check
export const healthCheck = async (): Promise<boolean> => {
  try {
    await api.get('/health');
    return true;
  } catch {
    return false;
  }
};