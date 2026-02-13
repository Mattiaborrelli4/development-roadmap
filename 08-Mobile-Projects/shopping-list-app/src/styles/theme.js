import {StyleSheet} from 'react-native';
import {THEME} from '../utils/constants';

export const createTheme = (isDark = false) => {
  const colors = isDark ? THEME.dark : THEME.light;

  return StyleSheet.create({
    container: {
      flex: 1,
      backgroundColor: colors.background,
    },
    surface: {
      backgroundColor: colors.surface,
      padding: 16,
      borderRadius: 12,
      marginBottom: 12,
      shadowColor: colors.shadow,
      shadowOffset: {width: 0, height: 2},
      shadowOpacity: 1,
      shadowRadius: 4,
      elevation: 3,
    },
    card: {
      backgroundColor: colors.surface,
      padding: 16,
      borderRadius: 12,
      marginBottom: 12,
      borderWidth: 1,
      borderColor: colors.border,
    },
    title: {
      fontSize: 24,
      fontWeight: 'bold',
      color: colors.text,
      marginBottom: 8,
    },
    subtitle: {
      fontSize: 18,
      fontWeight: '600',
      color: colors.text,
      marginBottom: 4,
    },
    text: {
      fontSize: 16,
      color: colors.text,
    },
    textSecondary: {
      fontSize: 14,
      color: colors.textSecondary,
    },
    button: {
      backgroundColor: colors.primary,
      paddingVertical: 12,
      paddingHorizontal: 24,
      borderRadius: 8,
      alignItems: 'center',
      justifyContent: 'center',
    },
    buttonSecondary: {
      backgroundColor: 'transparent',
      borderWidth: 2,
      borderColor: colors.primary,
    },
    buttonText: {
      color: '#FFFFFF',
      fontSize: 16,
      fontWeight: '600',
    },
    buttonTextSecondary: {
      color: colors.primary,
      fontSize: 16,
      fontWeight: '600',
    },
    input: {
      backgroundColor: colors.surface,
      borderWidth: 1,
      borderColor: colors.border,
      borderRadius: 8,
      padding: 12,
      fontSize: 16,
      color: colors.text,
    },
    modalContainer: {
      flex: 1,
      backgroundColor: colors.background,
      padding: 20,
      paddingTop: 40,
    },
    modalHeader: {
      flexDirection: 'row',
      justifyContent: 'space-between',
      alignItems: 'center',
      marginBottom: 20,
    },
    fab: {
      position: 'absolute',
      bottom: 24,
      right: 24,
      width: 56,
      height: 56,
      borderRadius: 28,
      backgroundColor: colors.primary,
      justifyContent: 'center',
      alignItems: 'center',
      shadowColor: colors.shadow,
      shadowOffset: {width: 0, height: 4},
      shadowOpacity: 1,
      shadowRadius: 8,
      elevation: 8,
    },
    swipeActionLeft: {
      backgroundColor: colors.success,
      justifyContent: 'center',
      alignItems: 'flex-end',
      paddingRight: 20,
      width: 80,
    },
    swipeActionRight: {
      backgroundColor: colors.error,
      justifyContent: 'center',
      alignItems: 'flex-start',
      paddingLeft: 20,
      width: 80,
    },
    categoryBadge: {
      paddingHorizontal: 12,
      paddingVertical: 6,
      borderRadius: 16,
      marginRight: 8,
    },
    categoryBadgeText: {
      fontSize: 12,
      fontWeight: '600',
      color: '#FFFFFF',
    },
    progressBar: {
      height: 8,
      backgroundColor: colors.border,
      borderRadius: 4,
      overflow: 'hidden',
    },
    progressFill: {
      height: '100%',
      backgroundColor: colors.success,
    },
    listItemBought: {
      opacity: 0.6,
      textDecorationLine: 'line-through',
    },
    emptyState: {
      flex: 1,
      justifyContent: 'center',
      alignItems: 'center',
      padding: 40,
    },
    emptyStateText: {
      fontSize: 18,
      color: colors.textSecondary,
      marginTop: 16,
      textAlign: 'center',
    },
    header: {
      flexDirection: 'row',
      justifyContent: 'space-between',
      alignItems: 'center',
      padding: 20,
      paddingTop: 40,
      backgroundColor: colors.surface,
      borderBottomWidth: 1,
      borderBottomColor: colors.border,
    },
    listItem: {
      flexDirection: 'row',
      alignItems: 'center',
      padding: 16,
      backgroundColor: colors.surface,
      borderBottomWidth: 1,
      borderBottomColor: colors.border,
    },
    listItemImage: {
      width: 50,
      height: 50,
      borderRadius: 8,
      marginRight: 12,
      justifyContent: 'center',
      alignItems: 'center',
      fontSize: 24,
    },
    listItemInfo: {
      flex: 1,
    },
    listItemMeta: {
      fontSize: 12,
      color: colors.textSecondary,
      marginTop: 4,
    },
    chip: {
      paddingHorizontal: 12,
      paddingVertical: 6,
      borderRadius: 16,
      backgroundColor: colors.border,
      marginRight: 8,
      marginBottom: 8,
    },
    chipText: {
      fontSize: 14,
      color: colors.text,
    },
    chipActive: {
      backgroundColor: colors.primary,
    },
    chipActiveText: {
      color: '#FFFFFF',
      fontWeight: '600',
    },
    statistics: {
      flexDirection: 'row',
      justifyContent: 'space-around',
      padding: 16,
      backgroundColor: colors.surface,
      borderRadius: 12,
      marginBottom: 16,
    },
    statItem: {
      alignItems: 'center',
    },
    statValue: {
      fontSize: 24,
      fontWeight: 'bold',
      color: colors.primary,
    },
    statLabel: {
      fontSize: 12,
      color: colors.textSecondary,
      marginTop: 4,
    },
  });
};

export const spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
};

export const borderRadius = {
  sm: 4,
  md: 8,
  lg: 12,
  xl: 16,
  round: 999,
};
