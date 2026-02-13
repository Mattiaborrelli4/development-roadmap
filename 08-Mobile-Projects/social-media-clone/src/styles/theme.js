import { StyleSheet } from 'react-native';
import { THEME } from '../utils/constants';

export const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: THEME.colors.background,
  },
  centerContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: THEME.colors.background,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: THEME.spacing.lg,
    paddingVertical: THEME.spacing.md,
    borderBottomWidth: 1,
    borderBottomColor: THEME.colors.border,
    backgroundColor: THEME.colors.background,
  },
  headerTitle: {
    fontSize: THEME.fontSize.xl,
    fontWeight: 'bold',
    color: THEME.colors.text,
  },
  content: {
    flex: 1,
    backgroundColor: THEME.colors.background,
  },
  text: {
    fontSize: THEME.fontSize.md,
    color: THEME.colors.text,
  },
  textSecondary: {
    fontSize: THEME.fontSize.md,
    color: THEME.colors.textSecondary,
  },
  button: {
    backgroundColor: THEME.colors.primary,
    paddingHorizontal: THEME.spacing.xl,
    paddingVertical: THEME.spacing.md,
    borderRadius: THEME.colors.borderRadius.sm,
    alignItems: 'center',
    justifyContent: 'center',
  },
  buttonText: {
    color: '#fff',
    fontSize: THEME.fontSize.md,
    fontWeight: '600',
  },
  input: {
    borderWidth: 1,
    borderColor: THEME.colors.border,
    borderRadius: THEME.borderRadius.sm,
    paddingHorizontal: THEME.spacing.md,
    paddingVertical: THEME.spacing.sm,
    fontSize: THEME.fontSize.md,
    color: THEME.colors.text,
  },
  avatar: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: THEME.colors.backgroundSecondary,
  },
  avatarLarge: {
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: THEME.colors.backgroundSecondary,
  },
  username: {
    fontSize: THEME.fontSize.md,
    fontWeight: '600',
    color: THEME.colors.text,
  },
  caption: {
    fontSize: THEME.fontSize.md,
    color: THEME.colors.text,
    lineHeight: 20,
  },
  timestamp: {
    fontSize: THEME.fontSize.xs,
    color: THEME.colors.textSecondary,
    marginTop: THEME.spacing.xs,
  },
  divider: {
    height: 1,
    backgroundColor: THEME.colors.border,
    marginVertical: THEME.spacing.md,
  },
  emptyContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: THEME.spacing.xl,
  },
  emptyText: {
    fontSize: THEME.fontSize.lg,
    color: THEME.colors.textSecondary,
    marginTop: THEME.spacing.md,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
});

export default styles;
