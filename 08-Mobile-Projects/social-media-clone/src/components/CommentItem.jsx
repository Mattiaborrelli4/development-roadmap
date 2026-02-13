import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import Avatar from './Avatar';
import { THEME } from '../../utils/constants';
import { formatDistanceToNow } from 'date-fns';
import { it } from 'date-fns/locale';

const CommentItem = ({ comment, onLike, onReply }) => {
  return (
    <View style={styles.container}>
      <Avatar uri={comment.user.avatar} size={32} />
      <View style={styles.content}>
        <View style={styles.header}>
          <Text style={styles.username}>{comment.user.username}</Text>
          <Text style={styles.text}>{comment.text}</Text>
        </View>
        <View style={styles.footer}>
          <Text style={styles.timestamp}>
            {formatDistanceToNow(new Date(comment.createdAt), {
              addSuffix: true,
              locale: it,
            })}
          </Text>
          <TouchableOpacity onPress={() => onLike?.(comment.id)}>
            <Text style={styles.likeText}>Mi piace</Text>
          </TouchableOpacity>
          <TouchableOpacity onPress={() => onReply?.(comment)}>
            <Text style={styles.replyText}>Rispondi</Text>
          </TouchableOpacity>
        </View>
      </View>
      {comment.likes > 0 && (
        <TouchableOpacity onPress={() => onLike?.(comment.id)} style={styles.likesContainer}>
          <Text style={styles.likesText}>{comment.likes}</Text>
        </TouchableOpacity>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    paddingVertical: 8,
    paddingHorizontal: 16,
  },
  content: {
    flex: 1,
    marginLeft: 12,
  },
  header: {
    flexDirection: 'row',
    flexWrap: 'wrap',
  },
  username: {
    fontSize: 14,
    fontWeight: '600',
    color: THEME.colors.text,
    marginRight: 6,
  },
  text: {
    fontSize: 14,
    color: THEME.colors.text,
    flex: 1,
  },
  footer: {
    flexDirection: 'row',
    marginTop: 4,
  },
  timestamp: {
    fontSize: 12,
    color: THEME.colors.textSecondary,
    marginRight: 16,
  },
  likeText: {
    fontSize: 12,
    color: THEME.colors.textSecondary,
    marginRight: 16,
  },
  replyText: {
    fontSize: 12,
    color: THEME.colors.textSecondary,
  },
  likesContainer: {
    padding: 4,
  },
  likesText: {
    fontSize: 12,
    color: THEME.colors.textSecondary,
  },
});

export default CommentItem;
