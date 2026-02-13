import { SAMPLE_IMAGES, SAMPLE_AVATARS, POST_TYPES, NOTIFICATION_TYPES } from '../utils/constants';

// Dati simulati per l'applicazione

const USERS = [
  {
    id: '1',
    username: 'marco_rossi',
    avatar: SAMPLE_AVATARS[0],
    bio: '📸 Fotografo appassionato\n📍 Milano, Italia\n✨ Viaggi & Natura',
    posts: 156,
    followers: 2340,
    following: 890,
    isFollowing: false,
  },
  {
    id: '2',
    username: 'giulia_bianchi',
    avatar: SAMPLE_AVATARS[1],
    bio: '🎨 Designer & Creative\n💫 Milan based\n💌 DM per collaborazioni',
    posts: 234,
    followers: 5420,
    following: 432,
    isFollowing: true,
  },
  {
    id: '3',
    username: 'luca_verdi',
    avatar: SAMPLE_AVATARS[2],
    bio: '🏃‍♂️ Runner | 🚴 Cyclist\n🏔️ Mountain lover\n📍 Torino',
    posts: 89,
    followers: 1203,
    following: 567,
    isFollowing: true,
  },
  {
    id: '4',
    username: 'sophia_marta',
    avatar: SAMPLE_AVATARS[3],
    bio: '✨ Life enthusiast\n🌿 Plant mom\n🎵 Music addict',
    posts: 312,
    followers: 8934,
    following: 234,
    isFollowing: false,
  },
  {
    id: '5',
    username: 'andrea_ferrari',
    avatar: SAMPLE_AVATARS[4],
    bio: '👨‍💻 Tech lover\n📱 Mobile Developer\n☕ Coffee addicted',
    posts: 145,
    followers: 3456,
    following: 789,
    isFollowing: false,
  },
  {
    id: '6',
    username: 'elena_conti',
    avatar: SAMPLE_AVATARS[5],
    bio: '🌍 Travel blogger\n✈️ 50+ countries visited\n📸 Canon EOS R5',
    posts: 567,
    followers: 15432,
    following: 456,
    isFollowing: true,
  },
  {
    id: '7',
    username: 'paolo_russo',
    avatar: SAMPLE_AVATARS[6],
    bio: '🍕 Food lover\n👨‍🍳 Chef amatoriale\n📍 Napoli',
    posts: 234,
    followers: 6789,
    following: 345,
    isFollowing: false,
  },
  {
    id: '8',
    username: 'anna_lombardi',
    avatar: SAMPLE_AVATARS[7],
    bio: '🎭 Art & Culture\n🏛️ Museum guide\n📚 Book lover',
    posts: 178,
    followers: 2345,
    following: 678,
    isFollowing: true,
  },
  {
    id: '9',
    username: 'marco_colombo',
    avatar: SAMPLE_AVATARS[8],
    bio: '🎬 Film maker\n📽️ Video editor\n📍 Roma',
    posts: 89,
    followers: 4567,
    following: 234,
    isFollowing: false,
  },
  {
    id: '10',
    username: 'federica_rossi',
    avatar: SAMPLE_AVATARS[9],
    bio: '🧘‍♀️ Yoga instructor\n🌱 Wellness coach\n💚 Green lifestyle',
    posts: 345,
    followers: 9876,
    following: 567,
    isFollowing: true,
  },
  {
    id: '11',
    username: 'davide_bruno',
    avatar: SAMPLE_AVATARS[10],
    bio: '🎸 Musician\n🎹 Piano teacher\n📍 Bologna',
    posts: 123,
    followers: 3456,
    following: 890,
    isFollowing: false,
  },
  {
    id: '12',
    username: 'chiara_moretti',
    avatar: SAMPLE_AVATARS[11],
    bio: '👗 Fashion blogger\n🛍️ Shopping addict\n✨ Style advisor',
    posts: 456,
    followers: 12345,
    following: 345,
    isFollowing: true,
  },
];

// Utente corrente (loggato)
const CURRENT_USER = {
  id: 'current_user',
  username: 'io_mattia',
  avatar: 'https://i.pravatar.cc/150?img=33',
  bio: '📱 App Developer\n💻 Tech enthusiast\n📍 Italy',
  posts: 67,
  followers: 234,
  following: 456,
  isFollowing: false,
};

