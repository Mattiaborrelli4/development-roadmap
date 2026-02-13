import React from 'react';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createStackNavigator } from '@react-navigation/stack';
import { Ionicons } from '@expo/vector-icons';
import { useNotifications } from '../hooks/useNotifications';
import { THEME } from '../utils/constants';

// Screens
import FeedScreen from '../screens/FeedScreen';
import SearchScreen from '../screens/SearchScreen';
import NewPostScreen from '../screens/NewPostScreen';
import NotificationsScreen from '../screens/NotificationsScreen';
import ProfileScreen from '../screens/ProfileScreen';
import MessagesScreen from '../screens/MessagesScreen';
import PostDetailScreen from '../screens/PostDetailScreen';
import EditProfileScreen from '../screens/EditProfileScreen';

const Tab = createBottomTabNavigator();
const Stack = createStackNavigator();

// Feed Stack
const FeedStack = () => (
  <Stack.Navigator
    screenOptions={{
      headerShown: false,
      cardStyle: { backgroundColor: THEME.colors.background },
    }}
  >
    <Stack.Screen name="Feed" component={FeedScreen} />
    <Stack.Screen
      name="PostDetail"
      component={PostDetailScreen}
      options={{ presentation: 'modal' }}
    />
    <Stack.Screen name="Messages" component={MessagesScreen} />
  </Stack.Navigator>
);

// Search Stack
const SearchStack = () => (
  <Stack.Navigator
    screenOptions={{
      headerShown: false,
      cardStyle: { backgroundColor: THEME.colors.background },
    }}
  >
    <Stack.Screen name="Search" component={SearchScreen} />
    <Stack.Screen name="Profile" component={ProfileScreen} />
  </Stack.Navigator>
);

// Add Stack
const AddStack = () => (
  <Stack.Navigator
    screenOptions={{
      headerShown: false,
      cardStyle: { backgroundColor: THEME.colors.background },
    }}
  >
    <Stack.Screen name="NewPost" component={NewPostScreen} />
  </Stack.Navigator>
);

// Notifications Stack
const NotificationsStack = () => {
  const { unreadCount } = useNotifications();

  return (
    <Stack.Navigator
      screenOptions={{
        headerShown: false,
        cardStyle: { backgroundColor: THEME.colors.background },
      }}
    >
      <Stack.Screen name="Notifications" component={NotificationsScreen} />
      <Stack.Screen name="Profile" component={ProfileScreen} />
    </Stack.Navigator>
  );
};

// Profile Stack
const ProfileStack = () => (
  <Stack.Navigator
    screenOptions={{
      headerShown: false,
      cardStyle: { backgroundColor: THEME.colors.background },
    }}
  >
    <Stack.Screen name="Profile" component={ProfileScreen} />
    <Stack.Screen name="EditProfile" component={EditProfileScreen} />
    <Stack.Screen name="Messages" component={MessagesScreen} />
  </Stack.Navigator>
);

// Tab Bar Icon
const TabBarIcon = ({ name, focused, color }) => {
  let iconName = name;

  // Change icon when focused
  if (focused) {
    switch (name) {
      case 'home-outline':
        iconName = 'home';
        break;
      case 'search-outline':
        iconName = 'search';
        break;
      case 'add-circle-outline':
        iconName = 'add-circle';
        break;
      case 'heart-outline':
        iconName = 'heart';
        break;
      case 'person-outline':
        iconName = 'person';
        break;
    }
  }

  return <Ionicons name={iconName} size={focused ? 26 : 24} color={color} />;
};

// Custom Tab Bar Badge for Notifications
const NotificationsIcon = ({ focused, color, unreadCount }) => (
  <TabBarIcon name="heart-outline" focused={focused} color={color} />
);

// Tab Navigator
const TabNavigator = () => {
  const { unreadCount } = useNotifications();

  return (
    <Tab.Navigator
      screenOptions={{
        headerShown: false,
        tabBarActiveTintColor: THEME.colors.text,
        tabBarInactiveTintColor: THEME.colors.text,
        tabBarShowLabel: false,
        tabBarStyle: {
          backgroundColor: THEME.colors.background,
          borderTopWidth: 1,
          borderTopColor: THEME.colors.border,
          height: 50,
        },
        tabBarIconStyle: {
          marginTop: 8,
        },
      }}
    >
      <Tab.Screen
        name="Home"
        component={FeedStack}
        options={{
          tabBarIcon: ({ focused, color }) => (
            <TabBarIcon name="home-outline" focused={focused} color={color} />
          ),
        }}
      />
      <Tab.Screen
        name="SearchTab"
        component={SearchStack}
        options={{
          tabBarIcon: ({ focused, color }) => (
            <TabBarIcon name="search-outline" focused={focused} color={color} />
          ),
        }}
      />
      <Tab.Screen
        name="Add"
        component={AddStack}
        options={{
          tabBarIcon: ({ focused, color }) => (
            <TabBarIcon name="add-circle-outline" focused={focused} color={color} />
          ),
        }}
      />
      <Tab.Screen
        name="NotificationsTab"
        component={NotificationsStack}
        options={{
          tabBarIcon: ({ focused, color }) => (
            <TabBarIcon name="heart-outline" focused={focused} color={color} />
          ),
          tabBarBadge: unreadCount > 0 ? unreadCount : null,
          tabBarBadgeStyle: {
            backgroundColor: THEME.colors.error,
            fontSize: 10,
            minWidth: 18,
            height: 18,
            lineHeight: 18,
          },
        }}
      />
      <Tab.Screen
        name="ProfileTab"
        component={ProfileStack}
        options={{
          tabBarIcon: ({ focused, color }) => (
            <TabBarIcon name="person-outline" focused={focused} color={color} />
          ),
        }}
      />
    </Tab.Navigator>
  );
};

export default TabNavigator;
