import React from 'react';
import { Link } from 'react-router-dom';
import { AppBar, Toolbar, Typography, Box, Chip, IconButton } from '@mui/material';
import { SmartToy as BotIcon, Wifi as WifiIcon, WifiOff as WifiOffIcon } from '@mui/icons-material';
import { socketService } from '@services/socket';

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
    <AppBar position="sticky" elevation={1}>
      <Toolbar>
        <Box display="flex" alignItems="center" flexGrow={1}>
          <IconButton 
            component={Link} 
            to="/" 
            edge="start" 
            color="inherit"
            sx={{ mr: 2 }}
          >
            <BotIcon />
          </IconButton>
          <Typography variant="h6" component="div">
            AI Digital Workforce
          </Typography>
        </Box>
        
        <Chip
          icon={isConnected ? <WifiIcon /> : <WifiOffIcon />}
          label={isConnected ? 'Connected' : 'Disconnected'}
          color={isConnected ? 'success' : 'error'}
          size="small"
          variant="outlined"
        />
      </Toolbar>
    </AppBar>
  );
};