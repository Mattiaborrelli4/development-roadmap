import React from 'react';
import { useChat } from '../contexts/ChatContext';
import './RoomList.css';

export default function RoomList() {
  const { rooms, currentRoom, joinRoom, messages } = useChat();

  const getMessageCount = (roomId) => {
    return messages[roomId]?.length || 0;
  };

  return (
    <div className="room-list">
      <div className="room-list-header">
        <h2>🏠 Stanze</h2>
        <span className="room-count">{rooms.length}</span>
      </div>

      <div className="rooms">
        {rooms.map((room) => (
          <button
            key={room.id}
            className={`room-item ${currentRoom?.id === room.id ? 'active' : ''}`}
            onClick={() => joinRoom(room.id)}
          >
            <div className="room-emoji">{room.emoji}</div>
            <div className="room-info">
              <div className="room-name">{room.name}</div>
              <div className="room-description">{room.description}</div>
            </div>
            <div className="room-meta">
              <span className="message-count">{getMessageCount(room.id)}</span>
              {currentRoom?.id === room.id && (
                <span className="active-indicator">●</span>
              )}
            </div>
          </button>
        ))}
      </div>

      <div className="room-list-footer">
        <p>💬 {rooms.length} stanze disponibili</p>
      </div>
    </div>
  );
}
