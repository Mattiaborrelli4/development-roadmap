import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  SafeAreaView,
  TouchableOpacity,
  Alert,
} from 'react-native';
import { theme } from '../styles/theme';
import workoutService from '../services/workoutService';
import sensorService from '../services/sensorService';

const SettingsScreen = ({ navigation }) => {
  const handleResetData = () => {
    Alert.alert(
      'Resetta Dati',
      'Sei sicuro di voler eliminare tutti i dati? Questa azione non può essere annullata.',
      [
        { text: 'Annulla', style: 'cancel' },
        {
          text: 'Elimina',
          style: 'destructive',
          onPress: async () => {
            await workoutService.resetAllData();
            await sensorService.resetSteps();
            Alert.alert('Successo', 'Tutti i dati sono stati eliminati');
          }
        }
      ]
    );
  };

  const SettingItem = ({ title, description, onPress, showArrow = true, danger = false }) => (
    <TouchableOpacity
      style={[styles.settingItem, danger && styles.settingItemDanger]}
      onPress={onPress}
      activeOpacity={0.7}
    >
      <View style={styles.settingContent}>
        <Text style={[styles.settingTitle, danger && styles.settingTitleDanger]}>
          {title}
        </Text>
        {description && (
          <Text style={styles.settingDescription}>{description}</Text>
        )}
      </View>
      {showArrow && <Text style={styles.settingArrow}>›</Text>}
    </TouchableOpacity>
  );

  const Section = ({ title, children }) => (
    <View style={styles.section}>
      <Text style={styles.sectionTitle}>{title}</Text>
      <View style={styles.sectionContent}>{children}</View>
    </View>
  );

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => navigation.goBack()}>
          <Text style={styles.backButton}>‹ Indietro</Text>
        </TouchableOpacity>
        <Text style={styles.title}>Impostazioni</Text>
        <View style={{ width: 60 }} />
      </View>

      <ScrollView showsVerticalScrollIndicator={false}>
        {/* Account Section */}
        <Section title="PROFILO">
          <SettingItem
            title="Informazioni Personali"
            description="Gestisci il tuo profilo"
            onPress={() => {}}
          />
          <SettingItem
            title="Peso Corporeo"
            description="Usato per calcolare le calorie"
            onPress={() => {}}
          />
        </Section>

        {/* Goals Section */}
        <Section title="OBIETTIVI">
          <SettingItem
            title="Obiettivi Predefiniti"
            description="Ripristina gli obiettivi iniziali"
            onPress={() => {
              Alert.alert(
                'Reset Obiettivi',
                'Ripristinare gli obiettivi ai valori predefiniti?',
                [
                  { text: 'Annulla', style: 'cancel' },
                  {
                    text: 'Ripristina',
                    onPress: async () => {
                      Alert.alert('Info', 'Funzionalità di ripristino obiettivi');
                    }
                  }
                ]
              );
            }}
          />
        </Section>

        {/* Data Section */}
        <Section title="DATI">
          <SettingItem
            title="Esporta Dati"
            description="Esporta tutti i tuoi dati"
            onPress={() => {
              Alert.alert('Info', 'Funzionalità di esportazione dati');
            }}
          />
          <SettingItem
            title="Importa Dati"
            description="Importa dati da un backup"
            onPress={() => {
              Alert.alert('Info', 'Funzionalità di importazione dati');
            }}
          />
          <SettingItem
            title="Elimina Tutti i Dati"
            description="Rimuovi permanentemente tutti i dati"
            onPress={handleResetData}
            danger
          />
        </Section>

        {/* App Info Section */}
        <Section title="INFO APP">
          <SettingItem
            title="Versione"
            description="1.0.0"
            showArrow={false}
          />
          <SettingItem
            title="Librerie Utilizzate"
            description="React Native, Expo, Victory Native"
            showArrow={false}
          />
        </Section>

        {/* About Section */}
        <Section title="ALTRO">
          <SettingItem
            title="Guida"
            description="Come usare l'app"
            onPress={() => {
              Alert.alert(
                'Guida',
                '• Dashboard: Visualizza i passi e le statistiche del giorno\n' +
                '• Allenamenti: Aggiungi e gestisci i tuoi allenamenti\n' +
                '• Progressi: Analizza i tuoi progressi settimanali\n' +
                '• Obiettivi: Imposta e traccia i tuoi obiettivi'
              );
            }}
          />
          <SettingItem
            title="Privacy Policy"
            description="Come gestiamo i tuoi dati"
            onPress={() => {
              Alert.alert(
                'Privacy',
                'Tutti i dati sono salvati localmente sul dispositivo. ' +
                'Nessun dato viene inviato a server esterni.'
              );
            }}
          />
          <SettingItem
            title="Contatti"
            description="Supporto e feedback"
            onPress={() => {
              Alert.alert('Contatti', 'Per supporto, contatta lo sviluppatore.');
            }}
          />
        </Section>

        <View style={styles.footer}>
          <Text style={styles.footerText}>
            Fitness Tracker App
          </Text>
          <Text style={styles.footerSubtext}>
            Sviluppato con ❤️ usando React Native
          </Text>
        </View>

        <View style={{ height: 40 }} />
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: theme.colors.background,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: theme.spacing.lg,
    paddingTop: theme.spacing.lg,
    borderBottomWidth: 1,
    borderBottomColor: theme.colors.border,
  },
  backButton: {
    fontSize: theme.fontSize.lg,
    color: theme.colors.primary,
    width: 60,
  },
  title: {
    fontSize: theme.fontSize.xl,
    fontWeight: 'bold',
    color: theme.colors.text,
    flex: 1,
    textAlign: 'center',
  },
  section: {
    marginTop: theme.spacing.lg,
  },
  sectionTitle: {
    fontSize: theme.fontSize.sm,
    fontWeight: '600',
    color: theme.colors.textSecondary,
    marginLeft: theme.spacing.lg,
    marginBottom: theme.spacing.sm,
    textTransform: 'uppercase',
  },
  sectionContent: {
    backgroundColor: theme.colors.surface,
    borderTopWidth: 1,
    borderBottomWidth: 1,
    borderColor: theme.colors.border,
  },
  settingItem: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: theme.spacing.lg,
    borderBottomWidth: 1,
    borderBottomColor: theme.colors.border,
  },
  settingItemDanger: {
    backgroundColor: `${theme.colors.danger}10`,
  },
  settingContent: {
    flex: 1,
  },
  settingTitle: {
    fontSize: theme.fontSize.md,
    fontWeight: '500',
    color: theme.colors.text,
    marginBottom: theme.spacing.xs,
  },
  settingTitleDanger: {
    color: theme.colors.danger,
  },
  settingDescription: {
    fontSize: theme.fontSize.sm,
    color: theme.colors.textSecondary,
  },
  settingArrow: {
    fontSize: 24,
    color: theme.colors.textSecondary,
  },
  footer: {
    alignItems: 'center',
    padding: theme.spacing.xl,
    marginTop: theme.spacing.xl,
  },
  footerText: {
    fontSize: theme.fontSize.md,
    fontWeight: '600',
    color: theme.colors.text,
  },
  footerSubtext: {
    fontSize: theme.fontSize.sm,
    color: theme.colors.textSecondary,
    marginTop: theme.spacing.xs,
  },
});

export default SettingsScreen;
