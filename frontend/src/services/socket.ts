import { io, Socket } from 'socket.io-client';

const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000';

class SocketService {
  private socket: Socket | null = null;
  private listeners: Map<string, Set<Function>> = new Map();

  connect(taskId?: string): void {
    if (this.socket?.connected) {
      return;
    }

    this.socket = io(WS_URL, {
      auth: taskId ? { task_id: taskId } : {},
      transports: ['websocket', 'polling'],
    });

    this.socket.on('connect', () => {
      console.log('Connected to WebSocket');
      this.emit('connected', { connected: true });
    });

    this.socket.on('disconnect', () => {
      console.log('Disconnected from WebSocket');
      this.emit('connected', { connected: false });
    });

    // Forward all events to listeners
    const events = [
      'task_started',
      'agent_message',
      'task_completed',
      'human_intervention',
      'error',
      'task_subscribed',
    ];

    events.forEach(event => {
      this.socket!.on(event, (data) => {
        this.emit(event, data);
      });
    });
  }

  disconnect(): void {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
    }
  }

  subscribeToTask(taskId: string): void {
    if (this.socket?.connected) {
      this.socket.emit('subscribe_task', { task_id: taskId });
    }
  }

  sendHumanIntervention(taskId: string, message: string): void {
    if (this.socket?.connected) {
      this.socket.emit('human_intervention', { task_id: taskId, message });
    }
  }

  on(event: string, callback: Function): void {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, new Set());
    }
    this.listeners.get(event)!.add(callback);
  }

  off(event: string, callback: Function): void {
    if (this.listeners.has(event)) {
      this.listeners.get(event)!.delete(callback);
    }
  }

  private emit(event: string, data: any): void {
    if (this.listeners.has(event)) {
      this.listeners.get(event)!.forEach(callback => {
        callback(data);
      });
    }
  }

  isConnected(): boolean {
    return this.socket?.connected || false;
  }
}

export const socketService = new SocketService();