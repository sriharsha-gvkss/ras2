import React, { useState, useEffect, useRef } from 'react';
import './ChatBot.css';

const ChatBot = ({ 
  messages = [], 
  inputMessage = '', 
  onAddMessage, 
  onClearChat, 
  onUpdateInput 
}) => {
  const [isLoading, setIsLoading] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!inputMessage.trim()) return;

    const userMessage = {
      text: inputMessage,
      sender: 'user',
      timestamp: new Date().toLocaleTimeString()
    };

    onAddMessage(userMessage);
    onUpdateInput('');
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
        onAddMessage(botMessage);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        text: 'Sorry, I\'m having trouble connecting to the server. Please try again later.',
        sender: 'bot',
        timestamp: new Date().toLocaleTimeString()
      };
      onAddMessage(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      sendMessage();
    }
  };

  const toggleChat = () => {
    setIsOpen(!isOpen);
    if (!isOpen && messages.length === 0) {
      // Send welcome message
      const welcomeMessage = {
        text: 'Hello! I\'m your AI assistant. I can help you with:\n\n📊 Timesheets\n🏖️ Leave Management\n📧 Email Management\n📋 Task Management\n\nHow can I assist you today?',
        sender: 'bot',
        timestamp: new Date().toLocaleTimeString()
      };
      onAddMessage(welcomeMessage);
    }
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
    onUpdateInput(action);
    setTimeout(() => {
      const userMessage = {
        text: action,
        sender: 'user',
        timestamp: new Date().toLocaleTimeString()
      };
      onAddMessage(userMessage);
      onUpdateInput('');
      sendMessage();
    }, 100);
  };

  return (
    <div className="chatbot-container">
      {/* Chat Toggle Button */}
      <button 
        className="chatbot-toggle"
        onClick={toggleChat}
        title="Chat with AI Assistant"
      >
        {isOpen ? '✕' : '🤖'}
      </button>

      {/* Chat Window */}
      {isOpen && (
        <div className="chatbot-window">
          <div className="chatbot-header">
            <h3>AI Assistant</h3>
            <button onClick={toggleChat} className="close-btn">✕</button>
          </div>

          <div className="chatbot-messages">
            {messages.map((message, index) => (
              <div 
                key={index} 
                className={`message ${message.sender === 'user' ? 'user-message' : 'bot-message'}`}
              >
                <div className="message-content">
                  {message.text.split('\n').map((line, i) => (
                    <div key={i}>{line}</div>
                  ))}
                </div>
                <div className="message-timestamp">{message.timestamp}</div>
              </div>
            ))}
            {isLoading && (
              <div className="message bot-message">
                <div className="message-content">
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Quick Actions */}
          {messages.length === 1 && (
            <div className="quick-actions">
              <h4>Quick Actions:</h4>
              <div className="quick-actions-grid">
                {quickActions.map((action, index) => (
                  <button
                    key={index}
                    className="quick-action-btn"
                    onClick={() => handleQuickAction(action.action)}
                  >
                    {action.text}
                  </button>
                ))}
              </div>
            </div>
          )}

          <div className="chatbot-input">
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => onUpdateInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your message..."
              disabled={isLoading}
            />
            <button 
              onClick={sendMessage}
              disabled={isLoading || !inputMessage.trim()}
              className="send-btn"
            >
              ➤
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatBot; 