// Genera post casuali
const generatePosts = () => {
  const captions = [
    'Momento perfetto ✨ #vita #bellezza',
    'Giornata incredibile 🌞 #summer #vibes',
    'Cosa ne pensate? 🤔 #community #feedback',
    'Nuovo inizio 🚀 #nuovo #goals',
    'Ricordi preziosi 💫 #memories #love',
    'Lavoro in corso 💪 #grind #hustle',
    'Visto da qui 🌅 #perspective #view',
    'Weekend mood 😎 #relax #fun',
    'Ispirazione del giorno 💡 #creative #art',
    'Amo questo posto 🌍 #travel #explore',
    'Buongiorno mondo! ☀️ #morning #positive',
    'Notte magica 🌙 #night #dreams',
    'Piccole cose ❤️ #simple #joy',
    'Grande traguardo 🏆 #achievement #success',
    'Avventura awaits 🎒 #adventure #wild',
    'Coffee time ☕ #coffee #morning',
    'Sport time 🏃‍♂️ #fitness #active',
    'Rilassamento totale 🧘‍♂️ #zen #peace',
    'Creative vibes 🎨 #design #art',
    'Food porn 🍕 #food #yummy',
  ];

  const locations = [
    'Milano, Italia',
    'Roma, Italia',
    'Torino, Italia',
    'Napoli, Italia',
    'Firenze, Italia',
    'Venezia, Italia',
    'Bologna, Italia',
    'Verona, Italia',
    'Genova, Italia',
    'Palermo, Italia',
  ];

  const posts = [];
  const now = Date.now();

  for (let i = 0; i < 25; i++) {
    const user = USERS[Math.floor(Math.random() * USERS.length)];
    const isVideo = Math.random() > 0.8; // 20% video

    posts.push({
      id: `post_${i + 1}`,
      user: {
        id: user.id,
        username: user.username,
        avatar: user.avatar,
      },
      content: {
        type: isVideo ? POST_TYPES.VIDEO : POST_TYPES.IMAGE,
        uri: isVideo
          ? 'https://sample-videos.com/video321/mp4/720/big_buck_bunny_720p_1mb.mp4'
          : SAMPLE_IMAGES[i % SAMPLE_IMAGES.length],
      },
      caption: captions[Math.floor(Math.random() * captions.length)],
      likes: Math.floor(Math.random() * 5000),
      liked: Math.random() > 0.7,
      comments: Math.floor(Math.random() * 200),
      createdAt: now - (i * 3600000) - Math.floor(Math.random() * 86400000),
      location: locations[Math.floor(Math.random() * locations.length)],
    });
  }

  return posts;
};

const POSTS = generatePosts();

// Genera notifiche
const generateNotifications = () => {
  const notifications = [];
  const now = Date.now();
  const messages = [
    { type: NOTIFICATION_TYPES.LIKE, message: 'ha messo like al tuo post' },
    { type: NOTIFICATION_TYPES.COMMENT, message: 'ha commentato: "Bellissimo!"' },
    { type: NOTIFICATION_TYPES.COMMENT, message: 'ha commentato: "Seguo!"' },
    { type: NOTIFICATION_TYPES.FOLLOW, message: 'ha iniziato a seguirti' },
    { type: NOTIFICATION_TYPES.MENTION, message: 'ti ha menzionato in un commento' },
  ];

  for (let i = 0; i < 30; i++) {
    const user = USERS[Math.floor(Math.random() * USERS.length)];
    const msg = messages[Math.floor(Math.random() * messages.length)];
    const post = POSTS[Math.floor(Math.random() * POSTS.length)];

    notifications.push({
      id: `notif_${i + 1}`,
      type: msg.type,
      user: {
        id: user.id,
        username: user.username,
        avatar: user.avatar,
      },
      post: msg.type !== NOTIFICATION_TYPES.FOLLOW ? {
        id: post.id,
        content: post.content,
      } : null,
      message: msg.message,
      createdAt: now - (i * 1800000) - Math.floor(Math.random() * 3600000),
      read: i > 5,
    });
  }

  return notifications;
};

const NOTIFICATIONS = generateNotifications();

