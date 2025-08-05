import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Download, Loader2, Trash2 } from 'lucide-react';
import type { Task, Message } from '../types';
import { taskApi, messageApi } from '../services/api';
import { socketService } from '../services/socket';
import { ChatWindow } from '../components/chat/ChatWindow';
import { TaskStatus } from '../components/task/TaskStatus';
import { ExportModal } from '../components/export/ExportModal';
import { formatDate } from '../utils/date';

export const TaskDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [task, setTask] = useState<Task | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(true);
  const [deleting, setDeleting] = useState(false);
  const [showExport, setShowExport] = useState(false);

  useEffect(() => {
    if (id) {
      loadTaskData();
      socketService.connect(id);
      socketService.subscribeToTask(id);

      // Listen for task updates
      const handleTaskCompleted = (data: any) => {
        if (data.task_id === id) {
          setTask(prev => prev ? { ...prev, status: 'completed', deliverable: data.deliverable } : null);
        }
      };

      const handleTaskStarted = (data: any) => {
        if (data.task_id === id) {
          setTask(prev => prev ? { ...prev, status: 'in_progress' } : null);
        }
      };

      socketService.on('task_completed', handleTaskCompleted);
      socketService.on('task_started', handleTaskStarted);

      return () => {
        socketService.off('task_completed', handleTaskCompleted);
        socketService.off('task_started', handleTaskStarted);
      };
    }
  }, [id]);

  const loadTaskData = async () => {
    if (!id) return;

    try {
      setLoading(true);
      const [taskData, messagesData] = await Promise.all([
        taskApi.get(id),
        messageApi.getTaskMessages(id),
      ]);
      setTask(taskData);
      setMessages(messagesData.messages);
    } catch (error) {
      console.error('Failed to load task:', error);
      navigate('/');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!id || !confirm('Are you sure you want to delete this task?')) return;

    setDeleting(true);
    try {
      await taskApi.delete(id);
      navigate('/');
    } catch (error) {
      console.error('Failed to delete task:', error);
      setDeleting(false);
    }
  };

  if (loading || !task) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Loader2 className="h-8 w-8 animate-spin text-primary-600" />
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-6">
        <button
          onClick={() => navigate('/')}
          className="flex items-center space-x-2 text-gray-600 hover:text-gray-900 mb-4"
        >
          <ArrowLeft className="h-4 w-4" />
          <span>Back to Tasks</span>
        </button>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-start justify-between mb-4">
            <div className="flex-1">
              <h1 className="text-2xl font-bold text-gray-900 mb-2">{task.title}</h1>
              <p className="text-gray-600 mb-4">{task.description}</p>
              
              <div className="flex items-center space-x-4 text-sm text-gray-500">
                <TaskStatus status={task.status} />
                <span>Created {formatDate(task.created_at)}</span>
                {task.updated_at && (
                  <span>Updated {formatDate(task.updated_at)}</span>
                )}
              </div>
            </div>

            <div className="flex items-center space-x-2">
              {task.deliverable && (
                <button
                  onClick={() => setShowExport(true)}
                  className="flex items-center space-x-2 bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 transition-colors"
                >
                  <Download className="h-4 w-4" />
                  <span>Export</span>
                </button>
              )}
              
              <button
                onClick={handleDelete}
                disabled={deleting}
                className="flex items-center space-x-2 bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {deleting ? (
                  <Loader2 className="h-4 w-4 animate-spin" />
                ) : (
                  <Trash2 className="h-4 w-4" />
                )}
                <span>Delete</span>
              </button>
            </div>
          </div>

          {task.deliverable && (
            <div className="mt-6 p-4 bg-green-50 border border-green-200 rounded-md">
              <h3 className="text-sm font-medium text-green-800 mb-2">
                ✓ Deliverable Ready
              </h3>
              <p className="text-sm text-green-700">
                The agents have completed your task. You can export the deliverable as PDF or Markdown.
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Chat Window */}
      <div className="h-[600px]">
        <ChatWindow taskId={task.id} initialMessages={messages} />
      </div>

      {/* Export Modal */}
      <ExportModal
        isOpen={showExport}
        onClose={() => setShowExport(false)}
        content={task.deliverable || ''}
        title={task.title}
      />
    </div>
  );
};