import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TextInput,
  TouchableOpacity,
  ScrollView,
  Alert,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { useNavigation } from '@react-navigation/native';
import { useAuth } from '../hooks/useAuth';
import { THEME } from '../utils/constants';

const EditProfileScreen = () => {
  const navigation = useNavigation();
  const { user, updateUser } = useAuth();

  const [formData, setFormData] = useState({
    username: user?.username || '',
    bio: user?.bio || '',
    email: 'mattia@example.com',
    phone: '+39 123 456 7890',
  });

  const handleSave = async () => {
    if (!formData.username.trim()) {
      Alert.alert('Errore', 'Il nome utente è obbligatorio');
      return;
    }

    try {
      await updateUser({
        username: formData.username,
        bio: formData.bio,
      });
      navigation.goBack();
    } catch (error) {
      console.error('Errore salvataggio:', error);
      Alert.alert('Errore', 'Impossibile salvare le modifiche');
    }
  };

  const handleChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      {/* Header */}
      <View style={styles.header}>
        <TouchableOpacity onPress={() => navigation.goBack()}>
          <Ionicons name="close" size={24} color={THEME.colors.text} />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Modifica profilo</Text>
        <TouchableOpacity onPress={handleSave}>
          <Text style={styles.saveButton}>Salva</Text>
        </TouchableOpacity>
      </View>

      <ScrollView style={styles.content}>
        {/* Avatar Section */}
        <View style={styles.avatarSection}>
          <View style={styles.avatarContainer}>
            <Ionicons name="person" size={64} color={THEME.colors.textSecondary} />
          </View>
          <TouchableOpacity style={styles.changePhotoButton}>
            <Text style={styles.changePhotoText}>Cambia foto profilo</Text>
          </TouchableOpacity>
        </View>

        {/* Form Fields */}
        <View style={styles.formContainer}>
          <View style={styles.fieldContainer}>
            <Text style={styles.fieldLabel}>Nome utente</Text>
            <TextInput
              style={styles.fieldInput}
              value={formData.username}
              onChangeText={(text) => handleChange('username', text)}
              autoCapitalize="none"
              autoCorrect={false}
            />
          </View>

          <View style={styles.fieldContainer}>
            <Text style={styles.fieldLabel}>Biografia</Text>
            <TextInput
              style={[styles.fieldInput, styles.textArea]}
              value={formData.bio}
              onChangeText={(text) => handleChange('bio', text)}
              multiline
              maxLength={150}
              textAlignVertical="top"
            />
            <Text style={styles.charCount}>
              {formData.bio.length}/150
            </Text>
          </View>

          <View style={styles.fieldContainer}>
            <Text style={styles.fieldLabel}>Email</Text>
            <TextInput
              style={styles.fieldInput}
              value={formData.email}
              onChangeText={(text) => handleChange('email', text)}
              autoCapitalize="none"
              autoCorrect={false}
              keyboardType="email-address"
            />
          </View>

          <View style={styles.fieldContainer}>
            <Text style={styles.fieldLabel}>Telefono</Text>
            <TextInput
              style={styles.fieldInput}
              value={formData.phone}
              onChangeText={(text) => handleChange('phone', text)}
              keyboardType="phone-pad"
            />
          </View>
        </View>

        {/* Additional Options */}
        <View style={styles.optionsContainer}>
          <TouchableOpacity style={styles.option}>
            <Text style={styles.optionText}>Impostazioni personali</Text>
            <Ionicons name="chevron-forward" size={20} color={THEME.colors.textSecondary} />
          </TouchableOpacity>

          <TouchableOpacity style={styles.option}>
            <Text style={styles.optionText}>Account privato</Text>
            <View style={styles.toggle}>
              <View style={[styles.toggleKnob, styles.toggleInactive]} />
            </View>
          </TouchableOpacity>
        </View>

        {/* Danger Zone */}
        <View style={styles.dangerZone}>
          <TouchableOpacity style={styles.dangerButton}>
            <Text style={styles.dangerButtonText}>Disattiva account</Text>
          </TouchableOpacity>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: THEME.colors.background,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: THEME.colors.border,
  },
  headerTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: THEME.colors.text,
  },
  saveButton: {
    fontSize: 16,
    fontWeight: '600',
    color: THEME.colors.primary,
  },
  content: {
    flex: 1,
  },
  avatarSection: {
    alignItems: 'center',
    paddingVertical: 24,
    borderBottomWidth: 1,
    borderBottomColor: THEME.colors.border,
  },
  avatarContainer: {
    width: 86,
    height: 86,
    borderRadius: 43,
    backgroundColor: THEME.colors.backgroundSecondary,
    justifyContent: 'center',
    alignItems: 'center',
  },
  changePhotoButton: {
    marginTop: 12,
  },
  changePhotoText: {
    fontSize: 14,
    fontWeight: '600',
    color: THEME.colors.primary,
  },
  formContainer: {
    paddingVertical: 16,
  },
  fieldContainer: {
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderBottomWidth: 1,
    borderBottomColor: THEME.colors.border,
  },
  fieldLabel: {
    fontSize: 12,
    color: THEME.colors.textSecondary,
    marginBottom: 8,
  },
  fieldInput: {
    fontSize: 14,
    color: THEME.colors.text,
    paddingVertical: 4,
  },
  textArea: {
    minHeight: 80,
  },
  charCount: {
    fontSize: 12,
    color: THEME.colors.textSecondary,
    textAlign: 'right',
    marginTop: 4,
  },
  optionsContainer: {
    borderTopWidth: 1,
    borderTopColor: THEME.colors.border,
  },
  option: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingVertical: 16,
    borderBottomWidth: 1,
    borderBottomColor: THEME.colors.border,
  },
  optionText: {
    fontSize: 16,
    color: THEME.colors.text,
  },
  toggle: {
    width: 44,
    height: 24,
    borderRadius: 12,
    backgroundColor: THEME.colors.border,
    padding: 2,
  },
  toggleKnob: {
    width: 20,
    height: 20,
    borderRadius: 10,
    backgroundColor: '#fff',
  },
  toggleInactive: {
    alignSelf: 'flex-start',
  },
  dangerZone: {
    marginTop: 32,
    paddingHorizontal: 16,
    paddingBottom: 32,
  },
  dangerButton: {
    paddingVertical: 12,
  },
  dangerButtonText: {
    fontSize: 16,
    color: THEME.colors.error,
  },
});

export default EditProfileScreen;
