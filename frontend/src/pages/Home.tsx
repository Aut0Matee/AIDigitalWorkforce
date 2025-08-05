import React, { useState, useEffect } from 'react';
import { Plus, Loader2 } from 'lucide-react';
import { Link } from 'react-router-dom';
import { TaskCreation } from '../components/task/TaskCreation';
import { TaskList } from '../components/task/TaskList';
import { taskApi } from '../services/api';
import { Task } from '../types';

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
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">AI Digital Workforce</h1>
        <p className="text-lg text-gray-600">
          Watch AI agents collaborate in real-time to complete your tasks
        </p>
      </div>

      {showCreate ? (
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold text-gray-900">Create New Task</h2>
            <button
              onClick={() => setShowCreate(false)}
              className="text-sm text-gray-600 hover:text-gray-900"
            >
              Cancel
            </button>
          </div>
          <TaskCreation />
        </div>
      ) : (
        <div className="mb-8">
          <button
            onClick={() => setShowCreate(true)}
            className="flex items-center space-x-2 bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 transition-colors"
          >
            <Plus className="h-5 w-5" />
            <span>Create New Task</span>
          </button>
        </div>
      )}

      <div>
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Recent Tasks</h2>
        {loading ? (
          <div className="flex items-center justify-center py-12">
            <Loader2 className="h-8 w-8 animate-spin text-primary-600" />
          </div>
        ) : (
          <TaskList tasks={tasks} />
        )}
      </div>
    </div>
  );
};