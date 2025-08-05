import React, { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { MainLayout } from './components/layout/MainLayout';
import { Home } from './pages/Home';
import { TaskDetail } from './pages/TaskDetail';
import { socketService } from './services/socket';

function App() {
  useEffect(() => {
    // Connect to WebSocket on app load
    socketService.connect();

    return () => {
      // Disconnect on unmount
      socketService.disconnect();
    };
  }, []);

  return (
    <Router>
      <Routes>
        <Route path="/" element={<MainLayout />}>
          <Route index element={<Home />} />
          <Route path="task/:id" element={<TaskDetail />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;