// Genera storie
const generateStories = () => {
  const stories = [];
  const now = Date.now();

  for (let i = 0; i < 10; i++) {
    const user = USERS[i];
    stories.push({
      id: `story_${i + 1}`,
      user: {
        id: user.id,
        username: user.username,
        avatar: user.avatar,
      },
      uri: SAMPLE_IMAGES[i % SAMPLE_IMAGES.length],
      createdAt: now - (i * 3600000),
      viewed: i > 3,
    });
  }

  return stories;
};

const STORIES = generateStories();

// API simulata
class DataService {
  constructor() {
    this.posts = [...POSTS];
    this.notifications = [...NOTIFICATIONS];
    this.stories = [...STORIES];
    this.users = [...USERS];
    this.currentUser = CURRENT_USER;
    this.comments = this.generateComments();
  }

  generateComments() {
    const comments = {};
    const commentTexts = [
      'Bellissimo! 🔥',
      'Fantastico!',
      'Seguito!',
      'Ame questo post ❤️',
      'Incredibile!',
      'Wow!',
      'Grandioso!',
      'Perfetto!',
      'Stupendo!',
      'Meraviglioso!',
    ];

    POSTS.forEach(post => {
      const postComments = [];
      const commentCount = Math.floor(Math.random() * 10) + 1;

      for (let i = 0; i < commentCount; i++) {
        const user = USERS[Math.floor(Math.random() * USERS.length)];
        postComments.push({
          id: `comment_${post.id}_${i + 1}`,
          post: post.id,
          user: {
            id: user.id,
            username: user.username,
            avatar: user.avatar,
          },
          text: commentTexts[Math.floor(Math.random() * commentTexts.length)],
          createdAt: post.createdAt + (i * 60000),
          likes: Math.floor(Math.random() * 50),
        });
      }

      comments[post.id] = postComments;
    });

    return comments;
  }

  // Auth
  getCurrentUser() {
    return new Promise((resolve) => {
      setTimeout(() => resolve(this.currentUser), 300);
    });
  }

  // Posts
  getPosts(page = 1, limit = 10) {
    return new Promise((resolve) => {
      setTimeout(() => {
        const start = (page - 1) * limit;
        const end = start + limit;
        resolve({
          posts: this.posts.slice(start, end),
          hasMore: end < this.posts.length,
          page,
        });
      }, 500);
    });
  }

