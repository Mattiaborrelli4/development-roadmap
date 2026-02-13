// Costanti per l'app Fitness Tracker

export const WORKOUT_TYPES = {
  RUNNING: 'running',
  CYCLING: 'cycling',
  WALKING: 'walking',
  GYM: 'gym',
  SWIMMING: 'swimming',
  YOGA: 'yoga',
  OTHER: 'other'
};

export const WORKOUT_LABELS = {
  running: 'Corsa',
  cycling: 'Ciclismo',
  walking: 'Camminata',
  gym: 'Palestra',
  swimming: 'Nuoto',
  yoga: 'Yoga',
  other: 'Altro'
};

export const GOAL_TYPES = {
  STEPS: 'steps',
  CALORIES: 'calories',
  DISTANCE: 'distance',
  DURATION: 'duration'
};

export const GOAL_PERIODS = {
  DAILY: 'daily',
  WEEKLY: 'weekly'
};

export const WORKOUT_ICONS = {
  running: '🏃',
  cycling: '🚴',
  walking: '🚶',
  gym: '🏋️',
  swimming: '🏊',
  yoga: '🧘',
  other: '💪'
};

export const ACHIEVEMENTS = {
  FIRST_WORKOUT: { id: 'first_workout', title: 'Primo Passo', description: 'Completa il primo allenamento', icon: '🎯', requirement: 1 },
  WEEK_STREAK: { id: 'week_streak', title: 'Settimana Intensa', description: 'Allena tutti i giorni per una settimana', icon: '🔥', requirement: 7 },
  MARATHON: { id: 'marathon', title: 'Maratoneta', description: 'Corri 42km in totale', icon: '🏅', requirement: 42 },
  CENTURY: { id: 'century', title: 'Centenario', description: 'Completa 100 allenamenti', icon: '💯', requirement: 100 },
  STEPS_10K: { id: 'steps_10k', title: 'Camminatore', description: 'Raggiungi 10.000 passi in un giorno', icon: '👟', requirement: 10000 },
  CALORIE_GOAL: { id: 'calorie_goal', title: 'Bruciagrassi', description: 'Brucia 500 calorie in un giorno', icon: '⚡', requirement: 500 }
};

export const DEFAULT_GOALS = {
  daily: {
    steps: 10000,
    calories: 500,
    distance: 5,
    duration: 30
  },
  weekly: {
    steps: 70000,
    calories: 3500,
    distance: 35,
    duration: 210
  }
};

export const COLORS = {
  primary: '#00D4AA',
  secondary: '#6C5CE7',
  accent: '#FF6B6B',
  success: '#00B894',
  warning: '#FDCB6E',
  danger: '#FF7675',
  info: '#74B9FF',
  background: '#F8F9FA',
  surface: '#FFFFFF',
  text: '#2D3436',
  textSecondary: '#636E72',
  border: '#DFE6E9',
  overlay: 'rgba(0, 0, 0, 0.5)'
};

export const CHART_COLORS = [
  '#00D4AA',
  '#6C5CE7',
  '#FF6B6B',
  '#FDCB6E',
  '#74B9FF',
  '#A29BFE',
  '#FD79A8',
  '#FAB1A0'
];

export const STORAGE_KEYS = {
  WORKOUTS: '@fitness_workouts',
  GOALS: '@fitness_goals',
  STEPS: '@fitness_steps',
  ACHIEVEMENTS: '@fitness_achievements',
  STATS: '@fitness_stats'
};
