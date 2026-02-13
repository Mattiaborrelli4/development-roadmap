import React, { useState, useCallback, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  TextInput,
  TouchableOpacity,
  KeyboardAvoidingView,
  Platform,
  Image,
  Dimensions,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { useRoute, useNavigation } from '@react-navigation/native';
import { usePosts } from '../hooks/usePosts';
import { THEME } from '../utils/constants';
import { formatDistanceToNow } from 'date-fns';
import { it } from 'date-fns/locale';
import CommentItem from '../components/CommentItem';
import dataService from '../services/dataService';
import storageService from '../services/storageService';

const { height: SCREEN_HEIGHT } = Dimensions.get('window');

const PostDetailScreen = () => {
  const route = useRoute();
  const navigation = useNavigation();
  const { postId } = route.params;
  const { getPostById, toggleLike } = usePosts();

  const [post, setPost] = useState(null);
  const [comments, setComments] = useState([]);
  const [commentText, setCommentText] = useState('');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadPostAndComments();
  }, [postId]);

  const loadPostAndComments = async () => {
    try {
      const [postData, commentsData] = await Promise.all([
        getPostById(postId),
        dataService.getComments(postId),
      ]);
      setPost(postData);
      setComments(commentsData);
    } catch (error) {
      console.error('Errore caricamento post:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleLike = useCallback(() => {
    if (post) {
      toggleLike(post.id);
      setPost(prev => ({
        ...prev,
        liked: !prev.liked,
        likes: prev.liked ? prev.likes - 1 : prev.likes + 1,
      }));
    }
  }, [post, toggleLike]);

  const handleSendComment = useCallback(async () => {
    if (!commentText.trim()) return;

    try {
      const newComment = await dataService.addComment(postId, commentText);
      setComments(prev => [newComment, ...prev]);
      setCommentText('');

      if (post) {
        setPost(prev => ({ ...prev, comments: prev.comments + 1 }));
      }
    } catch (error) {
      console.error('Errore invio commento:', error);
    }
  }, [commentText, postId, post]);

  const handleLikeComment = useCallback(async (commentId) => {
    try {
      await dataService.likeComment(commentId, postId);
      setComments(prev =>
        prev.map(comment =>
          comment.id === commentId
            ? { ...comment, likes: comment.likes + 1 }
            : comment
        )
      );
    } catch (error) {
      console.error('Errore like commento:', error);
    }
  }, [postId]);

  const renderHeader = () => {
    if (!post) return null;

    return (
      <View style={styles.postPreview}>
        <Image source={{ uri: post.content.uri }} style={styles.postImage} />
        <View style={styles.postActions}>
          <TouchableOpacity
            style={styles.actionButton}
            onPress={handleLike}
          >
            <Ionicons
              name={post.liked ? 'heart' : 'heart-outline'}
              size={24}
              color={post.liked ? THEME.colors.like : THEME.colors.text}
            />
          </TouchableOpacity>
          <TouchableOpacity style={styles.actionButton}>
            <Ionicons name="chatbubble-outline" size={24} color={THEME.colors.text} />
          </TouchableOpacity>
          <TouchableOpacity style={styles.actionButton}>
            <Ionicons name="paper-plane-outline" size={24} color={THEME.colors.text} />
          </TouchableOpacity>
        </View>
        <View style={styles.postInfo}>
          <Text style={styles.likes}>{post.likes} mi piace</Text>
          <Text style={styles.caption}>
            <Text style={styles.username}>{post.user.username}</Text>
            {' '}
            {post.caption}
          </Text>
          <Text style={styles.timestamp}>
            {formatDistanceToNow(new Date(post.createdAt), {
              addSuffix: true,
              locale: it,
            })}
          </Text>
        </View>
      </View>
    );
  };

  const renderComment = ({ item }) => (
    <CommentItem
      comment={item}
      onLike={handleLikeComment}
    />
  );

  if (isLoading) {
    return (
      <SafeAreaView style={styles.container} edges={['bottom']}>
        <View style={styles.loadingContainer}>
          <Text>Caricamento...</Text>
        </View>
      </SafeAreaView>
    );
  }

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      keyboardVerticalOffset={0}
    >
      <SafeAreaView style={styles.container} edges={['bottom']}>
        {/* Header */}
        <View style={styles.header}>
          <TouchableOpacity onPress={() => navigation.goBack()}>
            <Ionicons name="arrow-back" size={24} color={THEME.colors.text} />
          </TouchableOpacity>
          <Text style={styles.headerTitle}>Commenti</Text>
          <TouchableOpacity>
            <Ionicons name="ellipsis-horizontal" size={24} color={THEME.colors.text} />
          </TouchableOpacity>
        </View>

        {/* Content */}
        <FlatList
          data={comments}
          keyExtractor={(item) => item.id}
          renderItem={renderComment}
          ListHeaderComponent={renderHeader}
          ListEmptyComponent={
            <View style={styles.emptyContainer}>
              <Text style={styles.emptyText}>
                Nessun commento. Sii il primo a commentare!
              </Text>
            </View>
          }
          contentContainerStyle={styles.listContent}
        />

        {/* Comment Input */}
        <View style={styles.inputContainer}>
          <TextInput
            style={styles.input}
            placeholder="Aggiungi un commento..."
            placeholderTextColor={THEME.colors.textSecondary}
            value={commentText}
            onChangeText={setCommentText}
            multiline
          />
          <TouchableOpacity
            style={[styles.sendButton, !commentText.trim() && styles.sendButtonDisabled]}
            onPress={handleSendComment}
            disabled={!commentText.trim()}
          >
            <Text style={styles.sendButtonText}>Invia</Text>
          </TouchableOpacity>
        </View>
      </SafeAreaView>
    </KeyboardAvoidingView>
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
  postPreview: {
    borderBottomWidth: 1,
    borderBottomColor: THEME.colors.border,
    paddingBottom: 12,
  },
  postImage: {
    width: '100%',
    height: SCREEN_HEIGHT * 0.4,
  },
  postActions: {
    flexDirection: 'row',
    paddingHorizontal: 12,
    paddingVertical: 12,
  },
  actionButton: {
    marginRight: 16,
  },
  postInfo: {
    paddingHorizontal: 12,
  },
  likes: {
    fontSize: 14,
    fontWeight: '600',
    color: THEME.colors.text,
    marginBottom: 6,
  },
  caption: {
    fontSize: 14,
    color: THEME.colors.text,
    marginBottom: 4,
  },
  username: {
    fontWeight: '600',
  },
  timestamp: {
    fontSize: 12,
    color: THEME.colors.textSecondary,
  },
  listContent: {
    flexGrow: 1,
  },
  emptyContainer: {
    paddingVertical: 40,
    alignItems: 'center',
  },
  emptyText: {
    fontSize: 16,
    color: THEME.colors.textSecondary,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  inputContainer: {
    flexDirection: 'row',
    alignItems: 'flex-end',
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderTopWidth: 1,
    borderTopColor: THEME.colors.border,
    backgroundColor: THEME.colors.background,
  },
  input: {
    flex: 1,
    minHeight: 40,
    maxHeight: 100,
    paddingHorizontal: 12,
    paddingVertical: 8,
    backgroundColor: THEME.colors.backgroundSecondary,
    borderRadius: 20,
    fontSize: 14,
    color: THEME.colors.text,
    marginRight: 12,
  },
  sendButton: {
    paddingHorizontal: 16,
    paddingVertical: 8,
  },
  sendButtonDisabled: {
    opacity: 0.5,
  },
  sendButtonText: {
    fontSize: 16,
    fontWeight: '600',
    color: THEME.colors.primary,
  },
});

export default PostDetailScreen;