  getPostById(postId) {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        const post = this.posts.find(p => p.id === postId);
        if (post) {
          resolve(post);
        } else {
          reject(new Error('Post non trovato'));
        }
      }, 300);
    });
  }

  likePost(postId) {
    return new Promise((resolve) => {
      setTimeout(() => {
        const post = this.posts.find(p => p.id === postId);
        if (post) {
          post.liked = true;
          post.likes += 1;
          resolve(post);
        }
      }, 200);
    });
  }

  unlikePost(postId) {
    return new Promise((resolve) => {
      setTimeout(() => {
        const post = this.posts.find(p => p.id === postId);
        if (post) {
          post.liked = false;
          post.likes -= 1;
          resolve(post);
        }
      }, 200);
    });
  }

  createPost(content) {
    return new Promise((resolve) => {
      setTimeout(() => {
        const newPost = {
          id: `post_${Date.now()}`,
          user: this.currentUser,
          content: content,
          caption: '',
          likes: 0,
          liked: false,
          comments: 0,
          createdAt: Date.now(),
        };
        this.posts.unshift(newPost);
        resolve(newPost);
      }, 500);
    });
  }

  // Comments
  getComments(postId) {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve(this.comments[postId] || []);
      }, 300);
    });
  }

  addComment(postId, text) {
    return new Promise((resolve) => {
      setTimeout(() => {
        const newComment = {
          id: `comment_${Date.now()}`,
          post: postId,
          user: this.currentUser,
          text,
          createdAt: Date.now(),
          likes: 0,
        };

        if (!this.comments[postId]) {
          this.comments[postId] = [];
        }
        this.comments[postId].unshift(newComment);

        const post = this.posts.find(p => p.id === postId);
        if (post) {
          post.comments += 1;
        }

        resolve(newComment);
      }, 300);
    });
  }

  likeComment(commentId, postId) {
    return new Promise((resolve) => {
      setTimeout(() => {
        const comment = this.comments[postId]?.find(c => c.id === commentId);
        if (comment) {
          comment.likes += 1;
          resolve(comment);
        }
      }, 200);
    });
  }

  // Users
  searchUsers(query) {
    return new Promise((resolve) => {
      setTimeout(() => {
        if (!query) {
          resolve(this.users.slice(0, 10));
          return;
        }

        const filtered = this.users.filter(user =>
          user.username.toLowerCase().includes(query.toLowerCase())
        );
        resolve(filtered);
      }, 300);
    });
  }

  getUserById(userId) {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        const user = this.users.find(u => u.id === userId);
        if (user) {
          resolve(user);
        } else if (userId === this.currentUser.id) {
          resolve(this.currentUser);
        } else {
          reject(new Error('Utente non trovato'));
        }
      }, 300);
    });
  }

  getUserPosts(userId) {
    return new Promise((resolve) => {
      setTimeout(() => {
        const userPosts = this.posts.filter(p => p.user.id === userId);
        resolve(userPosts);
      }, 300);
    });
  }

  followUser(userId) {
    return new Promise((resolve) => {
      setTimeout(() => {
        const user = this.users.find(u => u.id === userId);
        if (user) {
          user.isFollowing = true;
          user.followers += 1;
          this.currentUser.following += 1;
          resolve(user);
        }
      }, 300);
    });
  }

  unfollowUser(userId) {
    return new Promise((resolve) => {
      setTimeout(() => {
        const user = this.users.find(u => u.id === userId);
        if (user) {
          user.isFollowing = false;
          user.followers -= 1;
          this.currentUser.following -= 1;
          resolve(user);
        }
      }, 300);
    });
  }

  // Notifications
  getNotifications() {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve(this.notifications);
      }, 300);
    });
  }

  markNotificationAsRead(notificationId) {
    return new Promise((resolve) => {
      setTimeout(() => {
        const notification = this.notifications.find(n => n.id === notificationId);
        if (notification) {
          notification.read = true;
          resolve(notification);
        }
      }, 200);
    });
  }

  markAllNotificationsAsRead() {
    return new Promise((resolve) => {
      setTimeout(() => {
        this.notifications.forEach(n => n.read = true);
        resolve(true);
      }, 300);
    });
  }

  getUnreadCount() {
    return new Promise((resolve) => {
      setTimeout(() => {
        const unreadCount = this.notifications.filter(n => !n.read).length;
        resolve(unreadCount);
      }, 200);
    });
  }

  // Stories
  getStories() {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve(this.stories);
      }, 300);
    });
  }

  markStoryAsViewed(storyId) {
    return new Promise((resolve) => {
      setTimeout(() => {
        const story = this.stories.find(s => s.id === storyId);
        if (story) {
          story.viewed = true;
          resolve(story);
        }
      }, 200);
    });
  }

  // Messages
  getConversations() {
    return new Promise((resolve) => {
      setTimeout(() => {
        const conversations = this.users.slice(0, 5).map(user => ({
          id: `conv_${user.id}`,
          user,
          lastMessage: 'Ciao! Come stai?',
          lastMessageTime: Date.now() - Math.floor(Math.random() * 86400000),
          unread: Math.random() > 0.5,
        }));
        resolve(conversations);
      }, 300);
    });
  }

  getMessages(conversationId) {
    return new Promise((resolve) => {
      setTimeout(() => {
        const messages = [
          { id: '1', sender: 'other', text: 'Ciao!', createdAt: Date.now() - 3600000 },
          { id: '2', sender: 'me', text: 'Hey! Come va?', createdAt: Date.now() - 3500000 },
          { id: '3', sender: 'other', text: 'Tutto bene, tu?', createdAt: Date.now() - 3400000 },
          { id: '4', sender: 'me', text: 'Bene grazie!', createdAt: Date.now() - 3300000 },
        ];
        resolve(messages);
      }, 300);
    });
  }

  sendMessage(conversationId, text) {
    return new Promise((resolve) => {
      setTimeout(() => {
        const message = {
          id: `msg_${Date.now()}`,
          sender: 'me',
          text,
          createdAt: Date.now(),
        };
        resolve(message);
      }, 300);
    });
  }
}

export default new DataService();
