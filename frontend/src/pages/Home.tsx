import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Button,
  CircularProgress,
  IconButton,
  Collapse
} from '@mui/material';
import { Add as PlusIcon, Close as CloseIcon } from '@mui/icons-material';
import { TaskCreation } from '@components/task/TaskCreation';
import { TaskList } from '@components/task/TaskList';
import { taskApi } from '@services/api';
import type { Task } from '@/types';

export const Home: React.FC = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [showCreate, setShowCreate] = useState(false);

  useEffect(() => {
    loadTasks();
  }, []);

  const loadTasks = async () => {
    try {
      const response = await taskApi.list(1, 20);
      setTasks(response.tasks);
    } catch (error) {
      console.error('Failed to load tasks:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ py: 4 }}>
      <Box mb={4}>
        <Typography variant="h3" component="h1" gutterBottom fontWeight="bold">
          AI Digital Workforce
        </Typography>
        <Typography variant="h6" color="text.secondary">
          Watch AI agents collaborate in real-time to complete your tasks
        </Typography>
      </Box>

      <Collapse in={showCreate}>
        <Box mb={4}>
          <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
            <Typography variant="h5" component="h2">
              Create New Task
            </Typography>
            <IconButton onClick={() => setShowCreate(false)} size="small">
              <CloseIcon />
            </IconButton>
          </Box>
          <TaskCreation />
        </Box>
      </Collapse>

      <Collapse in={!showCreate}>
        <Box mb={4}>
          <Button
            variant="contained"
            startIcon={<PlusIcon />}
            onClick={() => setShowCreate(true)}
            size="large"
          >
            Create New Task
          </Button>
        </Box>
      </Collapse>

      <Box>
        <Typography variant="h5" component="h2" gutterBottom>
          Recent Tasks
        </Typography>
        {loading ? (
          <Box display="flex" justifyContent="center" py={6}>
            <CircularProgress />
          </Box>
        ) : (
          <TaskList tasks={tasks} />
        )}
      </Box>
    </Box>
  );
};