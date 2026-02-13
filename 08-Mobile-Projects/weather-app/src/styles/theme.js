export const theme = {
  colors: {
    primary: '#4facfe',
    secondary: '#00f2fe',
    accent: '#FF6B6B',
    text: '#2c3e50',
    textLight: '#7f8c8d',
    textWhite: '#ffffff',
    background: '#f8f9fa',
    card: '#ffffff',
    border: '#e1e8ed',
    shadow: 'rgba(0, 0, 0, 0.1)',
    success: '#4CAF50',
    warning: '#FFC107',
    error: '#F44336',
    info: '#2196F3',
  },

  gradients: {
    sunny: ['#4facfe', '#00f2fe'],
    cloudy: ['#bdc3c7', '#2c3e50'],
    rainy: ['#5b86e5', '#36d1dc'],
    stormy: ['#373b44', '#4286f4'],
    snowy: ['#e6e9f0', '#eef1f5'],
    default: ['#4facfe', '#00f2fe'],
  },

  spacing: {
    xs: 4,
    sm: 8,
    md: 16,
    lg: 24,
    xl: 32,
    xxl: 48,
  },

  borderRadius: {
    sm: 8,
    md: 12,
    lg: 16,
    xl: 24,
    full: 9999,
  },

  fontSize: {
    xs: 12,
    sm: 14,
    md: 16,
    lg: 18,
    xl: 24,
    xxl: 32,
    xxxl: 48,
  },

  fontWeight: {
    light: '300',
    regular: '400',
    medium: '500',
    semibold: '600',
    bold: '700',
  },

  shadows: {
    sm: {
      shadowColor: '#000',
      shadowOffset: { width: 0, height: 1 },
      shadowOpacity: 0.1,
      shadowRadius: 2,
      elevation: 2,
    },
    md: {
      shadowColor: '#000',
      shadowOffset: { width: 0, height: 2 },
      shadowOpacity: 0.15,
      shadowRadius: 4,
      elevation: 4,
    },
    lg: {
      shadowColor: '#000',
      shadowOffset: { width: 0, height: 4 },
      shadowOpacity: 0.2,
      shadowRadius: 8,
      elevation: 8,
    },
  },
};

export const commonStyles = {
  container: {
    flex: 1,
    backgroundColor: theme.colors.background,
  },
  centerContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  card: {
    backgroundColor: theme.colors.card,
    borderRadius: theme.borderRadius.md,
    padding: theme.spacing.md,
    ...theme.shadows.sm,
  },
  text: {
    fontSize: theme.fontSize.md,
    color: theme.colors.text,
  },
  title: {
    fontSize: theme.fontSize.xl,
    fontWeight: theme.fontWeight.bold,
    color: theme.colors.text,
  },
  subtitle: {
    fontSize: theme.fontSize.lg,
    fontWeight: theme.fontWeight.medium,
    color: theme.colors.textLight,
  },
};
