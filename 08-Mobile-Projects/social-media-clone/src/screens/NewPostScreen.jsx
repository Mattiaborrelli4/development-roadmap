import React, { useState, useCallback } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Image,
  TextInput,
  ScrollView,
  Alert,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { useNavigation } from '@react-navigation/native';
import * as ImagePicker from 'expo-image-picker';
import { usePosts } from '../hooks/usePosts';
import { useAuth } from '../hooks/useAuth';
import { THEME } from '../utils/constants';
import { POST_TYPES } from '../utils/constants';

const NewPostScreen = () => {
  const navigation = useNavigation();
  const { createPost } = usePosts();
  const { user } = useAuth();

  const [selectedMedia, setSelectedMedia] = useState(null);
  const [caption, setCaption] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const pickImage = async () => {
    try {
      const result = await ImagePicker.launchImageLibraryAsync({
        mediaTypes: ImagePicker.MediaTypeOptions.All,
        allowsEditing: true,
        aspect: [1, 1],
        quality: 1,
      });

      if (!result.canceled) {
        setSelectedMedia({
          uri: result.assets[0].uri,
          type: result.assets[0].type === 'video' ? POST_TYPES.VIDEO : POST_TYPES.IMAGE,
        });
      }
    } catch (error) {
      console.error('Errore selezione immagine:', error);
      Alert.alert('Errore', 'Impossibile selezionare l\'immagine');
    }
  };

  const takePhoto = async () => {
    try {
      const result = await ImagePicker.launchCameraAsync({
        mediaTypes: ImagePicker.MediaTypeOptions.Images,
        allowsEditing: true,
        aspect: [1, 1],
        quality: 1,
      });

      if (!result.canceled) {
        setSelectedMedia({
          uri: result.assets[0].uri,
          type: POST_TYPES.IMAGE,
        });
      }
    } catch (error) {
      console.error('Errore scatto foto:', error);
      Alert.alert('Errore', 'Impossibile scattare la foto');
    }
  };

  const handlePost = async () => {
    if (!selectedMedia) {
      Alert.alert('Attenzione', 'Seleziona un\'immagine o un video');
      return;
    }

    setIsLoading(true);
    try {
      const content = {
        ...selectedMedia,
        caption,
      };
      await createPost(content);
      navigation.goBack();
    } catch (error) {
      console.error('Errore pubblicazione:', error);
      Alert.alert('Errore', 'Impossibile pubblicare il post');
    } finally {
      setIsLoading(false);
    }
  };

  const showPickerOptions = () => {
    Alert.alert(
      'Seleziona media',
      'Scegli come aggiungere contenuti',
      [
        { text: 'Galleria', onPress: pickImage },
        { text: 'Fotocamera', onPress: takePhoto },
        { text: 'Annulla', style: 'cancel' },
      ]
    );
  };

  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      {/* Header */}
      <View style={styles.header}>
        <TouchableOpacity onPress={() => navigation.goBack()}>
          <Text style={styles.cancelButton}>Annulla</Text>
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Nuovo post</Text>
        <TouchableOpacity
          style={[styles.postButton, !selectedMedia && styles.postButtonDisabled]}
          onPress={handlePost}
          disabled={!selectedMedia || isLoading}
        >
          <Text style={[
            styles.postButtonText,
            !selectedMedia && styles.postButtonTextDisabled
          ]}>
            {isLoading ? 'Pubblicazione...' : 'Pubblica'}
          </Text>
        </TouchableOpacity>
      </View>

      <ScrollView style={styles.content}>
        {/* Media Preview */}
        <View style={styles.mediaContainer}>
          {selectedMedia ? (
            <View style={styles.mediaPreview}>
              {selectedMedia.type === POST_TYPES.VIDEO ? (
                <View style={styles.videoPlaceholder}>
                  <Ionicons name="play-circle" size={64} color={THEME.colors.textSecondary} />
                  <Text style={styles.videoText}>Video</Text>
                </View>
              ) : (
                <Image source={{ uri: selectedMedia.uri }} style={styles.mediaImage} />
              )}
              <TouchableOpacity
                style={styles.removeButton}
                onPress={() => setSelectedMedia(null)}
              >
                <Ionicons name="close-circle" size={24} color="#fff" />
              </TouchableOpacity>
            </View>
          ) : (
            <TouchableOpacity style={styles.placeholder} onPress={showPickerOptions}>
              <Ionicons name="image-outline" size={64} color={THEME.colors.textSecondary} />
              <Text style={styles.placeholderText}>Tocca per aggiungere foto o video</Text>
            </TouchableOpacity>
          )}
        </View>

        {/* Caption Input */}
        <View style={styles.captionContainer}>
          <Image source={{ uri: user?.avatar }} style={styles.avatar} />
          <TextInput
            style={styles.captionInput}
            placeholder="Scrivi una didascalia..."
            placeholderTextColor={THEME.colors.textSecondary}
            value={caption}
            onChangeText={setCaption}
            multiline
            maxLength={2200}
          />
        </View>

        {/* Additional Options */}
        <View style={styles.optionsContainer}>
          <TouchableOpacity style={styles.option}>
            <Ionicons name="add-circle-outline" size={24} color={THEME.colors.text} />
            <Text style={styles.optionText}>Tagga persone</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.option}>
            <Ionicons name="location-outline" size={24} color={THEME.colors.text} />
            <Text style={styles.optionText}>Aggiungi posizione</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.option}>
            <Ionicons name="happy-outline" size={24} color={THEME.colors.text} />
            <Text style={styles.optionText}>Aggiungi emoji</Text>
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
  cancelButton: {
    fontSize: 16,
    color: THEME.colors.text,
  },
  headerTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: THEME.colors.text,
  },
  postButton: {
    paddingVertical: 6,
    paddingHorizontal: 12,
    borderRadius: 6,
    backgroundColor: THEME.colors.primary,
  },
  postButtonDisabled: {
    backgroundColor: THEME.colors.backgroundSecondary,
  },
  postButtonText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#fff',
  },
  postButtonTextDisabled: {
    color: THEME.colors.textSecondary,
  },
  content: {
    flex: 1,
  },
  mediaContainer: {
    aspectRatio: 1,
    backgroundColor: THEME.colors.backgroundSecondary,
    margin: 16,
    marginBottom: 0,
  },
  mediaPreview: {
    width: '100%',
    height: '100%',
  },
  mediaImage: {
    width: '100%',
    height: '100%',
  },
  videoPlaceholder: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: THEME.colors.background,
  },
  videoText: {
    marginTop: 12,
    fontSize: 16,
    color: THEME.colors.textSecondary,
  },
  removeButton: {
    position: 'absolute',
    top: 12,
    right: 12,
  },
  placeholder: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  placeholderText: {
    marginTop: 12,
    fontSize: 16,
    color: THEME.colors.textSecondary,
  },
  captionContainer: {
    flexDirection: 'row',
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: THEME.colors.border,
  },
  avatar: {
    width: 40,
    height: 40,
    borderRadius: 20,
  },
  captionInput: {
    flex: 1,
    marginLeft: 12,
    fontSize: 14,
    color: THEME.colors.text,
    minHeight: 40,
  },
  optionsContainer: {
    marginTop: 16,
  },
  option: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: THEME.colors.border,
  },
  optionText: {
    fontSize: 16,
    color: THEME.colors.text,
    marginLeft: 12,
  },
});

export default NewPostScreen;
