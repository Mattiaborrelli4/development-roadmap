/**
 * Blog Platform MongoDB - Query Examples
 *
 * Raccolta di query comuni per la piattaforma blog.
 * Ogni query include spiegazione e esempio di utilizzo.
 *
 * Uso:
 * 1. Assicurarsi di aver eseguito setup.js e sample_data.js
 * 2. Eseguire nella shell MongoDB: load('queries.js')
 * 3. Chiamare le funzioni esempio: findPostsByCategory('tecnologia')
 */

// ==================== CONFIGURAZIONE ====================
const DB_NAME = 'blog_platform';

// ==================== 1. POSTS BY CATEGORY ====================

/**
 * Trova tutti i post pubblicati in una specifica categoria
 *
 * @param {string} categorySlug - Lo slug della categoria
 * @param {number} limit - Numero massimo di risultati (default: 10)
 */
function findPostsByCategory(categorySlug, limit = 10) {
  print('\n=== POSTS BY CATEGORY: ' + categorySlug + ' ===\n');

  const posts = db.posts.find(
    {
      'category.slug': categorySlug,
      status: 'published'
    },
    {
      title: 1,
      slug: 1,
      excerpt: 1,
      author: 1,
      'category.name': 1,
      views: 1,
      createdAt: 1,
      publishedAt: 1
    }
  )
  .sort({ publishedAt: -1 })
  .limit(limit)
  .toArray();

  posts.forEach(post => {
    print('📝 ' + post.title);
    print('   👤 ' + post.author.username);
    print('   📁 ' + post.category.name);
    print('   👁️  ' + post.views + ' views');
    print('   📅 ' + post.publishedAt?.toLocaleDateString('it-IT'));
    print('');
  });

  return posts;
}

// Esempio: findPostsByCategory('programmazione', 5);

// ==================== 2. TEXT SEARCH ====================

/**
 * Ricerca full-text nei post (title, content, excerpt, keywords)
 *
 * @param {string} searchTerm - Termine di ricerca
 * @param {number} limit - Numero massimo di risultati (default: 10)
 */
function textSearch(searchTerm, limit = 10) {
  print('\n=== TEXT SEARCH: "' + searchTerm + '" ===\n');

  const posts = db.posts.find(
    {
      $text: { $search: searchTerm },
      status: 'published'
    },
    {
      score: { $meta: 'textScore' },
      title: 1,
      slug: 1,
      excerpt: 1,
      author: 1,
      publishedAt: 1
    }
  )
  .sort({ score: { $meta: 'textScore' } })
  .limit(limit)
  .toArray();

  posts.forEach(post => {
    print('📝 ' + post.title);
    print('   📄 ' + post.excerpt.substring(0, 100) + '...');
    print('   👤 ' + post.author.username);
    print('');
  });

  return posts;
}

// Esempio: textSearch('mongodb tutorial');

// ==================== 3. POSTS BY TAG ====================

/**
 * Trova tutti i post con un tag specifico
 *
 * @param {string} tagName - Nome del tag
 * @param {number} limit - Numero massimo di risultati (default: 10)
 */
function findPostsByTag(tagName, limit = 10) {
  print('\n=== POSTS BY TAG: ' + tagName + ' ===\n');

  const posts = db.posts.find(
    {
      tags: tagName,
      status: 'published'
    },
    {
      title: 1,
      slug: 1,
      excerpt: 1,
      tags: 1,
      author: 1,
      publishedAt: 1
    }
  )
  .sort({ publishedAt: -1 })
  .limit(limit)
  .toArray();

  posts.forEach(post => {
    print('📝 ' + post.title);
    print('   🏷️  ' + post.tags.join(', '));
    print('   👤 ' + post.author.username);
    print('');
  });

  return posts;
}

// Esempio: findPostsByTag('javascript', 5);

// ==================== 4. AGGREGATION: POSTS PER CATEGORY ====================

/**
 * Aggregation pipeline: Conta post pubblicati per categoria
 */
