import React, { useState, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Image,
  Dimensions,
  Pressable,
} from 'react-native';
import { Video } from 'expo-av';
import { Ionicons } from '@expo/vector-icons';
import { formatDistanceToNow } from 'date-fns';
import { it } from 'date-fns/locale';
import { THEME } from '../../utils/constants';
import Avatar from './Avatar';
import LikeButton from './LikeButton';
import ActionButton from './ActionButton';

const { width } = Dimensions.get('window');
const POST_WIDTH = width;

const PostCard = ({ post, onLike, onComment, onShare, onSave, onPress, onUserPress }) => {
  const [isSaved, setIsSaved] = useState(false);
  const [doubleTapHeart, setDoubleTapHeart] = useState(false);
  const videoRef = useRef(null);
  const lastTap = useRef(0);

  const handleDoubleTap = () => {
    const now = Date.now();
    if (now - lastTap.current < 300) {
      setDoubleTapHeart(true);
      if (!post.liked) {
        onLike();
      }
      setTimeout(() => setDoubleTapHeart(false), 1000);
    }
    lastTap.current = now;
  };

  const handleSave = () => {
    setIsSaved(!isSaved);
    onSave?.(post.id);
  };

  const renderContent = () => {
    if (post.content.type === 'video') {
      return (
        <Pressable onPress={handleDoubleTap}>
          <Video
            ref={videoRef}
            source={{ uri: post.content.uri }}
            style={styles.content}
            useNativeControls
            resizeMode="cover"
            isLooping
          />
        </Pressable>
      );
    }

    return (
      <Pressable onPress={handleDoubleTap}>
        <Image source={{ uri: post.content.uri }} style={styles.content} />
      </Pressable>
    );
  };

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <TouchableOpacity
          style={styles.headerLeft}
          onPress={() => onUserPress?.(post.user.id)}
        >
          <Avatar uri={post.user.avatar} size={32} />
          <View style={styles.headerText}>
            <Text style={styles.username}>{post.user.username}</Text>
            {post.location && (
              <Text style={styles.location}>{post.location}</Text>
            )}
          </View>
        </TouchableOpacity>
        <TouchableOpacity>
          <Ionicons name="ellipsis-horizontal" size={20} color={THEME.colors.text} />
        </TouchableOpacity>
      </View>

      {/* Content */}
      {renderContent()}

      {/* Double Tap Heart Animation */}
      {doubleTapHeart && (
        <View style={styles.heartOverlay}>
          <Text style={styles.heartIcon}>❤️</Text>
        </View>
      )}

      {/* Actions */}
      <View style={styles.actions}>
        <View style={styles.actionsLeft}>
          <LikeButton liked={post.liked} onToggle={onLike} />
          <ActionButton
            iconName="chatbubble-outline"
            onPress={() => onComment?.(post)}
          />
          <ActionButton
            iconName="paper-plane-outline"
            onPress={() => onShare?.(post)}
          />
        </View>
        <TouchableOpacity onPress={handleSave}>
          <Ionicons
            name={isSaved ? "bookmark" : "bookmark-outline"}
            size={24}
            color={THEME.colors.text}
          />
        </TouchableOpacity>
      </View>

      {/* Likes */}
      <View style={styles.likesSection}>
        <Text style={styles.likes}>{post.likes} mi piace</Text>
      </View>

      {/* Caption */}
      <TouchableOpacity
        style={styles.captionSection}
        onPress={() => onPress?.(post)}
      >
        <Text style={styles.caption} numberOfLines={2}>
          <Text style={styles.captionUsername}>{post.user.username}</Text>
          {' '}
          {post.caption}
        </Text>
      </TouchableOpacity>

      {/* Comments */}
      {post.comments > 0 && (
        <TouchableOpacity
          style={styles.commentsSection}
          onPress={() => onPress?.(post)}
        >
          <Text style={styles.commentsLink}>
            Vedi tutti i {post.comments} commenti
          </Text>
        </TouchableOpacity>
      )}

      {/* Timestamp */}
      <View style={styles.timestampSection}>
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

const styles = StyleSheet.create({
  container: {
    backgroundColor: THEME.colors.background,
    marginBottom: 8,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 12,
    paddingVertical: 8,
  },
  headerLeft: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  headerText: {
    marginLeft: 12,
  },
  username: {
    fontSize: 14,
    fontWeight: '600',
    color: THEME.colors.text,
  },
  location: {
    fontSize: 12,
    color: THEME.colors.textSecondary,
    marginTop: 2,
  },
  content: {
    width: POST_WIDTH,
    height: POST_WIDTH,
    backgroundColor: THEME.colors.backgroundSecondary,
  },
  heartOverlay: {
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: [{ translateX: -35 }, { translateY: -35 }],
    zIndex: 10,
  },
  heartIcon: {
    fontSize: 70,
  },
  actions: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 12,
    paddingVertical: 8,
  },
  actionsLeft: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  likesSection: {
    paddingHorizontal: 12,
  },
  likes: {
    fontSize: 14,
    fontWeight: '600',
    color: THEME.colors.text,
  },
  captionSection: {
    paddingHorizontal: 12,
    marginTop: 4,
  },
  caption: {
    fontSize: 14,
    color: THEME.colors.text,
    lineHeight: 18,
  },
  captionUsername: {
    fontWeight: '600',
  },
  commentsSection: {
    paddingHorizontal: 12,
    marginTop: 4,
  },
  commentsLink: {
    fontSize: 14,
    color: THEME.colors.textSecondary,
  },
  timestampSection: {
    paddingHorizontal: 12,
    paddingVertical: 8,
  },
  timestamp: {
    fontSize: 12,
    color: THEME.colors.textSecondary,
    textTransform: 'lowercase',
  },
});

export default PostCard;
