import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import Avatar from './Avatar';
import { THEME } from '../../utils/constants';

const StoryRing = ({ story, onPress, size = 70 }) => {
  const ringColor = story.viewed ? THEME.colors.border : THEME.colors.storyRing;

  return (
    <TouchableOpacity
      style={styles.container}
      onPress={onPress}
      activeOpacity={0.7}
    >
      <Avatar
        uri={story.user.avatar}
        size={size}
        borderWidth={story.viewed ? 1 : 3}
        borderColor={ringColor}
        storyRing={!story.viewed}
      />
      <Text style={styles.username} numberOfLines={1}>
        {story.user.username}
      </Text>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    marginHorizontal: 8,
  },
  username: {
    fontSize: 12,
    color: THEME.colors.text,
    marginTop: 4,
    maxWidth: 70,
  },
});

export default StoryRing;
