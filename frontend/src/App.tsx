import { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme, CssBaseline } from '@mui/material';
import { MainLayout } from '@components/layout/MainLayout';
import { Home } from '@pages/Home';
import { TaskDetail } from '@pages/TaskDetail';
import { socketService } from '@services/socket';

// Create Material-UI theme
const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
    background: {
      default: '#f5f5f5',
    },
  },
  typography: {
    fontFamily: [
      '-apple-system',
      'BlinkMacSystemFont',
      '"Segoe UI"',
      'Roboto',
      '"Helvetica Neue"',
      'Arial',
      'sans-serif',
    ].join(','),
  },
});

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
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Routes>
          <Route path="/" element={<MainLayout />}>
            <Route index element={<Home />} />
            <Route path="task/:id" element={<TaskDetail />} />
          </Route>
        </Routes>
      </Router>
    </ThemeProvider>
  );
}

export default App;