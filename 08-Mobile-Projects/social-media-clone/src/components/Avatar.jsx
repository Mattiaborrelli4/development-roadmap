import React from 'react';
import { View, Image, StyleSheet } from 'react-native';
import { THEME } from '../../utils/constants';

const Avatar = ({
  uri,
  size = 40,
  borderWidth = 0,
  borderColor = THEME.colors.border,
  storyRing = false,
}) => {
  const avatarStyle = {
    width: size,
    height: size,
    borderRadius: size / 2,
    borderWidth,
    borderColor,
  };

  const containerStyle = {
    width: size + (storyRing ? 6 : 0),
    height: size + (storyRing ? 6 : 0),
    borderRadius: (size + (storyRing ? 6 : 0)) / 2,
    padding: storyRing ? 3 : 0,
    backgroundColor: storyRing
      ? THEME.colors.storyRing
      : 'transparent',
  };

  return (
    <View style={containerStyle}>
      <Image
        source={{ uri }}
        style={avatarStyle}
        defaultSource={require('../../assets/adaptive-icon.png')}
      />
    </View>
  );
};

export default Avatar;
