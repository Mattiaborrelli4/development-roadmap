import React, { useState, useCallback, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Image,
  Dimensions,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { useRoute, useNavigation } from '@react-navigation/native';
import { useAuth } from '../hooks/useAuth';
import dataService from '../services/dataService';
import { THEME } from '../utils/constants';
import Avatar from '../components/Avatar';

const { width } = Dimensions.get('window');
const GRID_SPACING = 2;
const ITEM_SIZE = (width - GRID_SPACING * 2) / 3;

const ProfileScreen = () => {
  const route = useRoute();
  const navigation = useNavigation();
  const { user: currentUser } = useAuth();
  const { userId } = route.params || {};

  const [user, setUser] = useState(null);
  const [posts, setPosts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedTab, setSelectedTab] = useState('posts'); // posts, saved, tagged

  const isOwnProfile = !userId || userId === currentUser?.id;

  useEffect(() => {
    loadUserData();
  }, [userId]);

  const loadUserData = async () => {
    setIsLoading(true);
    try {
      const targetUserId = userId || currentUser?.id;
      const [userData, userPosts] = await Promise.all([
        dataService.getUserById(targetUserId),
        dataService.getUserPosts(targetUserId),
      ]);
      setUser(userData);
      setPosts(userPosts);
    } catch (error) {
      console.error('Errore caricamento profilo:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleFollow = async () => {
    try {
      if (user.isFollowing) {
        await dataService.unfollowUser(user.id);
      } else {
        await dataService.followUser(user.id);
      }
      await loadUserData();
    } catch (error) {
      console.error('Errore follow/unfollow:', error);
    }
  };

  const handleEditProfile = () => {
    navigation.navigate('EditProfile');
  };

  const handleSettings = () => {
    // Implement settings navigation
  };

  const renderStat = (label, count) => (
    <View style={styles.stat}>
      <Text style={styles.statCount}>{count}</Text>
      <Text style={styles.statLabel}>{label}</Text>
    </View>
  );

  const renderGridItem = ({ item }) => (
    <TouchableOpacity style={styles.gridItem}>
      <Image source={{ uri: item.content.uri }} style={styles.gridImage} />
      {item.content.type === 'video' && (
        <View style={styles.videoIndicator}>
          <Ionicons name="play" size={16} color="#fff" />
        </View>
      )}
    </TouchableOpacity>
  );

  const renderEmptyGrid = () => (
    <View style={styles.emptyGrid}>
      <Ionicons name="grid-outline" size={64} color={THEME.colors.textSecondary} />
      <Text style={styles.emptyText}>
        {selectedTab === 'posts' && 'Nessun post ancora'}
        {selectedTab === 'saved' && 'Nessun post salvato'}
        {selectedTab === 'tagged' && 'Nessun post in cui sei taggato'}
      </Text>
    </View>
  );

  if (isLoading) {
    return (
      <SafeAreaView style={styles.container} edges={['top']}>
        <View style={styles.loadingContainer}>
          <Text>Caricamento...</Text>
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container} edges={['top']}>
      <ScrollView showsVerticalScrollIndicator={false}>
        {/* Header */}
        <View style={styles.header}>
          <Text style={styles.username}>{user?.username}</Text>
          <View style={styles.headerActions}>
            <TouchableOpacity onPress={() => navigation.navigate('Search')}>
              <Ionicons name="add-outline" size={24} color={THEME.colors.text} />
            </TouchableOpacity>
            <TouchableOpacity onPress={() => navigation.navigate('Messages')}>
              <Ionicons name="menu-outline" size={24} color={THEME.colors.text} />
            </TouchableOpacity>
          </View>
        </View>

        {/* Profile Info */}
        <View style={styles.profileSection}>
          <Avatar uri={user?.avatar} size={86} />

          <View style={styles.statsContainer}>
            {renderStat('Post', posts.length)}
            {renderStat('Follower', user?.followers || 0)}
            {renderStat('Seguiti', user?.following || 0)}
          </View>
        </View>

        <View style={styles.bioSection}>
          <Text style={styles.name}>{user?.username}</Text>
          <Text style={styles.bio}>{user?.bio}</Text>
        </View>

        {/* Action Buttons */}
        <View style={styles.actionsContainer}>
          {isOwnProfile ? (
            <>
              <TouchableOpacity
                style={[styles.button, styles.primaryButton]}
                onPress={handleEditProfile}
              >
                <Text style={styles.primaryButtonText}>Modifica profilo</Text>
              </TouchableOpacity>
              <TouchableOpacity
                style={[styles.button, styles.iconButton]}
                onPress={handleSettings}
              >
                <Ionicons name="settings-outline" size={18} color={THEME.colors.text} />
              </TouchableOpacity>
            </>
          ) : (
            <>
              <TouchableOpacity
                style={[
                  styles.button,
                  styles.followButton,
                  user?.isFollowing && styles.followingButton
                ]}
                onPress={handleFollow}
              >
                <Text style={[
                  styles.followButtonText,
                  user?.isFollowing && styles.followingButtonText
                ]}>
                  {user?.isFollowing ? 'Segui già' : 'Segui'}
                </Text>
              </TouchableOpacity>
              <TouchableOpacity
                style={[styles.button, styles.iconButton]}
                onPress={() => navigation.navigate('Messages', { userId: user?.id })}
              >
                <Ionicons name="paper-plane-outline" size={18} color={THEME.colors.text} />
              </TouchableOpacity>
            </>
          )}
        </View>

        {/* Tabs */}
        <View style={styles.tabsContainer}>
          <TouchableOpacity
            style={[styles.tab, selectedTab === 'posts' && styles.activeTab]}
            onPress={() => setSelectedTab('posts')}
          >
            <Ionicons
              name="grid"
              size={24}
              color={selectedTab === 'posts' ? THEME.colors.text : THEME.colors.textSecondary}
            />
          </TouchableOpacity>
          <TouchableOpacity
            style={[styles.tab, selectedTab === 'saved' && styles.activeTab]}
            onPress={() => setSelectedTab('saved')}
          >
            <Ionicons
              name="bookmark"
              size={24}
              color={selectedTab === 'saved' ? THEME.colors.text : THEME.colors.textSecondary}
            />
          </TouchableOpacity>
          <TouchableOpacity
            style={[styles.tab, selectedTab === 'tagged' && styles.activeTab]}
            onPress={() => setSelectedTab('tagged')}
          >
            <Ionicons
              name="person-outline"
              size={24}
              color={selectedTab === 'tagged' ? THEME.colors.text : THEME.colors.textSecondary}
            />
          </TouchableOpacity>
        </View>

        {/* Grid */}
        {posts.length > 0 ? (
          <View style={styles.grid}>
            {posts.map((post) => (
              <View key={post.id} style={styles.gridItem}>
                <Image source={{ uri: post.content.uri }} style={styles.gridImage} />
                {post.content.type === 'video' && (
                  <View style={styles.videoIndicator}>
                    <Ionicons name="play" size={16} color="#fff" />
                  </View>
                )}
              </View>
            ))}
          </View>
        ) : (
          renderEmptyGrid()
        )}
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: THEME.colors.background,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingVertical: 12,
  },
  username: {
    fontSize: 20,
    fontWeight: 'bold',
    color: THEME.colors.text,
  },
  headerActions: {
    flexDirection: 'row',
    gap: 16,
  },
  profileSection: {
    flexDirection: 'row',
    paddingHorizontal: 16,
    paddingVertical: 16,
    alignItems: 'center',
  },
  statsContainer: {
    flex: 1,
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginLeft: 24,
  },
  stat: {
    alignItems: 'center',
  },
  statCount: {
    fontSize: 18,
    fontWeight: 'bold',
    color: THEME.colors.text,
  },
  statLabel: {
    fontSize: 12,
    color: THEME.colors.text,
  },
  bioSection: {
    paddingHorizontal: 16,
    marginBottom: 16,
  },
  name: {
    fontSize: 14,
    fontWeight: '600',
    color: THEME.colors.text,
    marginBottom: 4,
  },
  bio: {
    fontSize: 14,
    color: THEME.colors.text,
    lineHeight: 18,
  },
  actionsContainer: {
    flexDirection: 'row',
    paddingHorizontal: 16,
    marginBottom: 16,
    gap: 8,
  },
  button: {
    flex: 1,
    height: 32,
    justifyContent: 'center',
    alignItems: 'center',
    borderRadius: 6,
  },
  primaryButton: {
    backgroundColor: THEME.colors.backgroundSecondary,
  },
  primaryButtonText: {
    fontSize: 14,
    fontWeight: '600',
    color: THEME.colors.text,
  },
  followButton: {
    backgroundColor: THEME.colors.primary,
  },
  followButtonText: {
    fontSize: 14,
    fontWeight: '600',
    color: '#fff',
  },
  followingButton: {
    backgroundColor: 'transparent',
    borderWidth: 1,
    borderColor: THEME.colors.border,
  },
  followingButtonText: {
    color: THEME.colors.text,
  },
  iconButton: {
    flex: 0,
    width: 32,
    backgroundColor: THEME.colors.backgroundSecondary,
  },
  tabsContainer: {
    flexDirection: 'row',
    borderTopWidth: 1,
    borderBottomColor: THEME.colors.border,
  },
  tab: {
    flex: 1,
    paddingVertical: 12,
    alignItems: 'center',
    borderBottomWidth: 1,
    borderBottomColor: 'transparent',
  },
  activeTab: {
    borderBottomColor: THEME.colors.text,
  },
  grid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
  },
  gridItem: {
    width: ITEM_SIZE,
    height: ITEM_SIZE,
    marginRight: GRID_SPACING,
    marginBottom: GRID_SPACING,
  },
  gridImage: {
    width: '100%',
    height: '100%',
  },
  videoIndicator: {
    position: 'absolute',
    top: 8,
    right: 8,
    width: 24,
    height: 24,
    borderRadius: 12,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  emptyGrid: {
    alignItems: 'center',
    paddingVertical: 60,
  },
  emptyText: {
    fontSize: 16,
    color: THEME.colors.textSecondary,
    marginTop: 16,
  },
});

export default ProfileScreen;
