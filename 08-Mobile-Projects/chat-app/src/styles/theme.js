import { StyleSheet, Dimensions } from 'react-native';

const { width, height } = Dimensions.get('window');

// Colori
export const colors = {
  primary: '#128C7E',       // WhatsApp green
  primaryDark: '#075E54',   // Darker green
  primaryLight: '#25D366', // Lighter green
  accent: '#34B7F1',        // Blue accent

  background: '#ECE5DD',    // Chat background
  backgroundLight: '#F0F0F0',
  white: '#FFFFFF',

  text: '#000000',
  textSecondary: '#666666',
  textLight: '#999999',

  messageSent: '#DCF8C6',  // Sent message bubble
  messageReceived: '#FFFFFF', // Received message bubble

  statusOnline: '#25D366',
  statusOffline: '#999999',
  statusAway: '#FFC107',

  error: '#DC3545',
  success: '#28A745',
  warning: '#FFC107',

  border: '#E0E0E0',
  divider: '#DDDDDD'
};

// Spaziature
export const spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32
};

// Font
export const typography = {
  h1: {
    fontSize: 32,
    fontWeight: 'bold',
    lineHeight: 40
  },
  h2: {
    fontSize: 24,
    fontWeight: 'bold',
    lineHeight: 32
  },
  h3: {
    fontSize: 20,
    fontWeight: '600',
    lineHeight: 28
  },
  h4: {
    fontSize: 18,
    fontWeight: '600',
    lineHeight: 24
  },
  body: {
    fontSize: 16,
    fontWeight: 'normal',
    lineHeight: 24
  },
  bodySmall: {
    fontSize: 14,
    fontWeight: 'normal',
    lineHeight: 20
  },
  caption: {
    fontSize: 12,
    fontWeight: 'normal',
    lineHeight: 16
  }
};

// Bordi
export const borderRadius = {
  sm: 4,
  md: 8,
  lg: 12,
  xl: 16,
  round: 999
};

// Ombre
export const shadows = {
  sm: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.18,
    shadowRadius: 1.0,
    elevation: 1
  },
  md: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.23,
    shadowRadius: 2.62,
    elevation: 4
  },
  lg: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.30,
    shadowRadius: 4.65,
    elevation: 8
  }
};

// Stili globali
export const globalStyles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.backgroundLight
  },
  scrollContainer: {
    flex: 1
  },
  safeArea: {
    flex: 1,
    backgroundColor: colors.backgroundLight
  },
  center: {
    justifyContent: 'center',
    alignItems: 'center'
  },
  row: {
    flexDirection: 'row',
    alignItems: 'center'
  },
  spaceBetween: {
    justifyContent: 'space-between'
  },
  shadow: shadows.md
});

// Stili specifici per chat
export const chatStyles = StyleSheet.create({
  // Lista chat
  chatItem: {
    flexDirection: 'row',
    padding: spacing.md,
    backgroundColor: colors.white,
    borderBottomWidth: 1,
    borderBottomColor: colors.divider
  },
  chatAvatar: {
    width: 56,
    height: 56,
    borderRadius: borderRadius.lg
  },
  chatInfo: {
    flex: 1,
    marginLeft: spacing.md,
    justifyContent: 'center'
  },
  chatName: {
    fontSize: 16,
    fontWeight: '600',
    color: colors.text
  },
  chatPreview: {
    fontSize: 14,
    color: colors.textSecondary,
    marginTop: spacing.xs
  },
  chatMeta: {
    alignItems: 'flex-end'
  },
  chatTime: {
    fontSize: 12,
    color: colors.textLight
  },
  unreadBadge: {
    minWidth: 20,
    height: 20,
    borderRadius: borderRadius.round,
    backgroundColor: colors.primaryLight,
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: spacing.sm,
    paddingHorizontal: 6
  },
  unreadText: {
    fontSize: 11,
    fontWeight: 'bold',
    color: colors.white
  },

  // Bolla messaggio
  messageBubble: {
    maxWidth: width * 0.75,
    padding: spacing.sm,
    borderRadius: borderRadius.lg,
    marginVertical: spacing.xs
  },
  messageSent: {
    backgroundColor: colors.messageSent,
    alignSelf: 'flex-end',
    borderBottomRightRadius: 4
  },
  messageReceived: {
    backgroundColor: colors.messageReceived,
    alignSelf: 'flex-start',
    borderBottomLeftRadius: 4,
    ...shadows.sm
  },
  messageText: {
    fontSize: 16,
    color: colors.text,
    lineHeight: 22
  },
  messageTime: {
    fontSize: 11,
    color: colors.textLight,
    marginTop: spacing.xs,
    textAlign: 'right'
  },
  messageMeta: {
    flexDirection: 'row',
    justifyContent: 'flex-end',
    alignItems: 'center',
    marginTop: spacing.xs
  },
  readReceipt: {
    fontSize: 12,
    color: colors.primary,
    marginRight: spacing.xs
  },

  // Header chat
  chatHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: spacing.sm,
    paddingVertical: spacing.xs,
    backgroundColor: colors.primary,
    elevation: 4
  },
  headerAvatar: {
    width: 40,
    height: 40,
    borderRadius: borderRadius.round,
    marginRight: spacing.sm
  },
  headerInfo: {
    flex: 1
  },
  headerName: {
    fontSize: 16,
    fontWeight: '600',
    color: colors.white
  },
  headerStatus: {
    fontSize: 12,
    color: colors.white
  },

  // Input
  chatInputContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: spacing.sm,
    paddingVertical: spacing.xs,
    backgroundColor: colors.backgroundLight,
    borderTopWidth: 1,
    borderTopColor: colors.divider
  },
  input: {
    flex: 1,
    height: 40,
    backgroundColor: colors.white,
    borderRadius: borderRadius.round,
    paddingHorizontal: spacing.md,
    marginHorizontal: spacing.sm,
    fontSize: 16
  },
  iconButton: {
    padding: spacing.sm
  },

  // Typing indicator
  typingContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: spacing.sm,
    paddingHorizontal: spacing.md
  },
  typingBubble: {
    backgroundColor: colors.white,
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.sm,
    borderRadius: borderRadius.lg,
    ...shadows.sm
  },
  typingText: {
    fontSize: 14,
    color: colors.textSecondary,
    fontStyle: 'italic'
  },
  typingDots: {
    flexDirection: 'row',
    marginLeft: spacing.sm
  },
  dot: {
    width: 6,
    height: 6,
    borderRadius: borderRadius.round,
    backgroundColor: colors.textLight,
    marginHorizontal: 2
  },

  // Online status
  onlineIndicator: {
    position: 'absolute',
    bottom: 2,
    right: 2,
    width: 14,
    height: 14,
    borderRadius: borderRadius.round,
    borderWidth: 2,
    borderColor: colors.white
  },

  // Avatar
  avatar: {
    justifyContent: 'center',
    alignItems: 'center'
  },
  avatarText: {
    fontSize: 20,
    fontWeight: '600',
    color: colors.white
  },

  // Empty state
  emptyContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: spacing.xl
  },
  emptyText: {
    fontSize: 16,
    color: colors.textSecondary,
    marginTop: spacing.md
  },

  // Loading
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center'
  }
});

export default {
  colors,
  spacing,
  typography,
  borderRadius,
  shadows,
  globalStyles,
  chatStyles
};
