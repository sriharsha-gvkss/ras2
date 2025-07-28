import React, { useState, useEffect } from 'react';
import {
  Container,
  Box,
  Typography,
  TextField,
  Button,
  Card,
  CardContent,
  Grid,
  Tabs,
  Tab,
  Alert,
  Paper,
  Divider,
  InputAdornment,
  Fade,
  Zoom,
  IconButton,
  CircularProgress
} from '@mui/material';
import { 
  Person, 
  AdminPanelSettings, 
  PersonAdd, 
  Lock, 
  Email, 
  Visibility, 
  VisibilityOff,
  Security,
  VerifiedUser
} from '@mui/icons-material';
import axios from 'axios';

const Login = ({ onLogin }) => {
  const [activeTab, setActiveTab] = useState(0);
  const [userUsername, setUserUsername] = useState('');
  const [userPassword, setUserPassword] = useState('');
  const [adminUsername, setAdminUsername] = useState('');
  const [adminPassword, setAdminPassword] = useState('');
  const [regUsername, setRegUsername] = useState('');
  const [regPassword, setRegPassword] = useState('');
  const [regEmail, setRegEmail] = useState('');
  const [regRole, setRegRole] = useState('user');
  const [message, setMessage] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [showRegPassword, setShowRegPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [backendStatus, setBackendStatus] = useState('checking');

  const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';

  // Check backend status on component mount
  useEffect(() => {
    const checkBackendStatus = async () => {
      try {
        const response = await axios.get(`${BACKEND_URL}/health`, { timeout: 5000 });
        if (response.status === 200) {
          setBackendStatus('connected');
        } else {
          setBackendStatus('error');
        }
      } catch (error) {
        console.error('Backend status check failed:', error);
        setBackendStatus('disconnected');
      }
    };

    checkBackendStatus();
  }, [BACKEND_URL]);

  const handleUserLogin = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setMessage('');

    try {
      const response = await axios.post(`${BACKEND_URL}/auth/login`, {
        username: userUsername,
        password: userPassword
      }, {
        timeout: 10000 // 10 second timeout
      });

      if (response.data.access_token) {
        // Store token in localStorage
        localStorage.setItem('authToken', response.data.access_token);
        localStorage.setItem('userRole', response.data.role);
        onLogin(response.data.role);
      }
    } catch (error) {
      console.error('Login error:', error);
      if (error.response?.status === 401) {
        setMessage('Invalid username or password. Try: user / user123 or admin / admin123');
      } else if (error.code === 'ERR_NETWORK' || error.code === 'ECONNREFUSED') {
        setMessage('Cannot connect to server. Please check if the backend is running at http://localhost:8000');
      } else if (error.code === 'ECONNABORTED') {
        setMessage('Request timed out. Please check your connection and try again.');
      } else {
        setMessage('Login failed. Please try again.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleAdminLogin = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setMessage('');

    try {
      const response = await axios.post(`${BACKEND_URL}/auth/login`, {
        username: adminUsername,
        password: adminPassword
      }, {
        timeout: 10000 // 10 second timeout
      });

      if (response.data.access_token) {
        localStorage.setItem('authToken', response.data.access_token);
        localStorage.setItem('userRole', response.data.role);
        onLogin(response.data.role);
      }
    } catch (error) {
      console.error('Login error:', error);
      if (error.response?.status === 401) {
        setMessage('Invalid username or password. Try: user / user123 or admin / admin123');
      } else if (error.code === 'ERR_NETWORK' || error.code === 'ECONNREFUSED') {
        setMessage('Cannot connect to server. Please check if the backend is running at http://localhost:8000');
      } else if (error.code === 'ECONNABORTED') {
        setMessage('Request timed out. Please check your connection and try again.');
      } else {
        setMessage('Login failed. Please try again.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleRegistration = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setMessage('');

    try {
      const response = await axios.post(`${BACKEND_URL}/auth/register`, {
        username: regUsername,
        password: regPassword,
        email: regEmail,
        role: regRole
      }, {
        timeout: 10000 // 10 second timeout
      });

      setMessage(`Registration successful! You can now login as ${regRole}`);
      setRegUsername('');
      setRegPassword('');
      setRegEmail('');
      setRegRole('user');
    } catch (error) {
      console.error('Registration error:', error);
      if (error.response?.status === 400) {
        setMessage('Username already exists. Please choose a different username.');
      } else if (error.code === 'ERR_NETWORK' || error.code === 'ECONNREFUSED') {
        setMessage('Cannot connect to server. Please check if the backend is running at http://localhost:8000');
      } else if (error.code === 'ECONNABORTED') {
        setMessage('Request timed out. Please check your connection and try again.');
      } else {
        setMessage('Registration failed. Please try again.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
    setMessage('');
  };

  return (
    <Box
      sx={{
        minHeight: '100vh',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        py: 4
      }}
    >
      <Container maxWidth="md">
        <Fade in timeout={1000}>
          <Box
            sx={{
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
            }}
          >
            <Zoom in timeout={1200}>
              <Paper
                elevation={24}
                sx={{
                  p: 4,
                  borderRadius: 4,
                  background: 'rgba(255, 255, 255, 0.95)',
                  backdropFilter: 'blur(10px)',
                  border: '1px solid rgba(255, 255, 255, 0.2)',
                  width: '100%',
                  maxWidth: 500
                }}
              >
                <Box sx={{ textAlign: 'center', mb: 3 }}>
                  <Security sx={{ fontSize: 60, color: 'primary.main', mb: 2 }} />
                  <Typography 
                    component="h1" 
                    variant="h4" 
                    gutterBottom
                    sx={{ 
                      fontWeight: 'bold',
                      background: 'linear-gradient(45deg, #667eea, #764ba2)',
                      backgroundClip: 'text',
                      WebkitBackgroundClip: 'text',
                      WebkitTextFillColor: 'transparent'
                    }}
                  >
                    AI Assistant Portal
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Secure access to your AI-powered workspace
                  </Typography>
                </Box>
                
                <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
                  <Tabs 
                    value={activeTab} 
                    onChange={handleTabChange} 
                    sx={{ 
                      '& .MuiTab-root': {
                        fontWeight: 'bold',
                        textTransform: 'none',
                        fontSize: '1rem'
                      }
                    }}
                    variant="fullWidth"
                  >
                    <Tab 
                      label="User Login" 
                      icon={<Person />} 
                      iconPosition="start"
                    />
                    <Tab 
                      label="Admin Login" 
                      icon={<AdminPanelSettings />} 
                      iconPosition="start"
                    />
                    <Tab 
                      label="Register" 
                      icon={<PersonAdd />} 
                      iconPosition="start"
                    />
                  </Tabs>
                </Box>

                {/* Backend Status Indicator */}
                <Box sx={{ mb: 2, textAlign: 'center' }}>
                  <Typography variant="body2" color="text.secondary" sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 1 }}>
                    <Box
                      component="span"
                      sx={{
                        width: 8,
                        height: 8,
                        borderRadius: '50%',
                        backgroundColor: 
                          backendStatus === 'connected' ? 'success.main' :
                          backendStatus === 'checking' ? 'warning.main' :
                          'error.main',
                        display: 'inline-block'
                      }}
                    />
                    Backend: {
                      backendStatus === 'connected' ? 'Connected' :
                      backendStatus === 'checking' ? 'Checking...' :
                      'Disconnected'
                    }
                  </Typography>
                </Box>

                {message && (
                  <Alert 
                    severity={message.includes('successful') ? 'success' : 'error'} 
                    sx={{ mb: 3, borderRadius: 2 }}
                    icon={message.includes('successful') ? <VerifiedUser /> : undefined}
                  >
                    {message}
                  </Alert>
                )}

                {activeTab === 0 && (
                  <Zoom in timeout={300}>
                    <form onSubmit={handleUserLogin}>
                      <TextField
                        fullWidth
                        label="Username"
                        value={userUsername}
                        onChange={(e) => setUserUsername(e.target.value)}
                        margin="normal"
                        required
                        autoComplete="username"
                        disabled={isLoading}
                        InputProps={{
                          startAdornment: (
                            <InputAdornment position="start">
                              <Person color="primary" />
                            </InputAdornment>
                          ),
                        }}
                        sx={{ mb: 2 }}
                      />
                      <TextField
                        fullWidth
                        label="Password"
                        type={showPassword ? 'text' : 'password'}
                        value={userPassword}
                        onChange={(e) => setUserPassword(e.target.value)}
                        margin="normal"
                        required
                        autoComplete="current-password"
                        disabled={isLoading}
                        InputProps={{
                          startAdornment: (
                            <InputAdornment position="start">
                              <Lock color="primary" />
                            </InputAdornment>
                          ),
                          endAdornment: (
                            <InputAdornment position="end">
                              <IconButton
                                onClick={() => setShowPassword(!showPassword)}
                                edge="end"
                                disabled={isLoading}
                              >
                                {showPassword ? <VisibilityOff /> : <Visibility />}
                              </IconButton>
                            </InputAdornment>
                          ),
                        }}
                        sx={{ mb: 3 }}
                      />
                      <span>
                        <Button
                          fullWidth
                          variant="contained"
                          type="submit"
                          size="large"
                          disabled={isLoading}
                          sx={{ 
                            py: 1.5,
                            borderRadius: 2,
                            background: 'linear-gradient(45deg, #667eea, #764ba2)',
                            '&:hover': {
                              background: 'linear-gradient(45deg, #5a6fd8, #6a4190)'
                            }
                          }}
                        >
                          {isLoading ? (
                            <CircularProgress size={24} color="inherit" />
                          ) : (
                            'Login as User'
                          )}
                        </Button>
                      </span>
                    </form>
                  </Zoom>
                )}

                {activeTab === 1 && (
                  <Zoom in timeout={300}>
                    <form onSubmit={handleAdminLogin}>
                      <TextField
                        fullWidth
                        label="Username"
                        value={adminUsername}
                        onChange={(e) => setAdminUsername(e.target.value)}
                        margin="normal"
                        required
                        autoComplete="username"
                        disabled={isLoading}
                        InputProps={{
                          startAdornment: (
                            <InputAdornment position="start">
                              <AdminPanelSettings color="secondary" />
                            </InputAdornment>
                          ),
                        }}
                        sx={{ mb: 2 }}
                      />
                      <TextField
                        fullWidth
                        label="Password"
                        type={showPassword ? 'text' : 'password'}
                        value={adminPassword}
                        onChange={(e) => setAdminPassword(e.target.value)}
                        margin="normal"
                        required
                        autoComplete="current-password"
                        disabled={isLoading}
                        InputProps={{
                          startAdornment: (
                            <InputAdornment position="start">
                              <Lock color="secondary" />
                            </InputAdornment>
                          ),
                          endAdornment: (
                            <InputAdornment position="end">
                              <IconButton
                                onClick={() => setShowPassword(!showPassword)}
                                edge="end"
                                disabled={isLoading}
                              >
                                {showPassword ? <VisibilityOff /> : <Visibility />}
                              </IconButton>
                            </InputAdornment>
                          ),
                        }}
                        sx={{ mb: 3 }}
                      />
                      <span>
                        <Button
                          fullWidth
                          variant="contained"
                          color="secondary"
                          type="submit"
                          size="large"
                          disabled={isLoading}
                          sx={{ 
                            py: 1.5,
                            borderRadius: 2,
                            background: 'linear-gradient(45deg, #dc004e, #9c27b0)',
                            '&:hover': {
                              background: 'linear-gradient(45deg, #c5003e, #7b1fa2)'
                            }
                          }}
                        >
                          {isLoading ? (
                            <CircularProgress size={24} color="inherit" />
                          ) : (
                            'Login as Admin'
                          )}
                        </Button>
                      </span>
                    </form>
                  </Zoom>
                )}

                {activeTab === 2 && (
                  <Zoom in timeout={300}>
                    <form onSubmit={handleRegistration}>
                      <TextField
                        fullWidth
                        label="Username"
                        value={regUsername}
                        onChange={(e) => setRegUsername(e.target.value)}
                        margin="normal"
                        required
                        autoComplete="username"
                        disabled={isLoading}
                        InputProps={{
                          startAdornment: (
                            <InputAdornment position="start">
                              <PersonAdd color="success" />
                            </InputAdornment>
                          ),
                        }}
                        sx={{ mb: 2 }}
                      />
                      <TextField
                        fullWidth
                        label="Email"
                        type="email"
                        value={regEmail}
                        onChange={(e) => setRegEmail(e.target.value)}
                        margin="normal"
                        required
                        autoComplete="email"
                        disabled={isLoading}
                        InputProps={{
                          startAdornment: (
                            <InputAdornment position="start">
                              <Email color="success" />
                            </InputAdornment>
                          ),
                        }}
                        sx={{ mb: 2 }}
                      />
                      <TextField
                        fullWidth
                        label="Password"
                        type={showRegPassword ? 'text' : 'password'}
                        value={regPassword}
                        onChange={(e) => setRegPassword(e.target.value)}
                        margin="normal"
                        required
                        autoComplete="new-password"
                        disabled={isLoading}
                        InputProps={{
                          startAdornment: (
                            <InputAdornment position="start">
                              <Lock color="success" />
                            </InputAdornment>
                          ),
                          endAdornment: (
                            <InputAdornment position="end">
                              <IconButton
                                onClick={() => setShowRegPassword(!showRegPassword)}
                                edge="end"
                                disabled={isLoading}
                              >
                                {showRegPassword ? <VisibilityOff /> : <Visibility />}
                              </IconButton>
                            </InputAdornment>
                          ),
                        }}
                        sx={{ mb: 2 }}
                      />
                      <TextField
                        fullWidth
                        select
                        label="Role"
                        value={regRole}
                        onChange={(e) => setRegRole(e.target.value)}
                        margin="normal"
                        disabled={isLoading}
                        SelectProps={{
                          native: true,
                        }}
                        sx={{ mb: 3 }}
                      >
                        <option value="user">User</option>
                        <option value="admin">Admin</option>
                      </TextField>
                      <span>
                        <Button
                          fullWidth
                          variant="contained"
                          color="success"
                          type="submit"
                          size="large"
                          disabled={isLoading}
                          sx={{ 
                            py: 1.5,
                            borderRadius: 2,
                            background: 'linear-gradient(45deg, #4caf50, #2e7d32)',
                            '&:hover': {
                              background: 'linear-gradient(45deg, #43a047, #1b5e20)'
                            }
                          }}
                        >
                          {isLoading ? (
                            <CircularProgress size={24} color="inherit" />
                          ) : (
                            'Register'
                          )}
                        </Button>
                      </span>
                    </form>
                  </Zoom>
                )}

                <Divider sx={{ my: 3 }}>
                  <Typography variant="body2" color="text.secondary">
                    Demo Credentials
                  </Typography>
                </Divider>
                
                <Box sx={{ textAlign: 'center' }}>
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    <strong>User:</strong> user / user123
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    <strong>Admin:</strong> admin / admin123
                  </Typography>
                </Box>
              </Paper>
            </Zoom>
          </Box>
        </Fade>
      </Container>
    </Box>
  );
};

export default Login; 