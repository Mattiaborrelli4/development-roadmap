import { StyleSheet, Dimensions } from 'react-native';
import { COLORS, CHART_COLORS } from '../utils/constants';

const { width, height } = Dimensions.get('window');

export const theme = {
  colors: COLORS,
  chartColors: CHART_COLORS,
  spacing: {
    xs: 4,
    sm: 8,
    md: 16,
    lg: 24,
    xl: 32,
    xxl: 48
  },
  borderRadius: {
    sm: 8,
    md: 12,
    lg: 16,
    xl: 24,
    round: 999
  },
  fontSize: {
    xs: 10,
    sm: 12,
    md: 14,
    lg: 16,
    xl: 20,
    xxl: 24,
    xxxl: 32
  },
  shadows: {
    sm: {
      shadowColor: '#000',
      shadowOffset: { width: 0, height: 1 },
      shadowOpacity: 0.05,
      shadowRadius: 2,
      elevation: 1
    },
    md: {
      shadowColor: '#000',
      shadowOffset: { width: 0, height: 2 },
      shadowOpacity: 0.1,
      shadowRadius: 4,
      elevation: 2
    },
    lg: {
      shadowColor: '#000',
      shadowOffset: { width: 0, height: 4 },
      shadowOpacity: 0.15,
      shadowRadius: 8,
      elevation: 4
    }
  }
};

export const globalStyles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  safeArea: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  scrollContainer: {
    flexGrow: 1,
    padding: theme.spacing.md,
  },
  card: {
    backgroundColor: COLORS.surface,
    borderRadius: theme.borderRadius.md,
    padding: theme.spacing.md,
    ...theme.shadows.sm,
  },
  title: {
    fontSize: theme.fontSize.xl,
    fontWeight: 'bold',
    color: COLORS.text,
    marginBottom: theme.spacing.md,
  },
  subtitle: {
    fontSize: theme.fontSize.lg,
    fontWeight: '600',
    color: COLORS.text,
    marginBottom: theme.spacing.sm,
  },
  text: {
    fontSize: theme.fontSize.md,
    color: COLORS.text,
  },
  textSecondary: {
    fontSize: theme.fontSize.md,
    color: COLORS.textSecondary,
  },
  button: {
    backgroundColor: COLORS.primary,
    borderRadius: theme.borderRadius.md,
    paddingVertical: theme.spacing.md,
    paddingHorizontal: theme.spacing.lg,
    alignItems: 'center',
    justifyContent: 'center',
    ...theme.shadows.sm,
  },
  buttonText: {
    color: COLORS.surface,
    fontSize: theme.fontSize.lg,
    fontWeight: '600',
  },
  buttonSecondary: {
    backgroundColor: COLORS.surface,
    borderWidth: 1,
    borderColor: COLORS.primary,
  },
  buttonSecondaryText: {
    color: COLORS.primary,
  },
  input: {
    backgroundColor: COLORS.surface,
    borderWidth: 1,
    borderColor: COLORS.border,
    borderRadius: theme.borderRadius.sm,
    paddingHorizontal: theme.spacing.md,
    paddingVertical: theme.spacing.sm,
    fontSize: theme.fontSize.md,
    color: COLORS.text,
  },
  errorText: {
    color: COLORS.danger,
    fontSize: theme.fontSize.sm,
    marginTop: theme.spacing.xs,
  },
  successText: {
    color: COLORS.success,
    fontSize: theme.fontSize.sm,
    marginTop: theme.spacing.xs,
  },
  divider: {
    height: 1,
    backgroundColor: COLORS.border,
    marginVertical: theme.spacing.md,
  },
  row: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  spaceBetween: {
    justifyContent: 'space-between',
  },
  center: {
    justifyContent: 'center',
    alignItems: 'center',
  },
  mb_sm: { marginBottom: theme.spacing.sm },
  mb_md: { marginBottom: theme.spacing.md },
  mb_lg: { marginBottom: theme.spacing.lg },
  mt_sm: { marginTop: theme.spacing.sm },
  mt_md: { marginTop: theme.spacing.md },
  mt_lg: { marginTop: theme.spacing.lg },
  p_md: { padding: theme.spacing.md },
  ph_md: { paddingHorizontal: theme.spacing.md },
  pv_md: { paddingVertical: theme.spacing.md },
});

export const { width: SCREEN_WIDTH, height: SCREEN_HEIGHT } = Dimensions.get('window');
