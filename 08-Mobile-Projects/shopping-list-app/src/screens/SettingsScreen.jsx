import React, {useState, useEffect} from 'react';
import {
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  StyleSheet,
  Switch,
  Alert,
} from 'react-native';
import storageService from '../services/storageService';
import syncService from '../services/syncService';
import {THEME} from '../utils/constants';

const SettingsScreen = ({navigation}) => {
  const [settings, setSettings] = useState({
    theme: 'light',
    notifications: true,
    autoSort: true,
  });
  const [statistics, setStatistics] = useState(null);
  const [syncStatus, setSyncStatus] = useState(syncService.getSyncStatus());

  useEffect(() => {
    loadSettings();
    loadStatistics();
  }, []);

  const loadSettings = async () => {
    const loadedSettings = await storageService.getSettings();
    setSettings(loadedSettings);
  };

  const loadStatistics = async () => {
    const stats = await storageService.getStatistics();
    setStatistics(stats);
  };

  const handleSettingChange = async (key, value) => {
    const newSettings = {...settings, [key]: value};
    setSettings(newSettings);
    await storageService.saveSettings(newSettings);
  };

  const handleSync = async () => {
    const result = await syncService.sync();
    if (result.success) {
      Alert.alert('Successo', result.message);
    } else {
      Alert.alert('Errore', result.message);
    }
    setSyncStatus(syncService.getSyncStatus());
  };

  const handleClearData = () => {
    Alert.alert(
      'Pulisci Dati',
      'Sei sicuro di voler eliminare tutti i dati? Questa azione è irreversibile.',
      [
        {text: 'Annulla', style: 'cancel'},
        {
          text: 'Elimina Tutto',
          style: 'destructive',
          onPress: async () => {
            await storageService.clearAll();
            Alert.alert('Successo', 'Tutti i dati sono stati eliminati');
            loadStatistics();
          },
        },
      ]
    );
  };

  const renderStatistics = () => {
    if (!statistics) return null;

    return (
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>📊 Statistiche</Text>

        <View style={styles.statsContainer}>
          <View style={styles.statItem}>
            <Text style={styles.statValue}>{statistics.totalLists}</Text>
            <Text style={styles.statLabel}>Liste</Text>
          </View>
          <View style={styles.statItem}>
            <Text style={styles.statValue}>{statistics.totalItems}</Text>
            <Text style={styles.statLabel}>Elementi</Text>
          </View>
          <View style={styles.statItem}>
            <Text style={styles.statValue}>{statistics.boughtItems}</Text>
            <Text style={styles.statLabel}>Comprati</Text>
          </View>
          <View style={styles.statItem}>
            <Text style={styles.statValue}>{statistics.sharedLists}</Text>
            <Text style={styles.statLabel}>Condivise</Text>
          </View>
        </View>

        <View style={styles.completionRate}>
          <Text style={styles.completionRateLabel}>Tasso di Completamento</Text>
          <Text style={styles.completionRateValue}>{statistics.completionRate}%</Text>
        </View>
      </View>
    );
  };

  return (
    <ScrollView style={styles.container}>
      {/* Statistics Section */}
      {renderStatistics()}

      {/* Appearance Section */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>🎨 Aspetto</Text>

        <TouchableOpacity
          style={styles.settingItem}
          onPress={() => navigation.navigate('ThemeSettings')}>
          <View style={styles.settingInfo}>
            <Text style={styles.settingLabel}>Tema</Text>
            <Text style={styles.settingValue}>
              {settings.theme === 'light' ? '☀️ Chiaro' : '🌙 Scuro'}
            </Text>
          </View>
          <Text style={styles.chevron}>›</Text>
        </TouchableOpacity>
      </View>

      {/* Preferences Section */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>⚙️ Preferenze</Text>

        <View style={styles.settingItem}>
          <View style={styles.settingInfo}>
            <Text style={styles.settingLabel}>Notifiche</Text>
            <Text style={styles.settingDescription}>
              Ricevi promemoria per la spesa
            </Text>
          </View>
          <Switch
            value={settings.notifications}
            onValueChange={value => handleSettingChange('notifications', value)}
            trackColor={{false: '#E0E0E0', true: '#4ECDC4'}}
            thumbColor="#FFFFFF"
          />
        </View>

        <View style={styles.settingItem}>
          <View style={styles.settingInfo}>
            <Text style={styles.settingLabel}>Ordinamento Automatico</Text>
            <Text style={styles.settingDescription}>
              Raggruppa gli elementi per categoria
            </Text>
          </View>
          <Switch
            value={settings.autoSort}
            onValueChange={value => handleSettingChange('autoSort', value)}
            trackColor={{false: '#E0E0E0', true: '#4ECDC4'}}
            thumbColor="#FFFFFF"
          />
        </View>
      </View>

      {/* Sync Section */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>☁️ Sincronizzazione</Text>

        <TouchableOpacity style={styles.settingItem} onPress={handleSync}>
          <View style={styles.settingInfo}>
            <Text style={styles.settingLabel}>Sincronizza Ora</Text>
            <Text style={styles.settingValue}>
              {syncStatus.lastSync
                ? `Ultimo: ${new Date(syncStatus.lastSync).toLocaleString('it-IT')}`
                : 'Mai sincronizzato'}
            </Text>
          </View>
          <View style={styles.syncButton}>
            <Text style={styles.syncButtonText}>
              {syncStatus.inProgress ? '⏳' : '🔄'}
            </Text>
          </View>
        </TouchableOpacity>

        <View style={styles.infoBox}>
          <Text style={styles.infoText}>
            ℹ️ La sincronizzazione è simulata per dimostrazione. In un'app
            reale, i dati verrebbero sincronizzati con un server cloud.
          </Text>
        </View>
      </View>

      {/* Data Management Section */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>💾 Gestione Dati</Text>

        <TouchableOpacity
          style={styles.settingItem}
          onPress={() => {
            navigation.navigate('ImportExport');
          }}>
          <View style={styles.settingInfo}>
            <Text style={styles.settingLabel}>Importa/Esporta Dati</Text>
            <Text style={styles.settingDescription}>
              Backup e ripristino delle liste
            </Text>
          </View>
          <Text style={styles.chevron}>›</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={[styles.settingItem, styles.dangerItem]}
          onPress={handleClearData}>
          <View style={styles.settingInfo}>
            <Text style={[styles.settingLabel, styles.dangerText]}>
              Elimina Tutti i Dati
            </Text>
            <Text style={styles.settingDescription}>
              Rimuovi tutte le liste e gli elementi
            </Text>
          </View>
          <Text style={styles.dangerIcon}>🗑️</Text>
        </TouchableOpacity>
      </View>

      {/* About Section */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>ℹ️ Info</Text>

        <View style={styles.settingItem}>
          <View style={styles.settingInfo}>
            <Text style={styles.settingLabel}>Versione</Text>
            <Text style={styles.settingValue}>1.0.0</Text>
          </View>
        </View>

        <TouchableOpacity
          style={styles.settingItem}
          onPress={() => {
            Alert.alert(
              'Lista della Spesa',
              'App per gestire le liste della spesa condivise con la famiglia.\n\nSviluppata con React Native ed Expo.'
            );
          }}>
          <View style={styles.settingInfo}>
            <Text style={styles.settingLabel}>Info App</Text>
          </View>
          <Text style={styles.chevron}>›</Text>
        </TouchableOpacity>
      </View>

      <View style={styles.footer}>
        <Text style={styles.footerText}>
          Creato con ❤️ usando React Native
        </Text>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F5F5',
  },
  section: {
    backgroundColor: '#FFFFFF',
    marginTop: 16,
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#E0E0E0',
    borderTopWidth: 1,
    borderTopColor: '#E0E0E0',
  },
  sectionTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: '#7F8C8D',
    marginBottom: 12,
    textTransform: 'uppercase',
  },
  statsContainer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    paddingVertical: 16,
  },
  statItem: {
    alignItems: 'center',
  },
  statValue: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#4ECDC4',
  },
  statLabel: {
    fontSize: 12,
    color: '#7F8C8D',
    marginTop: 4,
  },
  completionRate: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 16,
    backgroundColor: '#F5F5F5',
    borderRadius: 8,
    marginTop: 8,
  },
  completionRateLabel: {
    fontSize: 16,
    color: '#2C3E50',
  },
  completionRateValue: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#4CAF50',
  },
  settingItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#F0F0F0',
  },
  settingInfo: {
    flex: 1,
  },
  settingLabel: {
    fontSize: 16,
    fontWeight: '500',
    color: '#2C3E50',
    marginBottom: 2,
  },
  settingValue: {
    fontSize: 14,
    color: '#7F8C8D',
  },
  settingDescription: {
    fontSize: 12,
    color: '#95A5A6',
  },
  chevron: {
    fontSize: 24,
    color: '#BDC3C7',
  },
  syncButton: {
    padding: 8,
  },
  syncButtonText: {
    fontSize: 20,
  },
  dangerItem: {
    // No special styling, using dangerText instead
  },
  dangerText: {
    color: '#F44336',
  },
  dangerIcon: {
    fontSize: 20,
  },
  infoBox: {
    backgroundColor: '#E3F2FD',
    borderRadius: 8,
    padding: 12,
    marginTop: 8,
    borderLeftWidth: 4,
    borderLeftColor: '#2196F3',
  },
  infoText: {
    fontSize: 12,
    color: '#1976D2',
    lineHeight: 18,
  },
  footer: {
    padding: 32,
    alignItems: 'center',
  },
  footerText: {
    fontSize: 12,
    color: '#95A5A6',
  },
});

export default SettingsScreen;
