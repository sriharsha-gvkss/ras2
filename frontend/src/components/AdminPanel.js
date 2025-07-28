import React, { useState, useEffect } from 'react';
import {
  Box,
  AppBar,
  Toolbar,
  Typography,
  IconButton,
  Container,
  Tabs,
  Tab,
  Card,
  CardContent,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Chip,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Grid,
  Alert,
  CircularProgress,
} from '@mui/material';
import {
  Logout,
  Dashboard as DashboardIcon,
  Email,
  Work,
  Person,
  CheckCircle,
  Pending,
  Refresh,
  AdminPanelSettings,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const AdminPanel = ({ onLogout }) => {
  const [activeTab, setActiveTab] = useState(0);
  const [leaves, setLeaves] = useState([]);
  const [timesheets, setTimesheets] = useState([]);
  const [emails, setEmails] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [approvalDialog, setApprovalDialog] = useState({ open: false, item: null, type: '' });
  const [approvalComment, setApprovalComment] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const fetchData = async () => {
    setLoading(true);
    setError('');
    
    try {
      // Fetch all data in parallel
      const [leavesResponse, timesheetsResponse, emailsResponse, tasksResponse] = await Promise.all([
        axios.get('http://localhost:8000/leaves/'),
        axios.get('http://localhost:8000/timesheets/'),
        axios.get('http://localhost:8000/emails/'),
        axios.get('http://localhost:8000/tasks/')
      ]);

      setLeaves(leavesResponse.data || []);
      setTimesheets(timesheetsResponse.data || []);
      setEmails(emailsResponse.data || []);
      setTasks(tasksResponse.data || []);
    } catch (error) {
      console.error('Error fetching data:', error);
      setError('Failed to fetch data. Please check if the backend server is running on http://localhost:8000');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };

  const handleApproval = async (item, type, status) => {
    setApprovalDialog({ open: true, item, type, status });
  };

  const confirmApproval = async () => {
    try {
      const { item, type, status } = approvalDialog;
      
      let endpoint = '';
      if (type === 'leave') {
        // For leaves, update the status
        const updateData = {
          status: status,
          approved_by: 'admin',
          approval_comment: approvalComment
        };
        endpoint = `http://localhost:8000/leaves/${item.id}`;
        await axios.put(endpoint, updateData);
      } else if (type === 'timesheet') {
        if (status === 'approved') {
          // For timesheets, use the approve endpoint
          endpoint = `http://localhost:8000/timesheets/${item.id}/approve`;
          await axios.post(endpoint, null, {
            params: { approver: 'admin' }
          });
        } else if (status === 'rejected') {
          // For rejection, we need to add a reject endpoint or update the timesheet
          const updateData = {
            submitted: false,
            approved_by: 'admin',
            status: 'rejected'
          };
          endpoint = `http://localhost:8000/timesheets/${item.id}`;
          await axios.put(endpoint, updateData);
        }
      }
      
      setApprovalDialog({ open: false, item: null, type: '' });
      setApprovalComment('');
      fetchData(); // Refresh data
    } catch (error) {
      console.error('Error updating item:', error);
      setError('Failed to update item. Please try again.');
    }
  };

  const getStatusColor = (status) => {
    switch (status?.toLowerCase()) {
      case 'approved':
        return 'success';
      case 'pending':
        return 'warning';
      case 'rejected':
        return 'error';
      default:
        return 'default';
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    try {
      return new Date(dateString).toLocaleDateString();
    } catch {
      return dateString;
    }
  };

  const pendingLeaves = leaves.filter(leave => leave.status?.toLowerCase() === 'pending');
  const approvedLeaves = leaves.filter(leave => leave.status?.toLowerCase() === 'approved');
  const pendingTimesheets = timesheets.filter(ts => !ts.submitted);
  const approvedTimesheets = timesheets.filter(ts => ts.submitted);

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ flexGrow: 1, height: '100vh', display: 'flex', flexDirection: 'column' }}>
      <AppBar position="static">
        <Toolbar>
          <AdminPanelSettings sx={{ mr: 2 }} />
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Admin Panel
          </Typography>
          <IconButton
            color="inherit"
            onClick={() => navigate('/dashboard')}
            sx={{ mr: 1 }}
          >
            <DashboardIcon />
          </IconButton>
          <IconButton color="inherit" onClick={onLogout}>
            <Logout />
          </IconButton>
        </Toolbar>
      </AppBar>

      <Container maxWidth="xl" sx={{ flexGrow: 1, py: 2 }}>
        <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 2 }}>
          <Tabs value={activeTab} onChange={handleTabChange} aria-label="admin tabs">
            <Tab label={`Pending Leaves (${pendingLeaves.length})`} />
            <Tab label={`Approved Leaves (${approvedLeaves.length})`} />
            <Tab label={`Pending Timesheets (${pendingTimesheets.length})`} />
            <Tab label={`Approved Timesheets (${approvedTimesheets.length})`} />
            <Tab label={`Emails (${emails.length})`} />
            <Tab label={`Tasks (${tasks.length})`} />
          </Tabs>
        </Box>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        <Box sx={{ display: 'flex', justifyContent: 'flex-end', mb: 2 }}>
          <Button
            variant="outlined"
            startIcon={<Refresh />}
            onClick={fetchData}
            disabled={loading}
          >
            Refresh
          </Button>
        </Box>

        {activeTab === 0 && (
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Pending Leave Requests
              </Typography>
              {pendingLeaves.length === 0 ? (
                <Typography color="text.secondary">No pending leave requests</Typography>
              ) : (
                <TableContainer component={Paper}>
                  <Table>
                    <TableHead>
                      <TableRow>
                        <TableCell>Employee</TableCell>
                        <TableCell>Leave Type</TableCell>
                        <TableCell>Date</TableCell>
                        <TableCell>Reason</TableCell>
                        <TableCell>Status</TableCell>
                        <TableCell>Actions</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {pendingLeaves.map((leave) => (
                        <TableRow key={leave.id}>
                          <TableCell>{leave.user_id || leave.username || 'Unknown'}</TableCell>
                          <TableCell>{leave.leave_type}</TableCell>
                          <TableCell>{formatDate(leave.date)}</TableCell>
                          <TableCell>{leave.reason}</TableCell>
                          <TableCell>
                            <Chip
                              label={leave.status}
                              color={getStatusColor(leave.status)}
                              size="small"
                            />
                          </TableCell>
                          <TableCell>
                            <Button
                              size="small"
                              color="success"
                              onClick={() => handleApproval(leave, 'leave', 'approved')}
                              sx={{ mr: 1 }}
                            >
                              Approve
                            </Button>
                            <Button
                              size="small"
                              color="error"
                              onClick={() => handleApproval(leave, 'leave', 'rejected')}
                            >
                              Reject
                            </Button>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              )}
            </CardContent>
          </Card>
        )}

        {activeTab === 1 && (
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Approved Leave Requests
              </Typography>
              {approvedLeaves.length === 0 ? (
                <Typography color="text.secondary">No approved leave requests</Typography>
              ) : (
                <TableContainer component={Paper}>
                  <Table>
                    <TableHead>
                      <TableRow>
                        <TableCell>Employee</TableCell>
                        <TableCell>Leave Type</TableCell>
                        <TableCell>Date</TableCell>
                        <TableCell>Reason</TableCell>
                        <TableCell>Status</TableCell>
                        <TableCell>Approved By</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {approvedLeaves.map((leave) => (
                        <TableRow key={leave.id}>
                          <TableCell>{leave.user_id || leave.username || 'Unknown'}</TableCell>
                          <TableCell>{leave.leave_type}</TableCell>
                          <TableCell>{formatDate(leave.date)}</TableCell>
                          <TableCell>{leave.reason}</TableCell>
                          <TableCell>
                            <Chip
                              label={leave.status}
                              color={getStatusColor(leave.status)}
                              size="small"
                            />
                          </TableCell>
                          <TableCell>{leave.approved_by || 'Admin'}</TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              )}
            </CardContent>
          </Card>
        )}

        {activeTab === 2 && (
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Pending Timesheets
              </Typography>
              {pendingTimesheets.length === 0 ? (
                <Typography color="text.secondary">No pending timesheets</Typography>
              ) : (
                <TableContainer component={Paper}>
                  <Table>
                    <TableHead>
                      <TableRow>
                        <TableCell>Employee</TableCell>
                        <TableCell>Date</TableCell>
                        <TableCell>From Time</TableCell>
                        <TableCell>To Time</TableCell>
                        <TableCell>Task Summary</TableCell>
                        <TableCell>Status</TableCell>
                        <TableCell>Actions</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {pendingTimesheets.map((timesheet) => (
                        <TableRow key={timesheet.id}>
                          <TableCell>{timesheet.user_id}</TableCell>
                          <TableCell>{formatDate(timesheet.date)}</TableCell>
                          <TableCell>{timesheet.from_time}</TableCell>
                          <TableCell>{timesheet.to_time}</TableCell>
                          <TableCell>{timesheet.task_summary}</TableCell>
                          <TableCell>
                            <Chip
                              label={timesheet.submitted ? "Approved" : "Pending"}
                              color={timesheet.submitted ? "success" : "warning"}
                              size="small"
                            />
                          </TableCell>
                          <TableCell>
                            <Button
                              size="small"
                              color="success"
                              onClick={() => handleApproval(timesheet, 'timesheet', 'approved')}
                              sx={{ mr: 1 }}
                            >
                              Approve
                            </Button>
                            <Button
                              size="small"
                              color="error"
                              onClick={() => handleApproval(timesheet, 'timesheet', 'rejected')}
                            >
                              Reject
                            </Button>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              )}
            </CardContent>
          </Card>
        )}

        {activeTab === 3 && (
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Approved Timesheets
              </Typography>
              {approvedTimesheets.length === 0 ? (
                <Typography color="text.secondary">No approved timesheets</Typography>
              ) : (
                <TableContainer component={Paper}>
                  <Table>
                    <TableHead>
                      <TableRow>
                        <TableCell>Employee</TableCell>
                        <TableCell>Date</TableCell>
                        <TableCell>From Time</TableCell>
                        <TableCell>To Time</TableCell>
                        <TableCell>Task Summary</TableCell>
                        <TableCell>Status</TableCell>
                        <TableCell>Approved By</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {approvedTimesheets.map((timesheet) => (
                        <TableRow key={timesheet.id}>
                          <TableCell>{timesheet.user_id}</TableCell>
                          <TableCell>{formatDate(timesheet.date)}</TableCell>
                          <TableCell>{timesheet.from_time}</TableCell>
                          <TableCell>{timesheet.to_time}</TableCell>
                          <TableCell>{timesheet.task_summary}</TableCell>
                          <TableCell>
                            <Chip
                              label={timesheet.submitted ? "Approved" : "Pending"}
                              color={timesheet.submitted ? "success" : "warning"}
                              size="small"
                            />
                          </TableCell>
                          <TableCell>{timesheet.approved_by || 'Admin'}</TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              )}
            </CardContent>
          </Card>
        )}

        {activeTab === 4 && (
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Email History
              </Typography>
              {emails.length === 0 ? (
                <Typography color="text.secondary">No emails found</Typography>
              ) : (
                <TableContainer component={Paper}>
                  <Table>
                    <TableHead>
                      <TableRow>
                        <TableCell>From</TableCell>
                        <TableCell>To</TableCell>
                        <TableCell>Subject</TableCell>
                        <TableCell>Date</TableCell>
                        <TableCell>Status</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {emails.map((email) => (
                        <TableRow key={email.id}>
                          <TableCell>{email.user_id || email.from_user || 'Unknown'}</TableCell>
                          <TableCell>{email.recipient || email.to_user || 'Unknown'}</TableCell>
                          <TableCell>{email.subject}</TableCell>
                          <TableCell>{formatDate(email.date)}</TableCell>
                          <TableCell>
                            <Chip
                              label={email.status}
                              color={getStatusColor(email.status)}
                              size="small"
                            />
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              )}
            </CardContent>
          </Card>
        )}

        {activeTab === 5 && (
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Task Management
              </Typography>
              {tasks.length === 0 ? (
                <Typography color="text.secondary">No tasks found</Typography>
              ) : (
                <TableContainer component={Paper}>
                  <Table>
                    <TableHead>
                      <TableRow>
                        <TableCell>Employee</TableCell>
                        <TableCell>Title</TableCell>
                        <TableCell>Description</TableCell>
                        <TableCell>Priority</TableCell>
                        <TableCell>Status</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {tasks.map((task) => (
                        <TableRow key={task.id}>
                          <TableCell>{task.user_id}</TableCell>
                          <TableCell>{task.title}</TableCell>
                          <TableCell>{task.description}</TableCell>
                          <TableCell>
                            <Chip
                              label={task.priority}
                              color={task.priority === 'High' ? 'error' : task.priority === 'Medium' ? 'warning' : 'success'}
                              size="small"
                            />
                          </TableCell>
                          <TableCell>
                            <Chip
                              label={task.status}
                              color={getStatusColor(task.status)}
                              size="small"
                            />
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              )}
            </CardContent>
          </Card>
        )}
      </Container>

      {/* Approval Dialog */}
      <Dialog open={approvalDialog.open} onClose={() => setApprovalDialog({ open: false, item: null, type: '' })}>
        <DialogTitle>
          {approvalDialog.status === 'approved' ? 'Approve' : 'Reject'} {approvalDialog.type}
        </DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            multiline
            rows={3}
            label="Comment (optional)"
            value={approvalComment}
            onChange={(e) => setApprovalComment(e.target.value)}
            sx={{ mt: 1 }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setApprovalDialog({ open: false, item: null, type: '' })}>
            Cancel
          </Button>
          <Button
            onClick={confirmApproval}
            color={approvalDialog.status === 'approved' ? 'success' : 'error'}
            variant="contained"
          >
            {approvalDialog.status === 'approved' ? 'Approve' : 'Reject'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default AdminPanel; 