import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Box,
  Typography,
  Button,
  Paper,
  CircularProgress,
  Alert,
  Breadcrumbs,
  Link
} from '@mui/material';
import {
  ArrowBack as ArrowLeftIcon,
  Download as DownloadIcon,
  Delete as TrashIcon,
  CheckCircle as CheckIcon
} from '@mui/icons-material';
import type { Task, Message } from '@/types';
import { taskApi, messageApi } from '@services/api';
import { socketService } from '@services/socket';
import { ChatWindow } from '@components/chat/ChatWindow';
import { TaskStatus } from '@components/task/TaskStatus';
import { ExportModal } from '@components/export/ExportModal';
import { formatDate } from '@utils/date';

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
          setTask((prev: Task | null) => prev ? { ...prev, status: 'completed', deliverable: data.deliverable } : null);
        }
      };

      const handleTaskStarted = (data: any) => {
        if (data.task_id === id) {
          setTask((prev: Task | null) => prev ? { ...prev, status: 'in_progress' } : null);
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
      // Filter out empty messages
      const validMessages = messagesData.messages.filter(
        (msg: Message) => msg.content && msg.content.trim()
      );
      setMessages(validMessages);
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
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="80vh">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ py: 3 }}>
      {/* Breadcrumbs */}
      <Breadcrumbs sx={{ mb: 3 }}>
        <Link
          component="button"
          variant="body1"
          onClick={() => navigate('/')}
          sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}
        >
          <ArrowLeftIcon fontSize="small" />
          Tasks
        </Link>
        <Typography color="text.primary">{task.title}</Typography>
      </Breadcrumbs>

      {/* Task Info */}
      <Paper elevation={2} sx={{ p: 3, mb: 3 }}>
        <Box display="flex" justifyContent="space-between" alignItems="flex-start" mb={2}>
          <Box flex={1}>
            <Typography variant="h4" component="h1" gutterBottom>
              {task.title}
            </Typography>
            <Typography variant="body1" color="text.secondary" paragraph>
              {task.description}
            </Typography>
            
            <Box display="flex" alignItems="center" gap={2} flexWrap="wrap">
              <TaskStatus status={task.status} size="medium" />
              <Typography variant="body2" color="text.secondary">
                Created {formatDate(task.created_at)}
              </Typography>
              {task.updated_at && (
                <Typography variant="body2" color="text.secondary">
                  Updated {formatDate(task.updated_at)}
                </Typography>
              )}
            </Box>
          </Box>

          <Box display="flex" gap={1}>
            {task.deliverable && (
              <Button
                variant="contained"
                color="success"
                startIcon={<DownloadIcon />}
                onClick={() => setShowExport(true)}
              >
                Export
              </Button>
            )}
            
            <Button
              variant="contained"
              color="error"
              startIcon={deleting ? <CircularProgress size={20} /> : <TrashIcon />}
              onClick={handleDelete}
              disabled={deleting}
            >
              Delete
            </Button>
          </Box>
        </Box>

        {task.deliverable && (
          <Alert
            severity="success"
            icon={<CheckIcon />}
            sx={{ mt: 3 }}
          >
            <Typography variant="subtitle2" fontWeight="bold">
              Deliverable Ready
            </Typography>
            <Typography variant="body2">
              The agents have completed your task. You can export the deliverable as PDF or Markdown.
            </Typography>
          </Alert>
        )}
      </Paper>

      {/* Chat Window */}
      <Box height={600}>
        <ChatWindow taskId={task.id} initialMessages={messages} />
      </Box>

      {/* Export Modal */}
      <ExportModal
        isOpen={showExport}
        onClose={() => setShowExport(false)}
        content={task.deliverable || ''}
        title={task.title}
      />
    </Box>
  );
};