function postsPerCategory() {
  print('\n=== POSTS PER CATEGORY (AGGREGATION) ===\n');

  const result = db.posts.aggregate([
    // Match solo post pubblicati
    { $match: { status: 'published' } },
    // Group per categoria
    {
      $group: {
        _id: '$category.name',
        slug: { $first: '$category.slug' },
        postCount: { $sum: 1 },
        totalViews: { $sum: '$views' },
        avgViews: { $avg: '$views' }
      }
    },
    // Sort per numero di post
    { $sort: { postCount: -1 } },
    // Format output
    {
      $project: {
        _id: 0,
        category: '$_id',
        slug: 1,
        postCount: 1,
        totalViews: 1,
        avgViews: { $round: ['$avgViews', 0] }
      }
    }
  ]).toArray();

  result.forEach(cat => {
    print('📁 ' + cat.category);
    print('   📝 Posts: ' + cat.postCount);
    print('   👁️  Total Views: ' + cat.totalViews);
    print('   📊 Avg Views: ' + cat.avgViews);
    print('');
  });

  return result;
}

// Esempio: postsPerCategory();

// ==================== 5. USER'S POSTS ====================

/**
 * Trova tutti i post di un utente specifico
 *
 * @param {string} username - Username dell'autore
 * @param {boolean} includeDrafts - Includi anche i draft (default: false)
 */
function findUserPosts(username, includeDrafts = false) {
  print('\n=== POSTS BY USER: ' + username + ' ===\n');

  const user = db.users.findOne({ username: username });
  if (!user) {
    print('⚠️  Utente non trovato');
    return [];
  }

  print('👤 ' + user.profile.firstName + ' ' + user.profile.lastName);
  print('📧 ' + user.email);
  print('🔖 ' + user.role);
  print('');

  const query = {
    'author.username': username
  };

  if (!includeDrafts) {
    query.status = 'published';
  }

  const posts = db.posts.find(query)
    .sort({ publishedAt: -1, createdAt: -1 })
    .toArray();

  const stats = {
    total: posts.length,
    published: posts.filter(p => p.status === 'published').length,
    draft: posts.filter(p => p.status === 'draft').length,
    featured: posts.filter(p => p.featured).length,
    totalViews: posts.reduce((sum, p) => sum + p.views, 0)
  };

  print('📊 Statistics:');
  print('   Total: ' + stats.total);
  print('   Published: ' + stats.published);
  print('   Draft: ' + stats.draft);
  print('   Featured: ' + stats.featured);
  print('   Total Views: ' + stats.totalViews);
  print('');

  posts.forEach(post => {
    print('📝 ' + post.title);
    print('   ' + post.status + ' | ' + post.views + ' views');
  });

  return posts;
}

// Esempio: findUserPosts('marirossi123');

// ==================== 6. LATEST POSTS ====================

/**
 * Trova gli ultimi N post pubblicati
 *
 * @param {number} limit - Numero di post da restituire (default: 10)
 */
function findLatestPosts(limit = 10) {
  print('\n=== LATEST POSTS ===\n');

  const posts = db.posts.find(
    { status: 'published' },
    {
      title: 1,
      slug: 1,
      excerpt: 1,
      author: 1,
      'category.name': 1,
      publishedAt: 1,
      views: 1
    }
  )
  .sort({ publishedAt: -1 })
  .limit(limit)
  .toArray();

  posts.forEach((post, index) => {
    print((index + 1) + '. ' + post.title);
    print('   👤 ' + post.author.username);
    print('   📁 ' + post.category.name);
    print('   📅 ' + post.publishedAt?.toLocaleDateString('it-IT'));
    print('   👁️  ' + post.views + ' views');
    print('');
  });

  return posts;
}

// Esempio: findLatestPosts(5);

// ==================== 7. FEATURED POSTS ====================

/**
 * Trova tutti i post in evidenza
 *
 * @param {number} limit - Numero massimo di risultati (default: 10)
 */
