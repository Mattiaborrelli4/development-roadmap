import React, { createContext, useContext, useState, useCallback } from 'react';
import dataService from '../services/dataService';
import storageService from '../services/storageService';

const PostsContext = createContext({});

export const DataProvider = ({ children }) => {
  const [posts, setPosts] = useState([]);
  const [stories, setStories] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);

  const loadPosts = useCallback(async (pageNum = 1, refresh = false) => {
    if (isLoading) return;

    setIsLoading(true);
    try {
      const response = await dataService.getPosts(pageNum, 10);

      if (refresh || pageNum === 1) {
        setPosts(response.posts);
      } else {
        setPosts(prev => [...prev, ...response.posts]);
      }

      setHasMore(response.hasMore);
      setPage(pageNum);
    } catch (error) {
      console.error('Errore caricamento post:', error);
    } finally {
      setIsLoading(false);
    }
  }, [isLoading]);

  const loadMorePosts = useCallback(async () => {
    if (!hasMore || isLoading) return;
    await loadPosts(page + 1);
  }, [hasMore, isLoading, page, loadPosts]);

  const refreshPosts = useCallback(async () => {
    await loadPosts(1, true);
  }, [loadPosts]);

  const likePost = useCallback(async (postId) => {
    try {
      const updatedPost = await dataService.likePost(postId);
      await storageService.toggleLikePost(postId);

      setPosts(prev =>
        prev.map(post =>
          post.id === postId ? updatedPost : post
        )
      );

      return updatedPost;
    } catch (error) {
      console.error('Errore like:', error);
      throw error;
    }
  }, []);

  const unlikePost = useCallback(async (postId) => {
    try {
      const updatedPost = await dataService.unlikePost(postId);
      await storageService.toggleLikePost(postId);

      setPosts(prev =>
        prev.map(post =>
          post.id === postId ? updatedPost : post
        )
      );

      return updatedPost;
    } catch (error) {
      console.error('Errore unlike:', error);
      throw error;
    }
  }, []);

  const toggleLike = useCallback(async (postId) => {
    const post = posts.find(p => p.id === postId);
    if (post?.liked) {
      await unlikePost(postId);
    } else {
      await likePost(postId);
    }
  }, [posts, likePost, unlikePost]);

  const createPost = useCallback(async (content) => {
    try {
      const newPost = await dataService.createPost(content);
      setPosts(prev => [newPost, ...prev]);
      return newPost;
    } catch (error) {
      console.error('Errore creazione post:', error);
      throw error;
    }
  }, []);

  const loadStories = useCallback(async () => {
    try {
      const storiesData = await dataService.getStories();
      setStories(storiesData);
      return storiesData;
    } catch (error) {
      console.error('Errore caricamento storie:', error);
    }
  }, []);

  const markStoryAsViewed = useCallback(async (storyId) => {
    try {
      await dataService.markStoryAsViewed(storyId);
      setStories(prev =>
        prev.map(story =>
          story.id === storyId ? { ...story, viewed: true } : story
        )
      );
    } catch (error) {
      console.error('Errore marca storia come vista:', error);
    }
  }, []);

  const getPostById = useCallback(async (postId) => {
    try {
      return await dataService.getPostById(postId);
    } catch (error) {
      console.error('Errore recupero post:', error);
      throw error;
    }
  }, []);

  return (
    <PostsContext.Provider
      value={{
        posts,
        stories,
        isLoading,
        hasMore,
        loadPosts,
        loadMorePosts,
        refreshPosts,
        likePost,
        unlikePost,
        toggleLike,
        createPost,
        loadStories,
        markStoryAsViewed,
        getPostById,
      }}
    >
      {children}
    </PostsContext.Provider>
  );
};

export const usePosts = () => {
  const context = useContext(PostsContext);
  if (!context) {
    throw new Error('usePosts deve essere usato dentro DataProvider');
  }
  return context;
};
