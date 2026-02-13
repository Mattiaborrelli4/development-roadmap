// Dati iniziali per le stanze e gli utenti
export const initialRooms = [
  {
    id: 'general',
    name: 'Generale',
    description: 'Discussioni generali su qualsiasi argomento',
    emoji: '💬'
  },
  {
    id: 'tech',
    name: 'Tecnologia',
    description: 'Parliamo di programmazione, framework e novità tech',
    emoji: '💻'
  },
  {
    id: 'music',
    name: 'Musica',
    description: 'Condividi la tua musica preferita e scopri nuova musica',
    emoji: '🎵'
  },
  {
    id: 'gaming',
    name: 'Gaming',
    description: 'Discussioni su videogiochi, console e e-sports',
    emoji: '🎮'
  },
  {
    id: 'random',
    name: 'Random',
    description: 'Tutto e il contrario di tutto',
    emoji: '🎲'
  }
];

export const initialMessages = {
  general: [
    {
      id: '1',
      roomId: 'general',
      userId: 'system',
      username: 'Sistema',
      text: 'Benvenuto nella chat generale! 🎉',
      timestamp: new Date(Date.now() - 3600000).toISOString(),
      type: 'system'
    },
    {
      id: '2',
      roomId: 'general',
      userId: 'user1',
      username: 'Mario',
      text: 'Ciao a tutti! Qualcuno ha provato il nuovo framework?',
      timestamp: new Date(Date.now() - 3000000).toISOString(),
      type: 'message'
    },
    {
      id: '3',
      roomId: 'general',
      userId: 'user2',
      username: 'Luca',
      text: 'Sì! È fantastico. La documentazione è ottima 🚀',
      timestamp: new Date(Date.now() - 2400000).toISOString(),
      type: 'message'
    }
  ],
  tech: [
    {
      id: '4',
      roomId: 'tech',
      userId: 'system',
      username: 'Sistema',
      text: 'Benvenuto nella stanza Tecnologia! 💻',
      timestamp: new Date(Date.now() - 7200000).toISOString(),
      type: 'system'
    },
    {
      id: '5',
      roomId: 'tech',
      userId: 'user3',
      username: 'Giulia',
      text: 'Qualcuno usa TypeScript con React?',
      timestamp: new Date(Date.now() - 3600000).toISOString(),
      type: 'message'
    }
  ],
  music: [
    {
      id: '6',
      roomId: 'music',
      userId: 'system',
      username: 'Sistema',
      text: 'Benvenuto nella stanza Musica! 🎵',
      timestamp: new Date(Date.now() - 5400000).toISOString(),
      type: 'system'
    }
  ],
  gaming: [
    {
      id: '7',
      roomId: 'gaming',
      userId: 'system',
      username: 'Sistema',
      text: 'Benvenuto nella stanza Gaming! 🎮',
      timestamp: new Date(Date.now() - 1800000).toISOString(),
      type: 'system'
    }
  ],
  random: [
    {
      id: '8',
      roomId: 'random',
      userId: 'system',
      username: 'Sistema',
      text: 'Benvenuto nella stanza Random! 🎲',
      timestamp: new Date(Date.now() - 900000).toISOString(),
      type: 'system'
    }
  ]
};

export const sampleMessages = [
  'Interessante! Raccontami di più 🤔',
  'Sono d\'accordo con te!',
  'Wow, non lo sapevo! 🎉',
  'Ho appena finito un progetto simile',
  'Qualcuno ha documentazione utile?',
  'Grazie per il consiglio! 👍',
  'Stasera provo a implementarlo',
  'È una feature molto richiesta',
  'Ho trovato un bug interessante...',
  'Prova a guardare la documentazione ufficiale',
  'Funziona perfettamente! ✨',
  'Qual è la tua opinione?',
  'Secondo me è la scelta migliore',
  'Esattamente! 💯',
  'Perfetto, grazie mille!'
];

export const emojis = [
  '😀', '😂', '😍', '🥰', '😎', '🤔', '😴', '🥳',
  '❤️', '👍', '👎', '👏', '🙌', '🤝', '✌️', '🤟',
  '🎉', '🎊', '🔥', '✨', '💯', '⭐', '💫', '🌟',
  '💻', '🎮', '🎵', '📚', '🎯', '🚀', '💡', '🔧'
];
