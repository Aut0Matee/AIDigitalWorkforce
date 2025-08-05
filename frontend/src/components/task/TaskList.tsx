import React from 'react';
import { Link } from 'react-router-dom';
import { ChevronRight, FileText, Calendar } from 'lucide-react';
import { Task } from '../../types';
import { TaskStatus } from './TaskStatus';
import { formatDate } from '../../utils/date';

interface TaskListProps {
  tasks: Task[];
}

export const TaskList: React.FC<TaskListProps> = ({ tasks }) => {
  if (tasks.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow p-8 text-center">
        <FileText className="h-12 w-12 text-gray-400 mx-auto mb-4" />
        <p className="text-gray-500">No tasks yet. Create your first task to get started!</p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow overflow-hidden">
      <ul className="divide-y divide-gray-200">
        {tasks.map((task) => (
          <li key={task.id}>
            <Link
              to={`/task/${task.id}`}
              className="block hover:bg-gray-50 px-6 py-4 transition-colors"
            >
              <div className="flex items-center justify-between">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between mb-2">
                    <h3 className="text-lg font-medium text-gray-900 truncate">
                      {task.title}
                    </h3>
                    <TaskStatus status={task.status} />
                  </div>
                  
                  <p className="text-sm text-gray-600 line-clamp-2 mb-2">
                    {task.description}
                  </p>
                  
                  <div className="flex items-center text-xs text-gray-500 space-x-4">
                    <div className="flex items-center space-x-1">
                      <Calendar className="h-3 w-3" />
                      <span>{formatDate(task.created_at)}</span>
                    </div>
                    {task.deliverable && (
                      <span className="text-green-600 font-medium">
                        ✓ Deliverable ready
                      </span>
                    )}
                  </div>
                </div>
                
                <ChevronRight className="h-5 w-5 text-gray-400 ml-4" />
              </div>
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
};