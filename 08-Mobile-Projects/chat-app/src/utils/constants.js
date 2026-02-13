// Utente corrente (hardcoded per demo)
export const CURRENT_USER_ID = 'user1';

// Dati mock per gli utenti
export const MOCK_USERS = [
  {
    id: 'user1',
    username: 'Mario Rossi',
    avatar: 'https://i.pravatar.cc/150?img=1',
    status: 'online',
    lastSeen: Date.now()
  },
  {
    id: 'user2',
    username: 'Laura Bianchi',
    avatar: 'https://i.pravatar.cc/150?img=5',
    status: 'online',
    lastSeen: Date.now() - 300000
  },
  {
    id: 'user3',
    username: 'Giuseppe Verdi',
    avatar: 'https://i.pravatar.cc/150?img=3',
    status: 'away',
    lastSeen: Date.now() - 900000
  },
  {
    id: 'user4',
    username: 'Anna Neri',
    avatar: 'https://i.pravatar.cc/150?img=9',
    status: 'offline',
    lastSeen: Date.now() - 3600000
  },
  {
    id: 'user5',
    username: 'Marco Ferrari',
    avatar: 'https://i.pravatar.cc/150?img=12',
    status: 'online',
    lastSeen: Date.now()
  }
];

// Dati mock per le stanze di chat
export const MOCK_CHAT_ROOMS = [
  {
    id: 'room1',
    name: 'Gruppo Lavoro',
    type: 'group',
    participants: ['user1', 'user2', 'user3'],
    lastMessage: {
      text: 'Buongiorno a tutti!',
      senderId: 'user2',
      timestamp: Date.now() - 300000
    },
    unreadCount: 3,
    createdAt: Date.now() - 86400000
  },
  {
    id: 'room2',
    name: 'Laura Bianchi',
    type: 'direct',
    participants: ['user1', 'user2'],
    lastMessage: {
      text: 'Ci vediamo domani?',
      senderId: 'user2',
      timestamp: Date.now() - 600000
    },
    unreadCount: 1,
    createdAt: Date.now() - 172800000
  },
  {
    id: 'room3',
    name: 'Famiglia',
    type: 'group',
    participants: ['user1', 'user4', 'user5'],
    lastMessage: {
      text: 'A che ora arrivate?',
      senderId: 'user4',
      timestamp: Date.now() - 1800000
    },
    unreadCount: 0,
    createdAt: Date.now() - 259200000
  }
];

// Messaggi mock iniziali per ogni stanza
export const MOCK_MESSAGES = {
  room1: [
    {
      id: 'msg1',
      roomId: 'room1',
      senderId: 'user1',
      text: 'Ciao ragazzi, come procede il progetto?',
      type: 'text',
      timestamp: Date.now() - 3600000,
      read: true,
      readBy: ['user2', 'user3']
    },
    {
      id: 'msg2',
      roomId: 'room1',
      senderId: 'user2',
      text: 'Tutto bene! Ho completato la mia parte.',
      type: 'text',
      timestamp: Date.now() - 300000,
      read: true,
      readBy: ['user1', 'user3']
    },
    {
      id: 'msg3',
      roomId: 'room1',
      senderId: 'user3',
      text: 'Ottimo lavoro! Io ho quasi finito.',
      type: 'text',
      timestamp: Date.now() - 200000,
      read: false,
      readBy: []
    }
  ],
  room2: [
    {
      id: 'msg4',
      roomId: 'room2',
      senderId: 'user2',
      text: 'Hey, ci vediamo domani per il caffè?',
      type: 'text',
      timestamp: Date.now() - 1800000,
      read: true,
      readBy: ['user1']
    },
    {
      id: 'msg5',
      roomId: 'room2',
      senderId: 'user1',
      text: 'Certo! A che ora?',
      type: 'text',
      timestamp: Date.now() - 1200000,
      read: true,
      readBy: ['user2']
    },
    {
      id: 'msg6',
      roomId: 'room2',
      senderId: 'user2',
      text: 'Ci vediamo domani?',
      type: 'text',
      timestamp: Date.now() - 600000,
      read: false,
      readBy: []
    }
  ],
  room3: [
    {
      id: 'msg7',
      roomId: 'room3',
      senderId: 'user4',
      text: 'A che ora arrivate domani?',
      type: 'text',
      timestamp: Date.now() - 1800000,
      read: true,
      readBy: ['user1', 'user5']
    }
  ]
};

// Frasi random per simulare messaggi in arrivo
export const RANDOM_MESSAGES = [
  'Hey, come va?',
  'Tutto bene!',
  'Ho visto quello che mi hai mandato',
  'Perfetto, grazie!',
  'Ok ci sentiamo dopo',
  'A che ora?',
  'Posso chiederti una cosa?',
  'Ho finito il lavoro',
  'Sei libero stasera?',
  'Grazie mille!',
  'Va bene!',
  'Ok perfetto',
  'Devo andare, ci vediamo!',
  'Bellissimo!',
  'Lo provo subito'
];

// Configurazioni timer
export const MESSAGE_INTERVAL_MIN = 10000; // 10 secondi
export const MESSAGE_INTERVAL_MAX = 30000; // 30 secondi
export const TYPING_DURATION = 2000; // 2 secondi
export const STATUS_CHANGE_INTERVAL = 60000; // 1 minuto

// Chiavi AsyncStorage
export const STORAGE_KEYS = {
  MESSAGES: '@chat_app_messages',
  ROOMS: '@chat_app_rooms',
  USERS: '@chat_app_users',
  CURRENT_USER: '@chat_app_current_user'
};

// Stato online
export const ONLINE_STATUS = {
  ONLINE: 'online',
  OFFLINE: 'offline',
  AWAY: 'away'
};

// Tipo messaggio
export const MESSAGE_TYPE = {
  TEXT: 'text',
  IMAGE: 'image',
  SYSTEM: 'system'
};

// Tipo stanza
export const ROOM_TYPE = {
  GROUP: 'group',
  DIRECT: 'direct'
};
