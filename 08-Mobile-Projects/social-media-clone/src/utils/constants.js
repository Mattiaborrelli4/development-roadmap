// Utiles costanti per l'applicazione

export const THEME = {
  colors: {
    primary: '#0095F6',
    primaryDark: '#1877F2',
    secondary: '#0095F6',
    background: '#FFFFFF',
    backgroundSecondary: '#FAFAFA',
    text: '#262626',
    textSecondary: '#8E8E8E',
    textLight: '#C7C7C7',
    border: '#DBDBDB',
    error: '#ED4956',
    success: '#00C853',
    like: '#ED4956',
    storyRing: '#C13584',
    storyRingGradient: ['#F58529', '#DD2A7B', '#8134AF', '#515BD4'],
  },
  spacing: {
    xs: 4,
    sm: 8,
    md: 12,
    lg: 16,
    xl: 20,
    xxl: 24,
  },
  borderRadius: {
    sm: 4,
    md: 8,
    lg: 12,
    xl: 16,
    round: 999,
  },
  fontSize: {
    xs: 10,
    sm: 12,
    md: 14,
    lg: 16,
    xl: 18,
    xxl: 24,
    xxxl: 32,
  },
  shadows: {
    sm: {
      shadowColor: '#000',
      shadowOffset: { width: 0, height: 1 },
      shadowOpacity: 0.1,
      shadowRadius: 2,
      elevation: 1,
    },
    md: {
      shadowColor: '#000',
      shadowOffset: { width: 0, height: 2 },
      shadowOpacity: 0.15,
      shadowRadius: 4,
      elevation: 2,
    },
  },
};

export const POST_TYPES = {
  IMAGE: 'image',
  VIDEO: 'video',
};

export const NOTIFICATION_TYPES = {
  LIKE: 'like',
  COMMENT: 'comment',
  FOLLOW: 'follow',
  MENTION: 'mention',
};

export const TABS = {
  HOME: 'Home',
  SEARCH: 'Search',
  ADD: 'Add',
  NOTIFICATIONS: 'Notifications',
  PROFILE: 'Profile',
};

export const SAMPLE_IMAGES = [
  'https://picsum.photos/600/600?random=1',
  'https://picsum.photos/600/600?random=2',
  'https://picsum.photos/600/600?random=3',
  'https://picsum.photos/600/600?random=4',
  'https://picsum.photos/600/600?random=5',
  'https://picsum.photos/600/600?random=6',
  'https://picsum.photos/600/600?random=7',
  'https://picsum.photos/600/600?random=8',
  'https://picsum.photos/600/600?random=9',
  'https://picsum.photos/600/600?random=10',
];

export const SAMPLE_AVATARS = [
  'https://i.pravatar.cc/150?img=1',
  'https://i.pravatar.cc/150?img=2',
  'https://i.pravatar.cc/150?img=3',
  'https://i.pravatar.cc/150?img=4',
  'https://i.pravatar.cc/150?img=5',
  'https://i.pravatar.cc/150?img=6',
  'https://i.pravatar.cc/150?img=7',
  'https://i.pravatar.cc/150?img=8',
  'https://i.pravatar.cc/150?img=9',
  'https://i.pravatar.cc/150?img=10',
  'https://i.pravatar.cc/150?img=11',
  'https://i.pravatar.cc/150?img=12',
];