function findFeaturedPosts(limit = 10) {
  print('\n=== FEATURED POSTS ===\n');

  const posts = db.posts.find(
    {
      featured: true,
      status: 'published'
    },
    {
      title: 1,
      slug: 1,
      excerpt: 1,
      author: 1,
      'category.name': 1,
      views: 1,
      publishedAt: 1
    }
  )
  .sort({ publishedAt: -1 })
  .limit(limit)
  .toArray();

  posts.forEach(post => {
    print('⭐ ' + post.title);
    print('   👤 ' + post.author.username);
    print('   📁 ' + post.category.name);
    print('   👁️  ' + post.views + ' views');
    print('   📅 ' + post.publishedAt?.toLocaleDateString('it-IT'));
    print('');
  });

  return posts;
}

// Esempio: findFeaturedPosts();

// ==================== 8. POST WITH COMMENTS ====================

/**
 * Trova un post e i suoi commenti
 *
 * @param {string} slug - Slug del post
 */
function findPostWithComments(slug) {
  print('\n=== POST WITH COMMENTS: ' + slug + ' ===\n');

  const post = db.posts.findOne({ slug: slug });

  if (!post) {
    print('⚠️  Post non trovato');
    return null;
  }

  print('📝 ' + post.title);
  print('👤 ' + post.author.username);
  print('📁 ' + post.category.name);
  print('🏷️  ' + post.tags.join(', '));
  print('👁️  ' + post.views + ' views');
  print('📅 ' + post.publishedAt?.toLocaleDateString('it-IT'));
  print('\n' + post.excerpt);
  print('\n---\n');

  // Commenti approvati
  const approvedComments = post.comments.filter(c => c.status === 'approved');
  print('💬 Commenti (' + approvedComments.length + '):');

  approvedComments.forEach(comment => {
    print('\n   👤 ' + comment.user.username);
    print('   📅 ' + comment.createdAt.toLocaleDateString('it-IT'));
    print('   💭 ' + comment.content);
  });

  if (approvedComments.length === 0) {
    print('\n   Nessun commento aprovato.');
  }

  return post;
}

// Esempio: findPostWithComments('introduzione-a-mongodb-guida-completa');

// ==================== 9. POSTS BY DATE RANGE ====================

/**
 * Trova post pubblicati in un range di date
 *
 * @param {Date|string} startDate - Data inizio
 * @param {Date|string} endDate - Data fine
 */
function findPostsByDateRange(startDate, endDate) {
  print('\n=== POSTS BY DATE RANGE ===\n');
  print('📅 Da: ' + new Date(startDate).toLocaleDateString('it-IT'));
  print('📅 A: ' + new Date(endDate).toLocaleDateString('it-IT'));
  print('');

  const posts = db.posts.find(
    {
      status: 'published',
      publishedAt: {
        $gte: new Date(startDate),
        $lte: new Date(endDate)
      }
    },
    {
      title: 1,
      slug: 1,
      author: 1,
      publishedAt: 1,
      views: 1
    }
  )
  .sort({ publishedAt: -1 })
  .toArray();

  print('📝 Totale: ' + posts.length + ' posts\n');

  posts.forEach(post => {
    print('• ' + post.title);
    print('  👤 ' + post.author.username);
    print('  📅 ' + post.publishedAt.toLocaleDateString('it-IT'));
    print('');
  });

  return posts;
}

// Esempio: findPostsByDateRange('2024-01-01', '2024-12-31');

// ==================== 10. TAG CLOUD (AGGREGATION) ====================

/**
 * Genera una tag cloud con i tag più utilizzati
 * Usa aggregation per contare i post per tag
 *
 * @param {number} limit - Numero massimo di tag (default: 30)
 */
function generateTagCloud(limit = 30) {
  print('\n=== TAG CLOUD (TOP ' + limit + ') ===\n');

  const result = db.posts.aggregate([
    // Match solo post pubblicati
    { $match: { status: 'published' } },
    // Unwind dell'array tags
    { $unwind: '$tags' },
    // Group per tag e conta
    {
      $group: {
        _id: '$tags',
        postCount: { $sum: 1 },
        totalViews: { $sum: '$views' }
      }
    },
    // Sort per post count
    { $sort: { postCount: -1 } },
    // Limita risultati
    { $limit: limit },
    // Format output
    {
      $project: {
        _id: 0,
        tag: '$_id',
        postCount: 1,
        totalViews: 1,
        avgViews: { $round: [{ $divide: ['$totalViews', '$postCount'] }, 0] }
      }
    }
  ]).toArray();

  result.forEach(tag => {
    const size = Math.min(1 + Math.log(tag.postCount) * 3, 5);
    const bar = '█'.repeat(Math.round(size));
    print(bar + ' ' + tag.tag + ' (' + tag.postCount + ' posts, ' + tag.totalViews + ' views)');
  });

  return result;
}

