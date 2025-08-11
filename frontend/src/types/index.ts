export enum TaskStatus {
  CREATED = 'created',
  IN_PROGRESS = 'in_progress',
  COMPLETED = 'completed',
  FAILED = 'failed'
}

export enum AgentRole {
  RESEARCHER = 'researcher',
  WRITER = 'writer',
  ANALYST = 'analyst',
  HUMAN = 'human',
  SYSTEM = 'system'
}

export interface Task {
  id: string;
  title: string;
  description: string;
  status: TaskStatus | 'created' | 'in_progress' | 'completed' | 'failed';
  deliverable: string | null;
  created_at: string;
  updated_at: string | null;
}

export interface Message {
  id: string;
  task_id: string;
  content: string;
  agent_role: AgentRole | 'researcher' | 'writer' | 'analyst' | 'human' | 'system';
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
  avatar?: string;
  color?: string;
}

export interface ExportOptions {
  format: 'pdf' | 'markdown' | 'docx';
  includeMetadata?: boolean;
  includeChat?: boolean;
}

export interface WebSocketMessage {
  event: 'task_started' | 'agent_message' | 'task_completed' | 'error' | 'user_message';
  task_id: string;
  data: any;
}