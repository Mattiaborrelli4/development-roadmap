import React, { useState, useEffect } from 'react';
import {
  View,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Text,
  Switch,
  Alert,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { Colors, Spacing, Typography, BorderRadius } from '../styles/theme';
import { storageService } from '../services/storageService';
import { albumService } from '../services/albumService';
import { photoService } from '../services/photoService';

const SettingsScreen = ({ navigation }) => {
  const [settings, setSettings] = useState({
    viewMode: 'grid',
    sortBy: 'date',
    defaultFilter: 'none',
  });
  const [stats, setStats] = useState({
    totalAlbums: 0,
    totalPhotos: 0,
    photosInAlbums: 0,
    photosWithoutAlbum: 0,
  });

  useEffect(() => {
    loadSettings();
    loadStats();
  }, []);

  const loadSettings = async () => {
    const savedSettings = await storageService.getSettings();
    setSettings(savedSettings);
  };

  const loadStats = async () => {
    const data = await albumService.getAlbumStats();
    setStats(data);
  };

  const handleClearAllData = () => {
    Alert.alert(
      'Cancella Tutti i Dati',
      'Sei sicuro di voler cancellare tutte le foto e gli album? Questa azione non può essere annullata.',
      [
        { text: 'Annulla', style: 'cancel' },
        {
          text: 'Cancella',
          style: 'destructive',
          onPress: async () => {
            await storageService.clearAll();
            await loadStats();
            Alert.alert('Fatto', 'Tutti i dati sono stati cancellati');
          },
        },
      ]
    );
  };

  const SettingItem = ({ icon, title, value, onPress, switchValue, onSwitchChange }) => (
    <TouchableOpacity
      style={styles.settingItem}
      onPress={onPress}
      disabled={!onPress && !onSwitchChange}
      activeOpacity={onPress || onSwitchChange ? 0.7 : 1}
    >
      <View style={styles.settingLeft}>
        <View style={styles.settingIcon}>
          <Ionicons name={icon} size={24} color={Colors.primary} />
        </View>
        <Text style={styles.settingTitle}>{title}</Text>
      </View>

      {onSwitchChange !== undefined ? (
        <Switch
          value={switchValue}
          onValueChange={onSwitchChange}
          trackColor={{ false: Colors.border, true: Colors.primary }}
          thumbColor={Colors.background}
        />
      ) : value ? (
        <View style={styles.settingRight}>
          <Text style={styles.settingValue}>{value}</Text>
          <Ionicons name="chevron-forward" size={20} color={Colors.textSecondary} />
        </View>
      ) : null}
    </TouchableOpacity>
  );

  const Section = ({ title, children }) => (
    <View style={styles.section}>
      <Text style={styles.sectionTitle}>{title}</Text>
      <View style={styles.sectionContent}>
        {children}
      </View>
    </View>
  );

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <TouchableOpacity onPress={() => navigation.goBack()}>
          <Ionicons name="arrow-back" size={28} color={Colors.text} />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Impostazioni</Text>
        <View style={{ width: 28 }} />
      </View>

      <ScrollView style={styles.content}>
        {/* Statistics Section */}
        <Section title="Statistiche">
          <SettingItem
            icon="images"
            title="Foto Totali"
            value={stats.totalPhotos.toString()}
          />
          <SettingItem
            icon="albums"
            title="Album Totali"
            value={stats.totalAlbums.toString()}
          />
          <SettingItem
            icon="folder"
            title="Foto in Album"
            value={stats.photosInAlbums.toString()}
          />
          <SettingItem
            icon="image-outline"
            title="Foto senza Album"
            value={stats.photosWithoutAlbum.toString()}
          />
        </Section>

        {/* View Settings Section */}
        <Section title="Visualizzazione">
          <SettingItem
            icon="grid"
            title="Modalità Vista"
            value={settings.viewMode === 'grid' ? 'Griglia' : 'Lista'}
            onPress={() => {
              const newValue = settings.viewMode === 'grid' ? 'list' : 'grid';
              const newSettings = { ...settings, viewMode: newValue };
              setSettings(newSettings);
              storageService.saveSettings(newSettings);
            }}
          />
          <SettingItem
            icon="funnel"
            title="Ordina Per"
            value={settings.sortBy === 'date' ? 'Data' : settings.sortBy === 'name' ? 'Nome' : 'Dimensione'}
            onPress={() => {
              const options = ['date', 'name', 'size'];
              const currentIndex = options.indexOf(settings.sortBy);
              const nextIndex = (currentIndex + 1) % options.length;
              const newValue = options[nextIndex];
              const newSettings = { ...settings, sortBy: newValue };
              setSettings(newSettings);
              storageService.saveSettings(newSettings);
            }}
          />
        </Section>

        {/* Filter Settings Section */}
        <Section title="Filtri">
          <SettingItem
            icon="color-filter"
            title="Filtro Predefinito"
            value={settings.defaultFilter === 'none' ? 'Nessuno' : settings.defaultFilter}
          />
        </Section>

        {/* About Section */}
        <Section title="Informazioni">
          <SettingItem
            icon="information-circle"
            title="Versione"
            value="1.0.0"
          />
          <SettingItem
            icon="code"
            title="Framework"
            value="React Native + Expo"
          />
        </Section>

        {/* Danger Zone */}
        <Section title="Zona Pericolosa">
          <TouchableOpacity
            style={styles.dangerButton}
            onPress={handleClearAllData}
          >
            <Ionicons name="trash" size={24} color={Colors.danger} />
            <Text style={styles.dangerButtonText}>Cancella Tutti i Dati</Text>
          </TouchableOpacity>
        </Section>
      </ScrollView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.background,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: Spacing.md,
    borderBottomWidth: 1,
    borderBottomColor: Colors.border,
  },
  headerTitle: {
    ...Typography.title,
  },
  content: {
    flex: 1,
  },
  section: {
    marginTop: Spacing.lg,
  },
  sectionTitle: {
    ...Typography.small,
    color: Colors.textSecondary,
    textTransform: 'uppercase',
    letterSpacing: 1,
    marginLeft: Spacing.lg,
    marginBottom: Spacing.sm,
  },
  sectionContent: {
    backgroundColor: Colors.background,
    borderTopWidth: 1,
    borderBottomWidth: 1,
    borderBottomColor: Colors.border,
    borderTopColor: Colors.border,
  },
  settingItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: Spacing.md,
    paddingLeft: Spacing.lg,
    borderBottomWidth: 1,
    borderBottomColor: Colors.border,
  },
  settingLeft: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  settingIcon: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: Colors.backgroundSecondary,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: Spacing.md,
  },
  settingTitle: {
    ...Typography.body,
  },
  settingRight: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: Spacing.sm,
  },
  settingValue: {
    ...Typography.body,
    color: Colors.textSecondary,
  },
  dangerButton: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    padding: Spacing.lg,
    margin: Spacing.lg,
    backgroundColor: Colors.danger,
    borderRadius: BorderRadius.md,
    gap: Spacing.sm,
  },
  dangerButtonText: {
    ...Typography.body,
    color: Colors.background,
    fontWeight: '600',
  },
});

export default SettingsScreen;
