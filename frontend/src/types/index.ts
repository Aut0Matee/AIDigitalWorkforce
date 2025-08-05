export interface Task {
  id: string;
  title: string;
  description: string;
  status: 'created' | 'in_progress' | 'completed' | 'failed';
  deliverable: string | null;
  created_at: string;
  updated_at: string | null;
}

export interface Message {
  id: string;
  task_id: string;
  content: string;
  agent_role: 'researcher' | 'writer' | 'analyst' | 'human' | 'system';
  created_at: string;
}

export interface TaskListResponse {
  tasks: Task[];
  total: number;
  page: number;
  size: number;
}

export interface MessageListResponse {
  messages: Message[];
  total: number;
  task_id: string;
}

export interface TaskCreate {
  title: string;
  description: string;
}

export interface AgentInfo {
  role: string;
  name: string;
  description: string;
  capabilities: string[];
}