# AI Assistant Frontend

A React-based frontend application that provides a chat interface to interact with an AI assistant powered by OpenAI and Rasa.

## Features

- **User Dashboard**: Chat interface with AI assistant
- **Admin Panel**: Management interface for leaves, timesheets, and emails
- **OpenAI Integration**: Natural language processing for user input
- **Rasa Bot Integration**: Backend processing and actions
- **Material-UI**: Modern, responsive design

## Prerequisites

- Node.js (v14 or higher)
- npm or yarn
- Backend server running on `http://localhost:8000`
- Rasa server running on `http://localhost:5005`
- OpenAI API key

## Installation

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

The application will open at `http://localhost:3000`.

## Usage

### User Login
- Use any username and password to login as a regular user
- Access the chat dashboard to interact with the AI assistant

### Admin Login
- Use any username and password to login as an admin
- Access both the chat dashboard and admin panel
- Manage leave requests, timesheets, and view email history

### Chat Interface
- Type natural language requests
- The system will:
  1. Process your input with OpenAI to understand intent
  2. Format the request for the Rasa bot
  3. Execute actions through the backend
  4. Display results in the chat

### Admin Panel
- **Pending Leaves**: Review and approve/reject leave requests
- **Approved Leaves**: View approved leave history
- **Pending Timesheets**: Review and approve/reject timesheet submissions
- **Approved Timesheets**: View approved timesheet history
- **Emails**: View email history

## API Integration

### OpenAI API
- Processes natural language input
- Extracts intent and entities
- Formats requests for Rasa bot

### Rasa Bot
- Handles conversation flow
- Executes custom actions
- Manages form filling

### Backend API
- Stores and retrieves data
- Handles business logic
- Manages approvals and status updates

## Available Commands

Users can interact with the AI assistant using natural language:

- **Leave Management**:
  - "I want to apply for sick leave"
  - "Apply for casual leave"
  - "Show my leave history"

- **Timesheet Management**:
  - "Submit my timesheet"
  - "Check my timesheet status"
  - "I worked from 9 AM to 5 PM today"

- **Email Management**:
  - "Send an email to john@example.com"
  - "I want to send an email from me@company.com to you@company.com"

- **General**:
  - "Hello" / "Hi"
  - "Goodbye" / "Bye"

## Configuration

### Environment Variables
Create a `.env` file in the frontend directory:

```env
REACT_APP_OPENAI_API_KEY=your_openai_api_key_here
REACT_APP_BACKEND_URL=http://localhost:8000
REACT_APP_RASA_URL=http://localhost:5005
```

### API Endpoints
- Backend: `http://localhost:8000`
- Rasa: `http://localhost:5005`
- OpenAI: `https://api.openai.com/v1`

## Development

### Project Structure
```
src/
├── components/
│   ├── Dashboard.js      # Main chat interface
│   ├── AdminPanel.js     # Admin management interface
│   └── Login.js          # Authentication component
├── App.js               # Main application component
├── App.css              # Global styles
└── index.js             # Application entry point
```

### Key Components

#### Dashboard
- Chat interface with message history
- OpenAI integration for natural language processing
- Rasa bot communication
- Real-time message updates

#### AdminPanel
- Tabbed interface for different data types
- Approval workflows for leaves and timesheets
- Data management and status updates
- Real-time data refresh

#### Login
- Simple authentication interface
- Role-based access control
- User and admin login options

## Troubleshooting

### Common Issues

1. **Backend Connection Error**:
   - Ensure the backend server is running on port 8000
   - Check CORS configuration

2. **Rasa Connection Error**:
   - Ensure Rasa server is running on port 5005
   - Check action server is running

3. **OpenAI API Error**:
   - Verify API key is correct
   - Check API quota and billing

4. **Build Errors**:
   - Clear node_modules and reinstall dependencies
   - Check for version conflicts

### Debug Mode
Enable debug logging by setting:
```javascript
localStorage.setItem('debug', 'true');
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.
