# AI Assistant Portal

A modern, full-stack AI Assistant application with authentication, chat interface, and backend integration. Built with React, FastAPI, and Material-UI.

## ✨ Features

- **🔐 Secure Authentication**: JWT-based authentication with user/admin roles
- **💬 AI Chat Interface**: Modern chat UI with typing indicators and animations
- **🤖 OpenAI Integration**: Smart responses with fallback processing
- **🎨 Modern UI/UX**: Beautiful gradient design with smooth animations
- **📱 Responsive Design**: Works on desktop and mobile devices
- **🔧 Backend API**: FastAPI backend with authentication and data management
- **📊 Admin Panel**: Admin-specific features and controls

## 🚀 Quick Start

### Prerequisites

- Node.js (v16 or higher)
- Python (v3.8 or higher)
- npm or yarn

### 1. Clone and Setup

```bash
git clone <repository-url>
cd ai-assistant-portal
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at `http://localhost:8000`

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create environment file
cp env.example .env

# Start the development server
npm start
```

The frontend will be available at `http://localhost:3000`

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the `frontend` directory:

```env
# OpenAI API Configuration (optional)
REACT_APP_OPENAI_API_KEY=your_openai_api_key_here

# Backend API URL
REACT_APP_BACKEND_URL=http://localhost:8000

# Rasa Bot URL
REACT_APP_RASA_URL=http://localhost:5005
```

### Demo Credentials

- **User**: `user` / `user123`
- **Admin**: `admin` / `admin123`

## 🎨 UI Improvements

### Modern Design Features

- **Gradient Backgrounds**: Beautiful purple-blue gradients throughout the app
- **Glass Morphism**: Translucent cards with backdrop blur effects
- **Smooth Animations**: Fade, zoom, and slide animations for better UX
- **Interactive Elements**: Hover effects and micro-interactions
- **Responsive Layout**: Mobile-friendly design with adaptive components

### Enhanced Components

- **Login Page**: Modern authentication with tabbed interface
- **Chat Interface**: Professional chat UI with typing indicators
- **Navigation**: Clean app bar with tooltips and icons
- **Loading States**: Spinners and progress indicators
- **Error Handling**: User-friendly error messages and fallbacks

## 🔐 Authentication System

### Features

- **JWT Tokens**: Secure token-based authentication
- **Role-based Access**: User and admin role management
- **Token Storage**: Secure localStorage token management
- **Auto-logout**: Token expiration handling
- **Protected Routes**: Route protection based on authentication status

### API Endpoints

- `POST /auth/login` - User login
- `POST /auth/register` - User registration
- `GET /auth/me` - Get current user info
- `GET /auth/validate` - Validate token

## 🤖 AI Integration

### OpenAI Integration

- **Smart Responses**: Context-aware AI responses
- **Rate Limiting**: Graceful handling of API limits
- **Fallback Processing**: Local keyword-based responses when API is unavailable
- **Environment Configuration**: Optional API key setup

### Chat Features

- **Real-time Chat**: Instant message exchange
- **Typing Indicators**: Visual feedback during AI processing
- **Message History**: Persistent chat history
- **Rich Responses**: Emoji and formatted text support
- **Error Recovery**: Graceful error handling and retry mechanisms

## 📁 Project Structure

```
ai-assistant-portal/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models/
│   │   ├── routes/
│   │   │   ├── auth.py
│   │   │   ├── emails.py
│   │   │   ├── jobs.py
│   │   │   ├── leaves.py
│   │   │   ├── tasks.py
│   │   │   └── timesheet.py
│   │   └── schemas/
│   ├── requirements.txt
│   └── README.md
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Login.js
│   │   │   ├── Dashboard.js
│   │   │   └── AdminPanel.js
│   │   ├── App.js
│   │   ├── App.css
│   │   └── index.js
│   ├── package.json
│   ├── env.example
│   └── README.md
├── rasa_bot/
│   ├── actions/
│   ├── data/
│   ├── config.yml
│   └── requirements.txt
└── README.md
```

## 🛠️ Development

### Backend Development

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development

```bash
cd frontend
npm start
```

### API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation.

## 🚀 Deployment

### Backend Deployment

1. Set up a production database
2. Configure environment variables
3. Use a production WSGI server (Gunicorn)
4. Set up reverse proxy (Nginx)

### Frontend Deployment

1. Build the production version: `npm run build`
2. Deploy to a static hosting service (Netlify, Vercel, etc.)
3. Configure environment variables

## 🔧 Troubleshooting

### Common Issues

1. **Backend Connection Error**: Ensure the backend is running on port 8000
2. **OpenAI Rate Limits**: The app will use fallback responses automatically
3. **Authentication Issues**: Check if JWT tokens are properly stored
4. **CORS Errors**: Backend CORS is configured for development

### Debug Mode

Enable debug logging by setting environment variables:

```env
DEBUG=true
LOG_LEVEL=debug
```

## 📝 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For support and questions, please open an issue on GitHub.

---

**Enjoy using the AI Assistant Portal! 🚀** 