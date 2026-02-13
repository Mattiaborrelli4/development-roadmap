import React, {useState} from 'react';
import {
  View,
  Text,
  Modal,
  TouchableOpacity,
  TextInput,
  StyleSheet,
  Alert,
} from 'react-native';

const ShareButton = ({list, onShare, onUnshare}) => {
  const [visible, setVisible] = useState(false);
  const [email, setEmail] = useState('');

  const handleShare = async () => {
    if (!email.trim()) {
      Alert.alert('Errore', 'Inserisci un indirizzo email');
      return;
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email.trim())) {
      Alert.alert('Errore', 'Inserisci un indirizzo email valido');
      return;
    }

    try {
      await onShare(list.id, email.trim());
      Alert.alert('Successo', `Lista condivisa con ${email}`);
      setEmail('');
      setVisible(false);
    } catch (error) {
      Alert.alert('Errore', 'Impossibile condividere la lista');
    }
  };

  const handleUnshare = async (sharedUser) => {
    Alert.alert(
      'Revoca condivisione',
      `Revocare la condivisione con ${sharedUser.email}?`,
      [
        {text: 'Annulla', style: 'cancel'},
        {
          text: 'Revoca',
          style: 'destructive',
          onPress: async () => {
            try {
              await onUnshare(list.id, sharedUser.email);
              Alert.alert('Successo', 'Condivisione revocata');
            } catch (error) {
              Alert.alert('Errore', 'Impossibile revocare la condivisione');
            }
          },
        },
      ]
    );
  };

  return (
    <>
      <TouchableOpacity
        style={styles.button}
        onPress={() => setVisible(true)}>
        <Text style={styles.icon}>{list.shared ? '👥' : '🔒'}</Text>
        <Text style={styles.text}>
          {list.shared ? 'Condivisa' : 'Condividi'}
        </Text>
      </TouchableOpacity>

      <Modal
        visible={visible}
        animationType="slide"
        transparent
        onRequestClose={() => setVisible(false)}>
        <TouchableOpacity
          style={styles.modalOverlay}
          activeOpacity={1}
          onPress={() => setVisible(false)}>
          <TouchableOpacity
            style={styles.modalContainer}
            activeOpacity={1}
            onPress={() => {}}>
            <View style={styles.header}>
              <Text style={styles.title}>Condividi Lista</Text>
              <TouchableOpacity onPress={() => setVisible(false)}>
                <Text style={styles.closeButton}>✕</Text>
              </TouchableOpacity>
            </View>

            <View style={styles.content}>
              <View style={styles.info}>
                <Text style={styles.listName}>{list.name}</Text>
                <Text style={styles.listIcon}>{list.icon}</Text>
              </View>

              {list.sharedWith && list.sharedWith.length > 0 && (
                <View style={styles.sharedWithSection}>
                  <Text style={styles.sectionTitle}>
                    Condivisa con:
                  </Text>
                  {list.sharedWith.map((user, index) => (
                    <TouchableOpacity
                      key={index}
                      style={styles.sharedUser}
                      onPress={() => handleUnshare(user)}>
                      <Text style={styles.sharedUserEmail}>
                        {user.email}
                      </Text>
                      <Text style={styles.removeButton}>Rimuovi</Text>
                    </TouchableOpacity>
                  ))}
                </View>
              )}

              <View style={styles.inputSection}>
                <Text style={styles.sectionTitle}>
                  Condividi con nuovo membro:
                </Text>
                <TextInput
                  style={styles.input}
                  value={email}
                  onChangeText={setEmail}
                  placeholder="email@esempio.com"
                  keyboardType="email-address"
                  autoCapitalize="none"
                />
                <TouchableOpacity
                  style={styles.shareButton}
                  onPress={handleShare}>
                  <Text style={styles.shareButtonText}>
                    Invita
                  </Text>
                </TouchableOpacity>
              </View>

              <View style={styles.note}>
                <Text style={styles.noteText}>
                  ℹ️ La condivisione è simulata per dimostrazione
                </Text>
              </View>
            </View>
          </TouchableOpacity>
        </TouchableOpacity>
      </Modal>
    </>
  );
};

const styles = StyleSheet.create({
  button: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 8,
    paddingHorizontal: 16,
    borderRadius: 8,
    backgroundColor: '#F5F5F5',
    borderWidth: 1,
    borderColor: '#E0E0E0',
  },
  icon: {
    fontSize: 16,
    marginRight: 8,
  },
  text: {
    fontSize: 14,
    fontWeight: '600',
    color: '#2C3E50',
  },
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  modalContainer: {
    backgroundColor: '#FFFFFF',
    borderRadius: 20,
    width: '90%',
    maxWidth: 400,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 20,
    borderBottomWidth: 1,
    borderBottomColor: '#E0E0E0',
  },
  title: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2C3E50',
  },
  closeButton: {
    fontSize: 24,
    color: '#7F8C8D',
  },
  content: {
    padding: 20,
  },
  info: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 16,
    backgroundColor: '#F5F5F5',
    borderRadius: 12,
    marginBottom: 20,
  },
  listName: {
    fontSize: 16,
    fontWeight: '600',
    color: '#2C3E50',
  },
  listIcon: {
    fontSize: 32,
  },
  sharedWithSection: {
    marginBottom: 20,
  },
  sectionTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: '#2C3E50',
    marginBottom: 12,
  },
  sharedUser: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 12,
    backgroundColor: '#F5F5F5',
    borderRadius: 8,
    marginBottom: 8,
  },
  sharedUserEmail: {
    fontSize: 14,
    color: '#2C3E50',
    flex: 1,
  },
  removeButton: {
    fontSize: 12,
    color: '#F44336',
    fontWeight: '600',
  },
  inputSection: {
    marginBottom: 20,
  },
  input: {
    backgroundColor: '#F5F5F5',
    borderRadius: 8,
    padding: 12,
    fontSize: 16,
    color: '#2C3E50',
    borderWidth: 1,
    borderColor: '#E0E0E0',
    marginBottom: 12,
  },
  shareButton: {
    backgroundColor: '#4ECDC4',
    borderRadius: 8,
    padding: 12,
    alignItems: 'center',
  },
  shareButtonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: '600',
  },
  note: {
    padding: 12,
    backgroundColor: '#FFF3CD',
    borderRadius: 8,
    borderLeftWidth: 4,
    borderLeftColor: '#FFC107',
  },
  noteText: {
    fontSize: 12,
    color: '#856404',
  },
});

export default ShareButton;
