import React from 'react';
import { useChat } from '../contexts/ChatContext';
import RoomList from './RoomList';
import UserList from './UserList';
import MessageList from './MessageList';
import MessageInput from './MessageInput';
import './ChatRoom.css';

export default function ChatRoom() {
  const { user, logout, currentRoom } = useChat();

  return (
    <div className="chat-room">
      <div className="chat-layout">
        {/* Sidebar sinistra - Lista stanze */}
        <aside className="sidebar left-sidebar">
          <RoomList />
        </aside>

        {/* Area principale - Chat */}
        <main className="chat-main">
          <div className="chat-content">
            <MessageList />
            <MessageInput />
          </div>
        </main>

        {/* Sidebar destra - Lista utenti */}
        <aside className="sidebar right-sidebar">
          <UserList />
        </aside>
      </div>

      {/* Header mobile */}
      <header className="mobile-header">
        <div className="mobile-user-info">
          <span className="user-avatar-small">
            {user?.username.charAt(0).toUpperCase()}
          </span>
          <span className="username">{user?.username}</span>
        </div>
        <button className="logout-button" onClick={logout} title="Esci">
          <svg
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
          >
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
            <polyline points="16 17 21 12 16 7" />
            <line x1="21" y1="12" x2="9" y2="12" />
          </svg>
          Esci
        </button>
      </header>

      {/* Room badge mobile */}
      {currentRoom && (
        <div className="mobile-room-badge">
          <span className="room-emoji-small">{currentRoom.emoji}</span>
          <span className="room-name-small">{currentRoom.name}</span>
        </div>
      )}
    </div>
  );
}
