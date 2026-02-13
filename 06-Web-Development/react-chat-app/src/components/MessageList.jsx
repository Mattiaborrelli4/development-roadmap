import React, { useRef, useEffect } from 'react';
import { useChat } from '../contexts/ChatContext';
import './MessageList.css';

export default function MessageList() {
  const { currentRoom, messages, user, typingUsers } = useChat();
  const messagesEndRef = useRef(null);
  const messagesContainerRef = useRef(null);

  const roomMessages = currentRoom ? (messages[currentRoom.id] || []) : [];

  // Auto-scroll all'ultimo messaggio
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [roomMessages]);

  const formatTime = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString('it-IT', {
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const formatDate = (timestamp) => {
    const date = new Date(timestamp);
    const today = new Date();
    const yesterday = new Date(today);
    yesterday.setDate(yesterday.getDate() - 1);

    if (date.toDateString() === today.toDateString()) {
      return 'Oggi';
    } else if (date.toDateString() === yesterday.toDateString()) {
      return 'Ieri';
    } else {
      return date.toLocaleDateString('it-IT', {
        day: '2-digit',
        month: 'short',
        year: 'numeric'
      });
    }
  };

  const groupMessagesByDate = (messages) => {
    const groups = [];
    let currentDate = null;

    messages.forEach((message, index) => {
      const messageDate = new Date(message.timestamp).toDateString();

      if (messageDate !== currentDate) {
        currentDate = messageDate;
        groups.push({ type: 'date', date: message.timestamp, messages: [] });
      }

      groups[groups.length - 1].messages.push(message);
    });

    return groups;
  };

  if (!currentRoom) {
    return (
      <div className="message-list empty">
        <div className="empty-state">
          <div className="empty-icon">💬</div>
          <h3>Benvenuto in React Chat!</h3>
          <p>Seleziona una stanza per iniziare a chattare</p>
        </div>
      </div>
    );
  }

  const messageGroups = groupMessagesByDate(roomMessages);
  const currentTypingUsers = typingUsers.filter(
    u => u.userId !== user?.id
  );

  return (
    <div className="message-list">
      <div className="chat-header">
        <div className="room-info">
          <span className="room-emoji">{currentRoom.emoji}</span>
          <div>
            <h3>{currentRoom.name}</h3>
            <p>{currentRoom.description}</p>
          </div>
        </div>
      </div>

      <div className="messages-container" ref={messagesContainerRef}>
        {messageGroups.length === 0 ? (
          <div className="empty-room">
            <p>🎉 Nessun messaggio in questa stanza!</p>
            <p>Sii il primo a scrivere qualcosa!</p>
          </div>
        ) : (
          messageGroups.map((group, groupIndex) => (
            <div key={groupIndex} className="message-group">
              <div className="date-divider">
                <span>{formatDate(group.date)}</span>
              </div>

              {group.messages.map((message) => {
                const isOwn = message.userId === user?.id;
                const showAvatar = !isOwn && message.type !== 'system' && message.type !== 'notification';

                return (
                  <div
                    key={message.id}
                    className={`message-wrapper ${isOwn ? 'own' : ''} ${message.type}`}
                  >
                    {message.type === 'system' || message.type === 'notification' ? (
                      <div className="system-message">
                        <span>{message.text}</span>
                        <small>{formatTime(message.timestamp)}</small>
                      </div>
                    ) : (
                      <div className="message">
                        {showAvatar && (
                          <div className="message-avatar">
                            {message.username.charAt(0).toUpperCase()}
                          </div>
                        )}
                        <div className="message-content-wrapper">
                          {!isOwn && (
                            <div className="message-sender">
                              {message.username}
                            </div>
                          )}
                          <div className="message-bubble">
                            <p>{message.text}</p>
                            <span className="message-time">
                              {formatTime(message.timestamp)}
                            </span>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          ))
        )}

        {currentTypingUsers.length > 0 && (
          <div className="typing-indicator">
            <div className="typing-dots">
              <span></span>
              <span></span>
              <span></span>
            </div>
            <span className="typing-text">
              {currentTypingUsers.length === 1
                ? `${currentTypingUsers[0].username} sta scrivendo...`
                : `${currentTypingUsers.map(u => u.username).join(', ')} stanno scrivendo...`}
            </span>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>
    </div>
  );
}
