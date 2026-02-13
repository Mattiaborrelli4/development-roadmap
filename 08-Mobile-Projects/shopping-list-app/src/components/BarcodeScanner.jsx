import React, {useState, useEffect} from 'react';
import {
  View,
  Text,
  Modal,
  TouchableOpacity,
  StyleSheet,
  Alert,
  PermissionsAndroid,
  Platform,
  TextInput,
} from 'react-native';
import {CameraView, Camera} from 'expo-camera';
import {BARCODE_DATABASE} from '../utils/constants';

const BarcodeScanner = ({visible, onClose, onScan}) => {
  const [hasPermission, setHasPermission] = useState(null);
  const [scanned, setScanned] = useState(false);
  const [manualInput, setManualInput] = useState('');
  const [showManualInput, setShowManualInput] = useState(false);

  useEffect(() => {
    (async () => {
      if (Platform.OS === 'android') {
        const {status} = await Camera.requestCameraPermissionsAsync();
        setHasPermission(status === 'granted');
      } else {
        const {status} = await Camera.requestCameraPermissionsAsync();
        setHasPermission(status === 'granted');
      }
    })();
  }, []);

  const handleBarCodeScanned = ({type, data}) => {
    if (scanned) return;

    setScanned(true);

    // Cerca nel database simulato
    const product = BARCODE_DATABASE[data];

    if (product) {
      Alert.alert(
        'Prodotto Trovato!',
        `${product.icon || '📦'} ${product.name}`,
        [
          {
            text: 'Annulla',
            onPress: () => setScanned(false),
          },
          {
            text: 'Usa',
            onPress: () => {
              onScan({
                barcode: data,
                name: product.name,
                category: product.category,
              });
              setScanned(false);
              onClose();
            },
          },
        ]
      );
    } else {
      Alert.alert(
        'Codice non trovato',
        `Codice: ${data}\nVuoi aggiungere manualmente?`,
        [
          {
            text: 'Annulla',
            onPress: () => setScanned(false),
          },
          {
            text: 'Aggiungi',
            onPress: () => {
              onScan({barcode: data});
              setScanned(false);
              onClose();
            },
          },
        ]
      );
    }
  };

  const handleManualSubmit = () => {
    if (!manualInput.trim()) {
      Alert.alert('Errore', 'Inserisci un codice a barre');
      return;
    }

    const product = BARCODE_DATABASE[manualInput.trim()];

    if (product) {
      onScan({
        barcode: manualInput.trim(),
        name: product.name,
        category: product.category,
      });
    } else {
      onScan({barcode: manualInput.trim()});
    }

    setManualInput('');
    setShowManualInput(false);
    onClose();
  };

  if (hasPermission === null) {
    return (
      <Modal visible={visible} onRequestClose={onClose}>
        <View style={styles.container}>
          <Text style={styles.message}>Richiesta permesso camera...</Text>
        </View>
      </Modal>
    );
  }

  if (hasPermission === false) {
    return (
      <Modal visible={visible} onRequestClose={onClose}>
        <View style={styles.container}>
          <Text style={styles.message}>
            Nessun accesso alla camera
          </Text>
          <TouchableOpacity style={styles.button} onPress={onClose}>
            <Text style={styles.buttonText}>Chiudi</Text>
          </TouchableOpacity>
        </View>
      </Modal>
    );
  }

  return (
    <Modal visible={visible} onRequestClose={onClose}>
      <View style={styles.container}>
        {!showManualInput ? (
          <>
            <CameraView
              style={styles.camera}
              onBarcodeScanned={scanned ? undefined : handleBarCodeScanned}
              barcodeScannerSettings={{
                barcodeTypes: ['ean13', 'ean8', 'upc_a', 'upc_e', 'code128'],
              }}
            />

            <View style={styles.overlay}>
              <View style={styles.scanArea}>
                <View style={styles.scanCorner} />
                <View style={[styles.scanCorner, styles.scanCornerTopRight]} />
                <View style={[styles.scanCorner, styles.scanCornerBottomLeft]} />
                <View style={[styles.scanCorner, styles.scanCornerBottomRight]} />
              </View>

              <Text style={styles.instruction}>
                Allinea il codice a barre nel riquadro
              </Text>

              <View style={styles.buttons}>
                <TouchableOpacity
                  style={[styles.actionButton, styles.closeButton]}
                  onPress={onClose}>
                  <Text style={styles.actionButtonText}>✕</Text>
                </TouchableOpacity>

                {scanned && (
                  <TouchableOpacity
                    style={[styles.actionButton, styles.rescanButton]}
                    onPress={() => setScanned(false)}>
                    <Text style={styles.actionButtonText}>↻ Ri_scansiona</Text>
                  </TouchableOpacity>
                )}

                <TouchableOpacity
                  style={[styles.actionButton, styles.manualButton]}
                  onPress={() => setShowManualInput(true)}>
                  <Text style={styles.actionButtonText}>⌨️ Manuale</Text>
                </TouchableOpacity>
              </View>
            </View>
          </>
        ) : (
          <View style={styles.manualContainer}>
            <View style={styles.manualHeader}>
              <Text style={styles.title}>Inserisci Codice</Text>
              <TouchableOpacity onPress={() => setShowManualInput(false)}>
                <Text style={styles.closeButton}>✕</Text>
              </TouchableOpacity>
            </View>

            <View style={styles.manualContent}>
              <Text style={styles.label}>Codice a barre:</Text>
              <TextInput
                style={styles.input}
                value={manualInput}
                onChangeText={setManualInput}
                placeholder="Es: 8001234567890"
                keyboardType="number-pad"
                autoFocus
              />

              <Text style={styles.hint}>
                Codici di prova:{'\n'}
                8001234567890 - Latte{'\n'}
                8001234567891 - Pane{'\n'}
                8001234567892 - Uova
              </Text>

              <TouchableOpacity
                style={styles.submitButton}
                onPress={handleManualSubmit}>
                <Text style={styles.submitButtonText}>Conferma</Text>
              </TouchableOpacity>
            </View>
          </View>
        )}
      </View>
    </Modal>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000',
  },
  camera: {
    flex: 1,
  },
  overlay: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'rgba(0, 0, 0, 0.3)',
  },
  scanArea: {
    width: 280,
    height: 280,
    position: 'relative',
  },
  scanCorner: {
    position: 'absolute',
    width: 40,
    height: 40,
    borderColor: '#4ECDC4',
    borderWidth: 4,
    borderTopLeftRadius: 8,
  },
  scanCornerTopRight: {
    top: 0,
    right: 0,
    borderTopLeftRadius: 0,
    borderTopRightRadius: 8,
  },
  scanCornerBottomLeft: {
    bottom: 0,
    left: 0,
    borderTopLeftRadius: 0,
    borderBottomLeftRadius: 8,
  },
  scanCornerBottomRight: {
    bottom: 0,
    right: 0,
    borderTopLeftRadius: 0,
    borderBottomRightRadius: 8,
  },
  instruction: {
    color: '#FFFFFF',
    fontSize: 16,
    marginTop: 20,
    textAlign: 'center',
    paddingHorizontal: 40,
  },
  buttons: {
    position: 'absolute',
    bottom: 40,
    flexDirection: 'row',
    gap: 12,
  },
  actionButton: {
    paddingHorizontal: 20,
    paddingVertical: 12,
    borderRadius: 8,
    backgroundColor: 'rgba(255, 255, 255, 0.9)',
  },
  actionButtonText: {
    fontSize: 14,
    fontWeight: '600',
    color: '#2C3E50',
  },
  closeButton: {
    backgroundColor: '#F44336',
  },
  rescanButton: {
    backgroundColor: '#4CAF50',
  },
  manualButton: {
    backgroundColor: '#2196F3',
  },
  manualContainer: {
    flex: 1,
    backgroundColor: '#FFFFFF',
  },
  manualHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 20,
    borderBottomWidth: 1,
    borderBottomColor: '#E0E0E0',
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#2C3E50',
  },
  manualContent: {
    flex: 1,
    padding: 20,
  },
  label: {
    fontSize: 16,
    fontWeight: '600',
    color: '#2C3E50',
    marginBottom: 12,
  },
  input: {
    backgroundColor: '#F5F5F5',
    borderRadius: 8,
    padding: 16,
    fontSize: 16,
    borderWidth: 1,
    borderColor: '#E0E0E0',
    marginBottom: 16,
  },
  hint: {
    fontSize: 12,
    color: '#7F8C8D',
    marginBottom: 20,
    lineHeight: 20,
  },
  submitButton: {
    backgroundColor: '#4ECDC4',
    borderRadius: 8,
    padding: 16,
    alignItems: 'center',
  },
  submitButtonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: '600',
  },
  message: {
    fontSize: 16,
    color: '#FFFFFF',
    textAlign: 'center',
  },
});

export default BarcodeScanner;
