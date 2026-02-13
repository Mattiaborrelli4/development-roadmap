import React, { createContext, useContext, useReducer, useEffect } from 'react';
import socket from '../utils/socket';
import { initialRooms, initialMessages } from '../data';

// Crea il Context
const ChatContext = createContext();

// Azioni
const ACTIONS = {
  SET_USER: 'SET_USER',
  SET_ROOMS: 'SET_ROOMS',
  SET_MESSAGES: 'SET_MESSAGES',
  ADD_MESSAGE: 'ADD_MESSAGE',
  SET_CURRENT_ROOM: 'SET_CURRENT_ROOM',
  SET_TYPING_USERS: 'SET_TYPING_USERS',
  SET_ONLINE_USERS: 'SET_ONLINE_USERS',
  SET_LOADING: 'SET_LOADING',
  SET_ERROR: 'SET_ERROR',
  ADD_TYPING_USER: 'ADD_TYPING_USER',
  REMOVE_TYPING_USER: 'REMOVE_TYPING_USER'
};

// Stato iniziale
const initialState = {
  user: null,
  rooms: [],
  messages: {},
  currentRoom: null,
  typingUsers: [],
  onlineUsers: [],
  loading: false,
  error: null,
  isConnected: false
};

// Reducer
function chatReducer(state, action) {
  switch (action.type) {
    case ACTIONS.SET_USER:
      return {
        ...state,
        user: action.payload,
        isConnected: !!action.payload
      };

    case ACTIONS.SET_ROOMS:
      return {
        ...state,
        rooms: action.payload
      };

    case ACTIONS.SET_MESSAGES:
      return {
        ...state,
        messages: action.payload
      };

    case ACTIONS.ADD_MESSAGE:
      const { roomId } = action.payload;
      const roomMessages = state.messages[roomId] || [];
      return {
        ...state,
        messages: {
          ...state.messages,
          [roomId]: [...roomMessages, action.payload]
        }
      };

    case ACTIONS.SET_CURRENT_ROOM:
      return {
        ...state,
        currentRoom: action.payload
      };

    case ACTIONS.SET_TYPING_USERS:
      return {
        ...state,
        typingUsers: action.payload
      };

    case ACTIONS.ADD_TYPING_USER:
      const exists = state.typingUsers.some(
        u => u.userId === action.payload.userId
      );
      if (exists) return state;
      return {
        ...state,
        typingUsers: [...state.typingUsers, action.payload]
      };

    case ACTIONS.REMOVE_TYPING_USER:
      return {
        ...state,
        typingUsers: state.typingUsers.filter(
          u => u.userId !== action.payload.userId
        )
      };

    case ACTIONS.SET_ONLINE_USERS:
      return {
        ...state,
        onlineUsers: action.payload
      };

    case ACTIONS.SET_LOADING:
      return {
        ...state,
        loading: action.payload
      };

    case ACTIONS.SET_ERROR:
      return {
        ...state,
        error: action.payload
      };

    default:
      return state;
  }
}

// Provider Component
export function ChatProvider({ children }) {
  const [state, dispatch] = useReducer(chatReducer, initialState);

  // Carica dati da localStorage
  useEffect(() => {
    const savedUser = localStorage.getItem('chatUser');
    const savedMessages = localStorage.getItem('chatMessages');

    if (savedUser) {
      dispatch({
        type: ACTIONS.SET_USER,
        payload: JSON.parse(savedUser)
      });
    }

    if (savedMessages) {
      dispatch({
        type: ACTIONS.SET_MESSAGES,
        payload: JSON.parse(savedMessages)
      });
    } else {
      dispatch({
        type: ACTIONS.SET_MESSAGES,
        payload: initialMessages
      });
    }

    dispatch({
      type: ACTIONS.SET_ROOMS,
      payload: initialRooms
    });

    // Carica utenti online
    dispatch({
      type: ACTIONS.SET_ONLINE_USERS,
      payload: socket.getOnlineUsers()
    });

    // Setup Socket listeners
    setupSocketListeners();
  }, []);

  // Salva messaggi in localStorage quando cambiano
  useEffect(() => {
    if (Object.keys(state.messages).length > 0) {
      localStorage.setItem('chatMessages', JSON.stringify(state.messages));
    }
  }, [state.messages]);

  const setupSocketListeners = () => {
    // Ascolta nuovi messaggi
    socket.on('message', (message) => {
      dispatch({
        type: ACTIONS.ADD_MESSAGE,
        payload: message
      });
    });

    // Ascolta eventi di digitazione
    socket.on('typing', (data) => {
      if (data.isTyping) {
        dispatch({
          type: ACTIONS.ADD_TYPING_USER,
          payload: data
        });
      } else {
        dispatch({
          type: ACTIONS.REMOVE_TYPING_USER,
          payload: data
        });
      }
    });

    // Ascolta connessioni
    socket.on('connect', () => {
      dispatch({ type: ACTIONS.SET_ERROR, payload: null });
    });

    // Ascolta disconnessioni
    socket.on('disconnect', () => {
      dispatch({ type: ACTIONS.SET_ERROR, payload: 'Connessione persa' });
    });
  };

  // Azioni
  const login = async (username) => {
    dispatch({ type: ACTIONS.SET_LOADING, payload: true });

    try {
      const userId = 'user_' + Date.now();
      const user = { id: userId, username };

      await socket.connect(userId, username);

      localStorage.setItem('chatUser', JSON.stringify(user));

      dispatch({
        type: ACTIONS.SET_USER,
        payload: user
      });

      dispatch({ type: ACTIONS.SET_LOADING, payload: false });

      return user;
    } catch (error) {
      dispatch({
        type: ACTIONS.SET_ERROR,
        payload: 'Errore durante il login'
      });
      dispatch({ type: ACTIONS.SET_LOADING, payload: false });
      throw error;
    }
  };

  const logout = () => {
    socket.disconnect();
    localStorage.removeItem('chatUser');
    dispatch({ type: ACTIONS.SET_USER, payload: null });
    dispatch({ type: ACTIONS.SET_CURRENT_ROOM, payload: null });
  };

  const joinRoom = (roomId) => {
    const room = state.rooms.find(r => r.id === roomId);
    if (room) {
      dispatch({ type: ACTIONS.SET_CURRENT_ROOM, payload: room });
      socket.joinRoom(roomId);

      // Simula messaggi in arrivo occasionalmente
      const interval = setInterval(() => {
        if (Math.random() > 0.7) {
          socket.simulateIncomingMessage(roomId);
        }
      }, 15000);

      // Simula digitazione
      setInterval(() => {
        if (Math.random() > 0.8) {
          socket.simulateTyping(roomId);
        }
      }, 20000);

      return () => clearInterval(interval);
    }
  };

  const sendMessage = (text) => {
    if (!state.currentRoom || !text.trim()) return;

    const message = socket.emitMessage(state.currentRoom.id, text);
    dispatch({
      type: ACTIONS.ADD_MESSAGE,
      payload: message
    });

    return message;
  };

  const sendTyping = (isTyping) => {
    if (state.currentRoom) {
      socket.emitTyping(state.currentRoom.id, isTyping);
    }
  };

  const value = {
    // Stato
    ...state,

    // Azioni
    login,
    logout,
    joinRoom,
    sendMessage,
    sendTyping
  };

  return (
    <ChatContext.Provider value={value}>
      {children}
    </ChatContext.Provider>
  );
}

// Hook personalizzato
export function useChat() {
  const context = useContext(ChatContext);
  if (!context) {
    throw new Error('useChat deve essere usato dentro un ChatProvider');
  }
  return context;
}
