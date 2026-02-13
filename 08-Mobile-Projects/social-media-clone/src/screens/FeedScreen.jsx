import React, { useCallback, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  RefreshControl,
  ScrollView,
  TouchableOpacity,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { usePosts } from '../hooks/usePosts';
import { useNavigation } from '@react-navigation/native';
import { THEME } from '../utils/constants';
import StoryRing from '../components/StoryRing';
import PostCard from '../components/PostCard';

const FeedScreen = () => {
  const navigation = useNavigation();
  const {
    posts,
    stories,
    isLoading,
    loadPosts,
    loadMorePosts,
    refreshPosts,
    loadStories,
    markStoryAsViewed,
    toggleLike,
  } = usePosts();

  useEffect(() => {
    loadPosts();
    loadStories();
  }, []);

  const handleRefresh = useCallback(() => {
    refreshPosts();
    loadStories();
  }, [refreshPosts, loadStories]);

  const handleLike = useCallback((postId) => {
    toggleLike(postId);
  }, [toggleLike]);

  const handleComment = useCallback((post) => {
    navigation.navigate('PostDetail', { postId: post.id });
  }, [navigation]);

  const handleUserPress = useCallback((userId) => {
    navigation.navigate('Profile', { userId });
  }, [navigation]);

  const handleStoryPress = useCallback((story) => {
    markStoryAsViewed(story.id);
    // Qui potresti navigare a uno schermo visualizzatore di storie
  }, [markStoryAsViewed]);

  const renderStory = ({ item }) => (
    <StoryRing story={item} onPress={() => handleStoryPress(item)} />
  );

  const renderPost = ({ item }) => (
    <PostCard
      post={item}
      onLike={() => handleLike(item.id)}
      onComment={handleComment}
      onUserPress={handleUserPress}
    />
  );

  const renderFooter = () => {
    if (!isLoading) return null;
    return (
      <View style={styles.footerLoader}>
        <Text style={styles.footerText}>Caricamento...</Text>
      </View>
    );
  };

  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      {/* Header */}
      <View style={styles.header}>
        <TouchableOpacity>
          <Ionicons name="camera-outline" size={24} color={THEME.colors.text} />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>SocialMedia</Text>
        <TouchableOpacity onPress={() => navigation.navigate('Messages')}>
          <Ionicons name="paper-plane-outline" size={24} color={THEME.colors.text} />
        </TouchableOpacity>
      </View>

      {/* Stories */}
      <ScrollView
        horizontal
        showsHorizontalScrollIndicator={false}
        style={styles.storiesContainer}
        contentContainerStyle={styles.storiesContent}
      >
        {stories.map((story) => (
          <View key={story.id}>
            <StoryRing story={story} onPress={() => handleStoryPress(story)} />
          </View>
        ))}
      </ScrollView>

      {/* Posts */}
      <FlatList
        data={posts}
        keyExtractor={(item) => item.id}
        renderItem={renderPost}
        onEndReached={loadMorePosts}
        onEndReachedThreshold={0.5}
        ListFooterComponent={renderFooter}
        refreshControl={
          <RefreshControl
            refreshing={isLoading}
            onRefresh={handleRefresh}
            tintColor={THEME.colors.primary}
          />
        }
        showsVerticalScrollIndicator={false}
      />
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
    fontSize: 20,
    fontWeight: 'bold',
    color: THEME.colors.text,
    fontFamily: 'Arial',
  },
  storiesContainer: {
    maxHeight: 100,
    backgroundColor: THEME.colors.background,
  },
  storiesContent: {
    paddingHorizontal: 8,
    paddingVertical: 12,
  },
  footerLoader: {
    paddingVertical: 20,
    alignItems: 'center',
  },
  footerText: {
    color: THEME.colors.textSecondary,
  },
});

export default FeedScreen;
