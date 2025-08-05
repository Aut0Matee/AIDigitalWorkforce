import React from 'react';
import { Link } from 'react-router-dom';
import { Bot, Activity } from 'lucide-react';
import { socketService } from '../../services/socket';

export const Header: React.FC = () => {
  const [isConnected, setIsConnected] = React.useState(false);

  React.useEffect(() => {
    const handleConnection = ({ connected }: { connected: boolean }) => {
      setIsConnected(connected);
    };

    socketService.on('connected', handleConnection);
    setIsConnected(socketService.isConnected());

    return () => {
      socketService.off('connected', handleConnection);
    };
  }, []);

  return (
    <header className="bg-white border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <Link to="/" className="flex items-center space-x-2">
            <Bot className="h-8 w-8 text-primary-600" />
            <span className="text-xl font-bold text-gray-900">AI Digital Workforce</span>
          </Link>
          
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <Activity className={`h-4 w-4 ${isConnected ? 'text-green-500' : 'text-red-500'}`} />
              <span className="text-sm text-gray-600">
                {isConnected ? 'Connected' : 'Disconnected'}
              </span>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};