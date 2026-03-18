import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import '../styles/Chatbot.css';

const API_BASE_URL = 'http://localhost:5000/api';

const Chatbot = () => {
  const userRole = localStorage.getItem('userRole');
  const welcomeMessage = userRole === 'candidate' 
    ? 'Hello! I am your Career Assistant. I can help you with job search, application tips, and interview preparation. How can I assist you today?'
    : 'Hello! I am your HR Assistant. How can I help you today?';
  
  const [messages, setMessages] = useState([
    { type: 'bot', text: welcomeMessage }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [faqs, setFaqs] = useState([]);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    fetchFAQs();
    seedFAQs();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const fetchFAQs = async () => {
    try {
      const token = localStorage.getItem('authToken');
      const response = await axios.get(`${API_BASE_URL}/chatbot/faqs`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setFaqs(response.data.faqs || []);
    } catch (error) {
      console.error('Error fetching FAQs:', error);
    }
  };

  const seedFAQs = async () => {
    try {
      const token = localStorage.getItem('authToken');
      await axios.post(`${API_BASE_URL}/chatbot/seed`, {}, {
        headers: { Authorization: `Bearer ${token}` }
      });
    } catch (error) {
      console.error('Error seeding FAQs:', error);
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!inputMessage.trim()) return;

    const userMessage = inputMessage.trim();
    setMessages([...messages, { type: 'user', text: userMessage }]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const token = localStorage.getItem('authToken');
      const response = await axios.post(
        `${API_BASE_URL}/chatbot/ask`,
        { message: userMessage },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      setMessages(prev => [...prev, { 
        type: 'bot', 
        text: response.data.answer,
        category: response.data.category 
      }]);
    } catch (error) {
      setMessages(prev => [...prev, { 
        type: 'bot', 
        text: 'Sorry, I encountered an error. Please try again.' 
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleQuickQuestion = (question) => {
    setInputMessage(question);
  };

  // Get quick questions based on user role
  const getQuickQuestions = () => {
    if (userRole === 'candidate') {
      return [
        { label: 'Available Jobs', question: 'What jobs are currently available?' },
        { label: 'Application Tips', question: 'How can I improve my job application?' },
        { label: 'Resume Help', question: 'What should I include in my resume?' },
        { label: 'Interview Tips', question: 'Can you give me interview preparation tips?' }
      ];
    } else {
      // HR role
      return [
        { label: 'Leave Policy', question: 'What is the leave policy?' },
        { label: 'Holidays', question: 'What are company holidays?' },
        { label: 'WFH Policy', question: 'Work from home policy?' },
        { label: 'Salary', question: 'When is salary paid?' }
      ];
    }
  };

  const quickQuestions = getQuickQuestions();

  return (
    <div className="chatbot-container">
      <div className="chatbot-header">
        <div className="header-content">
          <div className="bot-avatar">
            <i className="fas fa-robot"></i>
          </div>
          <div>
            <h2>{userRole === 'candidate' ? 'Career Assistant' : 'HR Assistant'}</h2>
            <p className="status">
              <span className="status-dot"></span>
              Online
            </p>
          </div>
        </div>
      </div>

      <div className="chatbot-body">
        <div className="messages-container">
          {messages.map((msg, index) => (
            <div key={index} className={`message ${msg.type}`}>
              {msg.type === 'bot' && (
                <div className="message-avatar">
                  <i className="fas fa-robot"></i>
                </div>
              )}
              <div className="message-content">
                <p>{msg.text}</p>
                {msg.category && (
                  <span className="message-category">{msg.category}</span>
                )}
              </div>
              {msg.type === 'user' && (
                <div className="message-avatar user">
                  <i className="fas fa-user"></i>
                </div>
              )}
            </div>
          ))}
          {isLoading && (
            <div className="message bot">
              <div className="message-avatar">
                <i className="fas fa-robot"></i>
              </div>
              <div className="message-content typing">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <div className="quick-questions">
          <h4>Quick Questions:</h4>
          <div className="quick-buttons">
            {quickQuestions.map((item, index) => (
              <button key={index} onClick={() => handleQuickQuestion(item.question)}>
                {item.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      <div className="chatbot-footer">
        <form onSubmit={handleSendMessage}>
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            placeholder="Type your question..."
            disabled={isLoading}
          />
          <button type="submit" disabled={isLoading || !inputMessage.trim()}>
            <i className="fas fa-paper-plane"></i>
          </button>
        </form>
      </div>
    </div>
  );
};

export default Chatbot;