// Esempio: generateTagCloud(20);

// ==================== 11. CATEGORY HIERARCHY ====================

/**
 * Trova tutte le categorie con eventuali sottocategorie
 */
function getCategoryHierarchy() {
  print('\n=== CATEGORY HIERARCHY ===\n');

  const categories = db.categories.find().sort({ order: 1 }).toArray();

  const rootCategories = categories.filter(c => !c.parentCategory);

  function printCategory(category, level = 0) {
    const indent = '  '.repeat(level);
    const children = categories.filter(c =>
      c.parentCategory && c.parentCategory.toString() === category._id.toString()
    );

    print(indent + '📁 ' + category.name + ' (' + category.postCount + ' posts)');
    print(indent + '   ' + category.slug);

    if (children.length > 0) {
      children.forEach(child => printCategory(child, level + 1));
    }
  }

  rootCategories.forEach(cat => {
    printCategory(cat);
    print('');
  });

  return categories;
}

// Esempio: getCategoryHierarchy();

// ==================== 12. POPULAR POSTS ====================

/**
 * Trova i post più visti
 *
 * @param {number} limit - Numero massimo di risultati (default: 10)
 */
function findPopularPosts(limit = 10) {
  print('\n=== MOST POPULAR POSTS ===\n');

  const posts = db.posts.find(
    { status: 'published' },
    {
      title: 1,
      slug: 1,
      author: 1,
      'category.name': 1,
      views: 1,
      publishedAt: 1
    }
  )
  .sort({ views: -1 })
  .limit(limit)
  .toArray();

  posts.forEach((post, index) => {
    print((index + 1) + '. ' + post.title);
    print('   👤 ' + post.author.username);
    print('   👁️  ' + post.views + ' views');
    print('   📅 ' + post.publishedAt?.toLocaleDateString('it-IT'));
    print('');
  });

  return posts;
}

// Esempio: findPopularPosts(5);

// ==================== 13. RELATED POSTS ====================

/**
 * Trova post correlati (stessa categoria o tag simili)
 *
 * @param {string} postId - ID del post di riferimento
 * @param {number} limit - Numero massimo di risultati (default: 5)
 */
function findRelatedPosts(postId, limit = 5) {
  print('\n=== RELATED POSTS ===\n');

  const originalPost = db.posts.findOne({ _id: ObjectId(postId) });

  if (!originalPost) {
    print('⚠️  Post non trovato');
    return [];
  }

  print('📝 Post originale: ' + originalPost.title);
  print('📁 Categoria: ' + originalPost.category.name);
  print('🏷️  Tags: ' + originalPost.tags.join(', '));
  print('\n---\n');

  // Trova post con stessa categoria o almeno un tag in comune
  const related = db.posts.find(
    {
      _id: { $ne: ObjectId(postId) },
      status: 'published',
      $or: [
        { 'category._id': originalPost.category._id },
        { tags: { $in: originalPost.tags } }
      ]
    },
    {
      title: 1,
      slug: 1,
      author: 1,
      'category.name': 1,
      tags: 1,
      views: 1
    }
  )
  .limit(limit)
  .toArray();

  related.forEach(post => {
    const commonTags = post.tags.filter(t => originalPost.tags.includes(t));
    print('📝 ' + post.title);
    print('   👤 ' + post.author.username);
    print('   🏷️  Tags in comune: ' + (commonTags.length > 0 ? commonTags.join(', ') : 'Nessuno'));
    print('   👁️  ' + post.views + ' views');
    print('');
  });

  return related;
}

