import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  StyleSheet,
  Alert,
  TextInput
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import UserAvatar from '../components/UserAvatar';
import { colors, spacing, chatStyles, globalStyles } from '../styles/theme';
import chatService from '../services/chatService';
import storageService from '../services/storageService';

const ProfileScreen = () => {
  const [currentUser, setCurrentUser] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const [editedUsername, setEditedUsername] = useState('');
  const [status, setStatus] = useState('online');

  useEffect(() => {
    loadCurrentUser();
  }, []);

  const loadCurrentUser = async () => {
    const user = await chatService.getCurrentUser();
    setCurrentUser(user);
    setEditedUsername(user?.username || '');
    setStatus(user?.status || 'online');
  };

  const handleSaveProfile = async () => {
    if (!editedUsername.trim()) {
      Alert.alert('Errore', 'Il nome utente non può essere vuoto');
      return;
    }

    await storageService.updateUser(currentUser.id, {
      username: editedUsername.trim()
    });

    setCurrentUser({
      ...currentUser,
      username: editedUsername.trim()
    });

    setIsEditing(false);
    Alert.alert('Successo', 'Profilo aggiornato!');
  };

  const handleStatusChange = async (newStatus) => {
    await chatService.updateUserStatus(currentUser.id, newStatus);
    setStatus(newStatus);
    setCurrentUser({
      ...currentUser,
      status: newStatus
    });
  };

  const handleClearAllData = () => {
    Alert.alert(
      'Cancella Tutti i Dati',
      'Sei sicuro di voler cancellare tutti i dati? Questa azione non può essere annullata.',
      [
        { text: 'Annulla', style: 'cancel' },
        {
          text: 'Cancella',
          style: 'destructive',
          onPress: async () => {
            await storageService.clearAllData();
            Alert.alert('Successo', 'Dati cancellati. Riavvia l\'applicazione.');
          }
        }
      ]
    );
  };

  const StatusOption = ({ label, value, icon }) => (
    <TouchableOpacity
      style={[styles.statusOption, status === value && styles.statusOptionActive]}
      onPress={() => handleStatusChange(value)}
    >
      <Ionicons
        name={icon}
        size={24}
        color={status === value ? colors.white : colors.textSecondary}
      />
      <Text style={[styles.statusOptionText, status === value && styles.statusOptionTextActive]}>
        {label}
      </Text>
    </TouchableOpacity>
  );

  const SettingItem = ({ icon, title, subtitle, onPress, color = colors.text }) => (
    <TouchableOpacity style={styles.settingItem} onPress={onPress}>
      <Ionicons name={icon} size={24} color={color} style={styles.settingIcon} />
      <View style={styles.settingContent}>
        <Text style={styles.settingTitle}>{title}</Text>
        {subtitle && <Text style={styles.settingSubtitle}>{subtitle}</Text>}
      </View>
      <Ionicons name="chevron-forward" size={20} color={colors.textLight} />
    </TouchableOpacity>
  );

  if (!currentUser) {
    return (
      <View style={chatStyles.loadingContainer}>
        <Text>Caricamento...</Text>
      </View>
    );
  }

  return (
    <ScrollView style={globalStyles.container}>
      {/* Profile Header */}
      <View style={styles.profileHeader}>
        <UserAvatar user={currentUser} size={100} />

        {isEditing ? (
          <View style={styles.editContainer}>
            <TextInput
              style={styles.editInput}
              value={editedUsername}
              onChangeText={setEditedUsername}
              placeholder="Nome utente"
              autoFocus
            />
            <View style={styles.editButtons}>
              <TouchableOpacity
                style={[styles.editButton, styles.cancelButton]}
                onPress={() => {
                  setIsEditing(false);
                  setEditedUsername(currentUser.username);
                }}
              >
                <Ionicons name="close" size={20} color={colors.white} />
              </TouchableOpacity>
              <TouchableOpacity
                style={[styles.editButton, styles.saveButton]}
                onPress={handleSaveProfile}
              >
                <Ionicons name="checkmark" size={20} color={colors.white} />
              </TouchableOpacity>
            </View>
          </View>
        ) : (
          <>
            <Text style={styles.profileName}>{currentUser.username}</Text>
            <Text style={styles.profileId}>ID: {currentUser.id}</Text>
            <TouchableOpacity
              style={styles.editProfileButton}
              onPress={() => setIsEditing(true)}
            >
              <Ionicons name="create-outline" size={20} color={colors.primary} />
              <Text style={styles.editProfileText}>Modifica Profilo</Text>
            </TouchableOpacity>
          </>
        )}
      </View>

      {/* Status Section */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Stato</Text>
        <View style={styles.statusContainer}>
          <StatusOption label="Online" value="online" icon="radio-button-on" />
          <StatusOption label="Away" value="away" icon="time" />
          <StatusOption label="Offline" value="offline" icon="radio-button-off" />
        </View>
      </View>

      {/* Settings Section */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Impostazioni</Text>

        <SettingItem
          icon="notifications"
          title="Notifiche"
          subtitle="Attive (simulato)"
        />

        <SettingItem
          icon="lock-closed"
          title="Privacy"
          subtitle="Chi può vedere il tuo stato"
        />

        <SettingItem
          icon="chatbubble"
          title="Chat"
          subtitle="Impostazioni messaggi"
        />

        <SettingItem
          icon="color-palette"
          title="Tema"
          subtitle="Chiaro (predefinito)"
        />
      </View>

      {/* Danger Zone */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Altro</Text>

        <SettingItem
          icon="information-circle"
          title="Informazioni"
          subtitle="Versione 1.0.0"
        />

        <SettingItem
          icon="trash"
          title="Cancella Dati"
          subtitle="Rimuovi tutti i dati locali"
          color={colors.error}
          onPress={handleClearAllData}
        />
      </View>

      {/* Footer */}
      <View style={styles.footer}>
        <Text style={styles.footerText}>Chat App v1.0.0</Text>
        <Text style={styles.footerText}>Real-time messaging con React Native</Text>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  profileHeader: {
    alignItems: 'center',
    padding: spacing.xl,
    backgroundColor: colors.white,
    borderBottomWidth: 1,
    borderBottomColor: colors.divider
  },
  profileName: {
    fontSize: 24,
    fontWeight: 'bold',
    color: colors.text,
    marginTop: spacing.md
  },
  profileId: {
    fontSize: 14,
    color: colors.textLight,
    marginTop: spacing.xs
  },
  editProfileButton: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: spacing.md,
    padding: spacing.sm
  },
  editProfileText: {
    fontSize: 14,
    color: colors.primary,
    marginLeft: spacing.xs
  },
  editContainer: {
    width: '100%',
    marginTop: spacing.md
  },
  editInput: {
    width: '100%',
    height: 48,
    borderWidth: 1,
    borderColor: colors.divider,
    borderRadius: 8,
    paddingHorizontal: spacing.md,
    fontSize: 16,
    color: colors.text
  },
  editButtons: {
    flexDirection: 'row',
    justifyContent: 'center',
    marginTop: spacing.md
  },
  editButton: {
    width: 48,
    height: 48,
    borderRadius: 24,
    justifyContent: 'center',
    alignItems: 'center',
    marginHorizontal: spacing.sm
  },
  saveButton: {
    backgroundColor: colors.primary
  },
  cancelButton: {
    backgroundColor: colors.textLight
  },
  section: {
    marginTop: spacing.md,
    backgroundColor: colors.white,
    borderTopWidth: 1,
    borderBottomWidth: 1,
    borderColor: colors.divider
  },
  sectionTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: colors.textSecondary,
    paddingHorizontal: spacing.md,
    paddingTop: spacing.md,
    paddingBottom: spacing.sm
  },
  statusContainer: {
    flexDirection: 'row',
    padding: spacing.md
  },
  statusOption: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    padding: spacing.md,
    marginHorizontal: spacing.xs,
    borderRadius: 8,
    backgroundColor: colors.backgroundLight
  },
  statusOptionActive: {
    backgroundColor: colors.primary
  },
  statusOptionText: {
    fontSize: 12,
    color: colors.textSecondary,
    marginLeft: spacing.xs
  },
  statusOptionTextActive: {
    color: colors.white
  },
  settingItem: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: spacing.md,
    borderBottomWidth: 1,
    borderBottomColor: colors.divider
  },
  settingIcon: {
    marginRight: spacing.md
  },
  settingContent: {
    flex: 1
  },
  settingTitle: {
    fontSize: 16,
    color: colors.text
  },
  settingSubtitle: {
    fontSize: 14,
    color: colors.textSecondary,
    marginTop: 2
  },
  footer: {
    alignItems: 'center',
    padding: spacing.xl,
    marginTop: spacing.md
  },
  footerText: {
    fontSize: 12,
    color: colors.textLight,
    marginBottom: spacing.xs
  }
});

export default ProfileScreen;
