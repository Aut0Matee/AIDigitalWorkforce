import React from 'react';
import { Link } from 'react-router-dom';
import {
  List,
  ListItem,
  ListItemButton,
  ListItemText,
  Paper,
  Typography,
  Box,
  Chip
} from '@mui/material';
import {
  ChevronRight as ChevronRightIcon,
  Description as FileTextIcon,
  CalendarMonth as CalendarIcon,
  CheckCircle as CheckIcon
} from '@mui/icons-material';
import type { Task } from '@/types';
import { TaskStatus } from './TaskStatus';
import { formatDate } from '@utils/date';

interface TaskListProps {
  tasks: Task[];
}

export const TaskList: React.FC<TaskListProps> = ({ tasks }) => {
  if (tasks.length === 0) {
    return (
      <Paper elevation={1} sx={{ p: 4, textAlign: 'center' }}>
        <FileTextIcon sx={{ fontSize: 48, color: 'text.secondary', mb: 2 }} />
        <Typography color="text.secondary">
          No tasks yet. Create your first task to get started!
        </Typography>
      </Paper>
    );
  }

  return (
    <Paper elevation={1}>
      <List disablePadding>
        {tasks.map((task, index) => (
          <ListItem
            key={task.id}
            divider={index < tasks.length - 1}
            disablePadding
          >
            <ListItemButton component={Link} to={`/task/${task.id}`}>
              <ListItemText
                primary={
                  <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
                    <Typography variant="h6" component="h3" sx={{ flexGrow: 1 }}>
                      {task.title}
                    </Typography>
                    <TaskStatus status={task.status} />
                  </Box>
                }
                secondary={
                  <>
                    <Typography
                      variant="body2"
                      color="text.secondary"
                      sx={{
                        overflow: 'hidden',
                        textOverflow: 'ellipsis',
                        display: '-webkit-box',
                        WebkitLineClamp: 2,
                        WebkitBoxOrient: 'vertical',
                        mb: 1
                      }}
                    >
                      {task.description}
                    </Typography>
                    <Box display="flex" alignItems="center" gap={2}>
                      <Box display="flex" alignItems="center" gap={0.5}>
                        <CalendarIcon sx={{ fontSize: 16 }} />
                        <Typography variant="caption">
                          {formatDate(task.created_at)}
                        </Typography>
                      </Box>
                      {task.deliverable && (
                        <Chip
                          icon={<CheckIcon />}
                          label="Deliverable ready"
                          size="small"
                          color="success"
                          variant="outlined"
                        />
                      )}
                    </Box>
                  </>
                }
              />
              <ChevronRightIcon color="action" />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
    </Paper>
  );
};