// Esempio: findRelatedPosts('...id del post...');

// ==================== 14. AUTHOR LEADERBOARD ====================

/**
 * Classifica degli autori per numero di post e views totali
 */
function getAuthorLeaderboard() {
  print('\n=== AUTHOR LEADERBOARD ===\n');

  const result = db.posts.aggregate([
    // Match solo post pubblicati
    { $match: { status: 'published' } },
    // Group per autore
    {
      $group: {
        _id: '$author.username',
        author: { $first: '$author' },
        postCount: { $sum: 1 },
        totalViews: { $sum: '$views' },
        avgViews: { $avg: '$views' },
        featuredCount: { $sum: { $cond: ['$featured', 1, 0] } }
      }
    },
    // Sort per views totali
    { $sort: { totalViews: -1 } },
    // Format output
    {
      $project: {
        _id: 0,
        username: '$_id',
        avatar: '$author.avatar',
        postCount: 1,
        totalViews: 1,
        avgViews: { $round: ['$avgViews', 0] },
        featuredCount: 1
      }
    }
  ]).toArray();

  result.forEach((author, index) => {
    print((index + 1) + '. ' + author.username);
    print('   📝 Posts: ' + author.postCount);
    print('   👁️  Total Views: ' + author.totalViews);
    print('   📊 Avg Views: ' + author.avgViews);
    print('   ⭐ Featured: ' + author.featuredCount);
    print('');
  });

  return result;
}

// Esempio: getAuthorLeaderboard();

// ==================== 15. SEARCH WITH FILTERS ====================

/**
 * Ricerca avanzata con filtri multipli
 *
 * @param {Object} filters - Oggetto con filtri
 *   - searchTerm: stringa per full-text search
 *   - category: slug categoria
 *   - tags: array di tag
 *   - author: username autore
 *   - dateFrom: data inizio
 *   - dateTo: data fine
 *   - featured: boolean
 *   - sortBy: 'date' | 'views' | 'relevance'
 *   - limit: numero risultati
 */
function searchWithFilters(filters = {}) {
  print('\n=== ADVANCED SEARCH ===\n');

  const query = { status: 'published' };

  // Full-text search
  if (filters.searchTerm) {
    query.$text = { $search: filters.searchTerm };
  }

  // Category filter
  if (filters.category) {
    query['category.slug'] = filters.category;
  }

  // Tags filter
  if (filters.tags && filters.tags.length > 0) {
    query.tags = { $in: filters.tags };
  }

  // Author filter
  if (filters.author) {
    query['author.username'] = filters.author;
  }

  // Date range filter
  if (filters.dateFrom || filters.dateTo) {
    query.publishedAt = {};
    if (filters.dateFrom) {
      query.publishedAt.$gte = new Date(filters.dateFrom);
    }
    if (filters.dateTo) {
      query.publishedAt.$lte = new Date(filters.dateTo);
    }
  }

  // Featured filter
  if (filters.featured !== undefined) {
    query.featured = filters.featured;
  }

  // Sort
  let sort = {};
  const projection = { score: { $meta: 'textScore' } };

  switch (filters.sortBy) {
    case 'views':
      sort = { views: -1 };
      break;
    case 'date':
      sort = { publishedAt: -1 };
      break;
    case 'relevance':
    default:
      if (filters.searchTerm) {
        sort = { score: { $meta: 'textScore' } };
      } else {
        sort = { publishedAt: -1 };
      }
  }

  const limit = filters.limit || 10;

  const posts = db.posts.find(query, projection)
    .sort(sort)
    .limit(limit)
    .toArray();

  print('🔍 Filtri applicati:');
  print('   Search: ' + (filters.searchTerm || 'N/A'));
  print('   Category: ' + (filters.category || 'N/A'));
  print('   Tags: ' + (filters.tags?.join(', ') || 'N/A'));
  print('   Author: ' + (filters.author || 'N/A'));
  print('   Featured: ' + (filters.featured !== undefined ? filters.featured : 'N/A'));
  print('   Sort by: ' + (filters.sortBy || 'date'));
  print('\n📝 Risultati: ' + posts.length + '\n');

  posts.forEach((post, index) => {
    print((index + 1) + '. ' + post.title);
    print('   👤 ' + post.author.username);
    print('   📁 ' + post.category.name);
    print('   👁️  ' + post.views + ' views');
    print('');
  });

  return posts;
}

