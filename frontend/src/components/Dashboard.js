import React, { useState, useRef, useEffect } from 'react';
import {
  Box,
  Typography,
  Container,
  AppBar,
  Toolbar,
  IconButton,
  Card,
  CardContent,
  Grid,
  Chip,
  Tooltip,
  TextField,
  Button,
  Paper,
  Avatar,
  Divider
} from '@mui/material';
import {
  Logout,
  AdminPanelSettings,
  SmartToy,
  Help,
  Settings,
  Work,
  Email,
  Event,
  Assignment,
  Send,
  Refresh
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const Dashboard = ({ onLogout, userRole }) => {
  const navigate = useNavigate();
  
  // Load chat state from localStorage or initialize empty
  const [messages, setMessages] = useState(() => {
    const savedMessages = localStorage.getItem('chatMessages');
    return savedMessages ? JSON.parse(savedMessages) : [];
  });
  
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Save messages to localStorage whenever they change
  useEffect(() => {
    localStorage.setItem('chatMessages', JSON.stringify(messages));
  }, [messages]);

  const sendMessage = async () => {
    if (!inputMessage.trim()) return;

    const userMessage = {
      text: inputMessage,
      sender: 'user',
      timestamp: new Date().toLocaleTimeString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:5005/webhooks/rest/webhook', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: inputMessage,
          sender: 'user'
        })
      });

      const data = await response.json();
      
      if (data && data.length > 0) {
        const botMessage = {
          text: data[0].text,
          sender: 'bot',
          timestamp: new Date().toLocaleTimeString()
        };
        setMessages(prev => [...prev, botMessage]);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        text: 'Sorry, I\'m having trouble connecting to the server. Please try again later.',
        sender: 'bot',
        timestamp: new Date().toLocaleTimeString()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      sendMessage();
    }
  };

  const clearChat = () => {
    setMessages([]);
    localStorage.removeItem('chatMessages');
  };

  const quickActions = [
    { text: 'Create timesheet', action: 'create a timesheet for today' },
    { text: 'Show timesheets', action: 'show my timesheets' },
    { text: 'Request leave', action: 'request leave for tomorrow' },
    { text: 'Create email', action: 'create an email to manager' },
    { text: 'Create task', action: 'create a new task' },
    { text: 'Help', action: 'help' }
  ];

  const handleQuickAction = (action) => {
    setInputMessage(action);
    setTimeout(() => sendMessage(), 100);
  };

  const features = [
    {
      icon: <Work sx={{ fontSize: 40, color: 'primary.main' }} />,
      title: 'Timesheets',
      description: 'Create and manage your work hours',
      color: '#667eea'
    },
    {
      icon: <Event sx={{ fontSize: 40, color: 'secondary.main' }} />,
      title: 'Leave Management',
      description: 'Request and track leave applications',
      color: '#764ba2'
    },
    {
      icon: <Email sx={{ fontSize: 40, color: 'success.main' }} />,
      title: 'Email Management',
      description: 'Compose and manage emails',
      color: '#4caf50'
    },
    {
      icon: <Assignment sx={{ fontSize: 40, color: 'warning.main' }} />,
      title: 'Task Management',
      description: 'Create and track tasks',
      color: '#ff9800'
    }
  ];

  const [timesheetForm, setTimesheetForm] = useState({
    user_id: '',
    email: '',
    date: '',
    from_time: '',
    to_time: '',
    task_summary: '',
    hours: '',
    description: '',
  });
  const [tsMessage, setTsMessage] = useState('');
  const handleTimesheetChange = (e) => {
    setTimesheetForm({ ...timesheetForm, [e.target.name]: e.target.value });
  };
  const handleTimesheetSubmit = async (e) => {
    e.preventDefault();
    setTsMessage('');
    try {
      const payload = {
        ...timesheetForm,
        hours: Number(timesheetForm.hours),
        date: timesheetForm.date, // YYYY-MM-DD
        from_time: timesheetForm.from_time, // HH:MM:SS
        to_time: timesheetForm.to_time, // HH:MM:SS
        submitted: false,
        approved_by: null
      };
      await axios.post('http://localhost:8000/timesheets/', payload);
      setTsMessage('Timesheet created successfully!');
      setTimesheetForm({
        user_id: '', email: '', date: '', from_time: '', to_time: '', task_summary: '', hours: '', description: ''
      });
    } catch (error) {
      setTsMessage('Error creating timesheet. Please check your input.');
    }
  };

  return (
    <Box sx={{ flexGrow: 1, height: '100vh', display: 'flex', flexDirection: 'column' }}>
      <AppBar 
        position="static" 
        sx={{ 
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          boxShadow: '0 4px 20px rgba(0,0,0,0.1)'
        }}
      >
        <Toolbar>
          <SmartToy sx={{ mr: 2, fontSize: 32 }} />
          <Typography variant="h6" component="div" sx={{ flexGrow: 1, fontWeight: 'bold' }}>
            AI Assistant Dashboard
          </Typography>
          
          <Tooltip title="Help">
            <IconButton color="inherit" sx={{ mr: 1 }}>
              <Help />
            </IconButton>
          </Tooltip>
          
          <Tooltip title="Settings">
            <IconButton color="inherit" sx={{ mr: 1 }}>
              <Settings />
            </IconButton>
          </Tooltip>
          
          {userRole === 'admin' && (
            <Tooltip title="Admin Panel">
              <IconButton
                color="inherit"
                onClick={() => navigate('/admin')}
                sx={{ mr: 1 }}
              >
                <AdminPanelSettings />
              </IconButton>
            </Tooltip>
          )}
          
          <Tooltip title="Logout">
            <IconButton color="inherit" onClick={onLogout}>
              <Logout />
            </IconButton>
          </Tooltip>
        </Toolbar>
      </AppBar>

      <Container maxWidth="xl" sx={{ flexGrow: 1, py: 2 }}>
        <Grid container spacing={3} sx={{ height: '100%' }}>
          {/* Left Side - Features Overview */}
          <Grid item xs={12} md={4}>
            <Card sx={{ height: '100%', borderRadius: 3, boxShadow: '0 4px 20px rgba(0,0,0,0.1)' }}>
              <CardContent sx={{ p: 3 }}>
                <Typography variant="h5" sx={{ fontWeight: 'bold', mb: 3, color: 'primary.main' }}>
                  Welcome! 🤖
                </Typography>
                
                <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
                  I can help you with:
                </Typography>

                <Grid container spacing={2} sx={{ mb: 3 }}>
                  {features.map((feature, index) => (
                    <Grid item xs={6} key={index}>
                      <Card 
                        sx={{ 
                          p: 2,
                          borderRadius: 2,
                          boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
                          transition: 'transform 0.2s',
                          '&:hover': {
                            transform: 'translateY(-2px)'
                          }
                        }}
                      >
                        <Box sx={{ textAlign: 'center' }}>
                          {feature.icon}
                          <Typography variant="body2" sx={{ fontWeight: 'bold', mt: 1 }}>
                            {feature.title}
                          </Typography>
                        </Box>
                      </Card>
                    </Grid>
                  ))}
                </Grid>

                <Divider sx={{ my: 2 }} />

                <Typography variant="h6" sx={{ fontWeight: 'bold', mb: 2 }}>
                  Quick Actions
                </Typography>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                  {quickActions.map((action, index) => (
                    <Chip
                      key={index}
                      label={action.text}
                      onClick={() => handleQuickAction(action.action)}
                      sx={{ 
                        cursor: 'pointer',
                        '&:hover': {
                          backgroundColor: 'primary.light',
                          color: 'white'
                        }
                      }}
                    />
                  ))}
                </Box>
                {/* Timesheet Creation Form */}
                <Box sx={{ mt: 4 }}>
                  <Typography variant="h6" sx={{ fontWeight: 'bold', mb: 2 }}>
                    Create Timesheet
                  </Typography>
                  <form onSubmit={handleTimesheetSubmit}>
                    <Grid container spacing={1}>
                      <Grid item xs={12}><TextField label="User ID" name="user_id" value={timesheetForm.user_id} onChange={handleTimesheetChange} fullWidth required /></Grid>
                      <Grid item xs={12}><TextField label="Email" name="email" value={timesheetForm.email} onChange={handleTimesheetChange} fullWidth required /></Grid>
                      <Grid item xs={12}><TextField label="Date" name="date" type="date" value={timesheetForm.date} onChange={handleTimesheetChange} fullWidth required InputLabelProps={{ shrink: true }} /></Grid>
                      <Grid item xs={6}><TextField label="From Time" name="from_time" type="time" value={timesheetForm.from_time} onChange={handleTimesheetChange} fullWidth required InputLabelProps={{ shrink: true }} /></Grid>
                      <Grid item xs={6}><TextField label="To Time" name="to_time" type="time" value={timesheetForm.to_time} onChange={handleTimesheetChange} fullWidth required InputLabelProps={{ shrink: true }} /></Grid>
                      <Grid item xs={12}><TextField label="Task Summary" name="task_summary" value={timesheetForm.task_summary} onChange={handleTimesheetChange} fullWidth required /></Grid>
                      <Grid item xs={6}><TextField label="Hours" name="hours" type="number" value={timesheetForm.hours} onChange={handleTimesheetChange} fullWidth required /></Grid>
                      <Grid item xs={12}><TextField label="Description" name="description" value={timesheetForm.description} onChange={handleTimesheetChange} fullWidth multiline rows={2} /></Grid>
                      <Grid item xs={12}><Button type="submit" variant="contained" color="primary" fullWidth>Create Timesheet</Button></Grid>
                      {tsMessage && <Grid item xs={12}><Typography color={tsMessage.includes('success') ? 'green' : 'red'}>{tsMessage}</Typography></Grid>}
                    </Grid>
                  </form>
                </Box>
              </CardContent>
            </Card>
          </Grid>

          {/* Right Side - Chat Interface */}
          <Grid item xs={12} md={8}>
            <Card sx={{ height: '100%', borderRadius: 3, boxShadow: '0 4px 20px rgba(0,0,0,0.1)' }}>
              <CardContent sx={{ p: 0, height: '100%', display: 'flex', flexDirection: 'column' }}>
                {/* Chat Header */}
                <Box sx={{ 
                  p: 3, 
                  borderBottom: '1px solid #e0e0e0',
                  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                  color: 'white',
                  borderRadius: '12px 12px 0 0'
                }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                      <Avatar sx={{ mr: 2, bgcolor: 'rgba(255,255,255,0.2)' }}>
                        <SmartToy />
                      </Avatar>
                      <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
                        AI Assistant Chat
                      </Typography>
                    </Box>
                    <Tooltip title="Clear Chat">
                      <IconButton onClick={clearChat} sx={{ color: 'white' }}>
                        <Refresh />
                      </IconButton>
                    </Tooltip>
                  </Box>
                </Box>

                {/* Chat Messages */}
                <Box sx={{ 
                  flexGrow: 1, 
                  overflow: 'auto', 
                  p: 3,
                  minHeight: '400px',
                  maxHeight: '60vh'
                }}>
                  {messages.length === 0 && (
                    <Box sx={{ textAlign: 'center', py: 8 }}>
                      <SmartToy sx={{ fontSize: 80, color: 'primary.main', mb: 2, opacity: 0.7 }} />
                      <Typography variant="h6" color="text.secondary" gutterBottom>
                        Welcome to AI Assistant! 🤖
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        I can help you with timesheets, leave applications, emails, and tasks.
                      </Typography>
                    </Box>
                  )}
                  
                  {messages.map((message, index) => (
                    <Box
                      key={index}
                      sx={{
                        display: 'flex',
                        justifyContent: message.sender === 'user' ? 'flex-end' : 'flex-start',
                        mb: 2,
                      }}
                    >
                      <Box sx={{ display: 'flex', alignItems: 'flex-start', maxWidth: '70%' }}>
                        {message.sender === 'bot' && (
                          <Avatar sx={{ mr: 1, bgcolor: 'primary.main' }}>
                            <SmartToy />
                          </Avatar>
                        )}
                        <Paper
                          elevation={2}
                          sx={{
                            p: 2,
                            borderRadius: 3,
                            backgroundColor: message.sender === 'user' 
                              ? 'primary.main' 
                              : 'grey.100',
                            color: message.sender === 'user' ? 'white' : 'text.primary',
                            maxWidth: '100%',
                            wordBreak: 'break-word'
                          }}
                        >
                          <Typography variant="body1" sx={{ whiteSpace: 'pre-line' }}>
                            {message.text}
                          </Typography>
                          <Typography variant="caption" sx={{ opacity: 0.7, mt: 1, display: 'block' }}>
                            {message.timestamp}
                          </Typography>
                        </Paper>
                        {message.sender === 'user' && (
                          <Avatar sx={{ ml: 1, bgcolor: 'secondary.main' }}>
                            👤
                          </Avatar>
                        )}
                      </Box>
                    </Box>
                  ))}
                  
                  {isLoading && (
                    <Box sx={{ display: 'flex', justifyContent: 'flex-start', mb: 2 }}>
                      <Box sx={{ display: 'flex', alignItems: 'flex-start' }}>
                        <Avatar sx={{ mr: 1, bgcolor: 'primary.main' }}>
                          <SmartToy />
                        </Avatar>
                        <Paper sx={{ p: 2, borderRadius: 3, backgroundColor: 'grey.100' }}>
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                            <Typography variant="body2" color="text.secondary">
                              AI is typing
                            </Typography>
                            <Box sx={{ display: 'flex', gap: 0.5 }}>
                              <Box sx={{ width: 4, height: 4, borderRadius: '50%', bgcolor: 'primary.main', animation: 'pulse 1s infinite' }} />
                              <Box sx={{ width: 4, height: 4, borderRadius: '50%', bgcolor: 'primary.main', animation: 'pulse 1s infinite 0.2s' }} />
                              <Box sx={{ width: 4, height: 4, borderRadius: '50%', bgcolor: 'primary.main', animation: 'pulse 1s infinite 0.4s' }} />
                            </Box>
                          </Box>
                        </Paper>
                      </Box>
                    </Box>
                  )}
                  <div ref={messagesEndRef} />
                </Box>

                {/* Chat Input */}
                <Box sx={{ p: 3, borderTop: '1px solid #e0e0e0' }}>
                  <Box sx={{ display: 'flex', gap: 2 }}>
                    <TextField
                      fullWidth
                      multiline
                      maxRows={3}
                      value={inputMessage}
                      onChange={(e) => setInputMessage(e.target.value)}
                      onKeyPress={handleKeyPress}
                      placeholder="Type your message here... 💬"
                      disabled={isLoading}
                      sx={{
                        '& .MuiOutlinedInput-root': {
                          borderRadius: 3,
                          backgroundColor: 'white'
                        }
                      }}
                    />
                    <Button
                      variant="contained"
                      onClick={sendMessage}
                      disabled={!inputMessage.trim() || isLoading}
                      sx={{
                        borderRadius: 3,
                        px: 3,
                        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                        '&:hover': {
                          background: 'linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%)'
                        }
                      }}
                    >
                      <Send />
                    </Button>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
};

export default Dashboard; 