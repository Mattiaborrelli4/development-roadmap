import React from 'react';
import { useChat } from '../contexts/ChatContext';
import './UserList.css';

export default function UserList() {
  const { onlineUsers, user } = useChat();

  const getStatusColor = (status) => {
    switch (status) {
      case 'online':
        return '#48bb78';
      case 'away':
        return '#ecc94b';
      case 'offline':
        return '#cbd5e0';
      default:
        return '#cbd5e0';
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'online':
        return 'Online';
      case 'away':
        return 'Assente';
      case 'offline':
        return 'Offline';
      default:
        return 'Sconosciuto';
    }
  };

  const formatLastSeen = (date) => {
    if (!date) return '';
    const now = new Date();
    const diff = now - new Date(date);
    const minutes = Math.floor(diff / 60000);

    if (minutes < 1) return 'Adesso';
    if (minutes < 60) return `${minutes}m fa`;
    const hours = Math.floor(minutes / 60);
    if (hours < 24) return `${hours}h fa`;
    const days = Math.floor(hours / 24);
    return `${days}g fa`;
  };

  const onlineCount = onlineUsers.filter(u => u.status === 'online').length;

  return (
    <div className="user-list">
      <div className="user-list-header">
        <h2>👥 Utenti</h2>
        <span className="online-count">{onlineCount} online</span>
      </div>

      <div className="users">
        {onlineUsers.map((u) => (
          <div
            key={u.id}
            className={`user-item ${u.id === user?.id ? 'current-user' : ''}`}
          >
            <div className="user-avatar">
              <span className="avatar-text">
                {u.username.charAt(0).toUpperCase()}
              </span>
              <span
                className="status-indicator"
                style={{ backgroundColor: getStatusColor(u.status) }}
              ></span>
            </div>
            <div className="user-info">
              <div className="user-name">
                {u.username}
                {u.id === user?.id && <span className="you-badge">(Tu)</span>}
              </div>
              <div className="user-status">
                {u.status === 'online' ? (
                  <>
                    <span className="status-dot online"></span>
                    {getStatusText(u.status)}
                  </>
                ) : u.status === 'away' ? (
                  <>
                    <span className="status-dot away"></span>
                    {getStatusText(u.status)}
                  </>
                ) : (
                  <>
                    <span className="status-dot offline"></span>
                    {formatLastSeen(u.lastSeen)}
                  </>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="user-list-footer">
        <p>🌐 {onlineUsers.length} utenti totali</p>
      </div>
    </div>
  );
}