// Esempi:
// searchWithFilters({ searchTerm: 'javascript', sortBy: 'relevance', limit: 5 });
// searchWithFilters({ category: 'tecnologia', sortBy: 'views', limit: 5 });
// searchWithFilters({ tags: ['mongodb', 'nodejs'], sortBy: 'date', limit: 10 });

// ==================== 16. MONTHLY ARCHIVE ====================

/**
 * Raggruppa i post per mese (archivio mensile)
 */
function getMonthlyArchive() {
  print('\n=== MONTHLY ARCHIVE ===\n');

  const result = db.posts.aggregate([
    // Match solo post pubblicati
    { $match: { status: 'published' } },
    // Crea campi anno-mese
    {
      $project: {
        title: 1,
        slug: 1,
        publishedAt: 1,
        year: { $year: '$publishedAt' },
        month: { $month: '$publishedAt' }
      }
    },
    // Group per anno-mese
    {
      $group: {
        _id: { year: '$year', month: '$month' },
        postCount: { $sum: 1 },
        posts: {
          $push: {
            title: '$title',
            slug: '$slug',
            publishedAt: '$publishedAt'
          }
        }
      }
    },
    // Sort per anno-mese decrescente
    { $sort: { '_id.year': -1, '_id.month': -1 } },
    // Format output
    {
      $project: {
        _id: 0,
        year: '$_id.year',
        month: '$_id.month',
        postCount: 1,
        posts: { $slice: ['$posts', 5] } // Max 5 posts per mese
      }
    }
  ]).toArray();

  const monthNames = [
    '', 'Gennaio', 'Febbraio', 'Marzo', 'Aprile', 'Maggio', 'Giugno',
    'Luglio', 'Agosto', 'Settembre', 'Ottobre', 'Novembre', 'Dicembre'
  ];

  result.forEach(archive => {
    print('📅 ' + monthNames[archive.month] + ' ' + archive.year);
    print('   (' + archive.postCount + ' posts)');
    archive.posts.forEach(post => {
      print('   • ' + post.title);
    });
    print('');
  });

  return result;
}

// Esempio: getMonthlyArchive();

// ==================== SUMMARY ====================

/**
 * Mostra un riepilogo di tutte le funzioni disponibili
 */
function showQueryHelp() {
  print('\n╔════════════════════════════════════════════════════════════╗');
  print('║        BLOG PLATFORM - QUERY FUNCTIONS                   ║');
  print('╚════════════════════════════════════════════════════════════╝\n');

  print('📚 POST QUERIES:');
  print('   findPostsByCategory(slug, limit)');
  print('   textSearch(searchTerm, limit)');
  print('   findPostsByTag(tagName, limit)');
  print('   findLatestPosts(limit)');
  print('   findFeaturedPosts(limit)');
  print('   findPopularPosts(limit)');
  print('   findPostsByDateRange(startDate, endDate)');
  print('   findPostWithComments(slug)');
  print('   findRelatedPosts(postId, limit)');

  print('\n📊 AGGREGATIONS:');
  print('   postsPerCategory()');
  print('   generateTagCloud(limit)');
  print('   getAuthorLeaderboard()');
  print('   getMonthlyArchive()');

  print('\n👤 USER QUERIES:');
  print('   findUserPosts(username, includeDrafts)');

  print('\n🗂️  CATEGORY QUERIES:');
  print('   getCategoryHierarchy()');

  print('\n🔍 ADVANCED:');
  print('   searchWithFilters(filters)');

  print('\nℹ️  HELP:');
  print('   showQueryHelp()');
  print('\n');
}

// Mostra help automaticamente
showQueryHelp();

print('\n✓ Queries caricate. Usa showQueryHelp() per vedere tutte le funzioni.\n');
