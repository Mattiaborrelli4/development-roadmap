import React from 'react';
import { ChatProvider, useChat } from './contexts/ChatContext';
import Login from './components/Login';
import ChatRoom from './components/ChatRoom';
import './App.css';

function AppContent() {
  const { user } = useChat();

  return user ? <ChatRoom /> : <Login />;
}

function App() {
  return (
    <ChatProvider>
      <AppContent />
    </ChatProvider>
  );
}

export default App;
