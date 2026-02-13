/**
 * Blog Platform MongoDB - Setup Script
 *
 * Questo script crea tutte le collections, gli indici e le configurazioni
 * necessarie per la piattaforma blog.
 *
 * Uso:
 * 1. Avviare MongoDB: mongod
 * 2. Eseguire: node setup.js
 *    oppure nella shell MongoDB: load('setup.js')
 */

// ==================== CONFIGURAZIONE ====================
const DB_NAME = 'blog_platform';

// Connessione al database (per uso con mongosh)
// use blog_platform;

// ==================== CREAZIONE DELLE COLLECTIONS ====================

/**
 * Nota: In MongoDB le collections vengono create automaticamente
 * al primo inserimento. Tuttavia, possiamo crearle esplicitamente
 * con opzioni di validazione.
 */

db.createCollection('users', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['username', 'email', 'password_hash', 'role'],
      properties: {
        username: {
          bsonType: 'string',
          description: 'Username deve essere una stringa ed è obbligatorio'
        },
        email: {
          bsonType: 'string',
          description: 'Email deve essere una stringa ed è obbligatorio'
        },
        password_hash: {
          bsonType: 'string',
          description: 'Password hash deve essere una stringa ed è obbligatorio'
        },
        role: {
          enum: ['author', 'editor', 'admin'],
          description: 'Role deve essere author, editor o admin'
        }
      }
    }
  }
});

db.createCollection('posts', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['title', 'slug', 'content', 'author', 'status'],
      properties: {
        title: {
          bsonType: 'string',
          description: 'Title deve essere una stringa ed è obbligatorio'
        },
        slug: {
          bsonType: 'string',
          description: 'Slug deve essere una stringa ed è obbligatorio'
        },
        content: {
          bsonType: 'string',
          description: 'Content deve essere una stringa ed è obbligatorio'
        },
        status: {
          enum: ['draft', 'published', 'archived'],
          description: 'Status deve essere draft, published o archived'
        },
        featured: {
          bsonType: 'bool',
          description: 'Featured deve essere un booleano'
        },
        views: {
          bsonType: 'int',
          description: 'Views deve essere un intero'
        }
      }
    }
  }
});

db.createCollection('categories', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['name', 'slug'],
      properties: {
        name: {
          bsonType: 'string',
          description: 'Name deve essere una stringa ed è obbligatorio'
        },
        slug: {
          bsonType: 'string',
          description: 'Slug deve essere una stringa ed è obbligatorio'
        }
      }
    }
  }
});

db.createCollection('tags');

print('✓ Collections create con successo');

// ==================== INDICI UNIQUE ====================

// Users: Indici unici
db.users.createIndex(
  { email: 1 },
  { unique: true, name: 'users_email_unique' }
);

db.users.createIndex(
  { username: 1 },
  { unique: true, name: 'users_username_unique' }
);

// Posts: Indice unico su slug (per URL unici)
db.posts.createIndex(
  { slug: 1 },
  { unique: true, name: 'posts_slug_unique' }
);

// Categories: Indice unico su slug
db.categories.createIndex(
  { slug: 1 },
  { unique: true, name: 'categories_slug_unique' }
);

// Tags: Indice unico su slug
db.tags.createIndex(
  { slug: 1 },
  { unique: true, name: 'tags_slug_unique' }
);

print('✓ Indici unique creati con successo');

// ==================== INDICI COMPOUND ====================

// Posts: Status + PublishedAt (per post pubblicati ordinati per data)
db.posts.createIndex(
  { status: 1, publishedAt: -1 },
  { name: 'posts_status_publishedAt' }
);

// Posts: Author + CreatedAt (post per autore ordinati)
db.posts.createIndex(
  { 'author.id': 1, createdAt: -1 },
  { name: 'posts_author_createdAt' }
);

// Posts: Category + Status (post per categoria pubblicati)
db.posts.createIndex(
  { 'category._id': 1, status: 1 },
  { name: 'posts_category_status' }
);

// Posts: Featured + Status + PublishedAt (post in evidenza)
db.posts.createIndex(
  { featured: -1, status: 1, publishedAt: -1 },
  { name: 'posts_featured_status_publishedAt' }
);

// Posts: Views + Status (post più visti)
db.posts.createIndex(
  { views: -1, status: 1 },
  { name: 'posts_views_status' }
);

// Posts: Tag + Status (ricerca per tag)
db.posts.createIndex(
  { tags: 1, status: 1 },
  { name: 'posts_tags_status' }
);

print('✓ Indici compound creati con successo');

// ==================== INDICI TEXT ====================

// Posts: Full-text search su title, content, excerpt
db.posts.createIndex(
  {
    title: 'text',
    content: 'text',
    excerpt: 'text',
    'metadata.keywords': 'text'
  },
  {
    name: 'posts_text_search',
    weights: {
      title: 10,
      content: 5,
      excerpt: 3,
      'metadata.keywords': 2
    },
    default_language: 'italian'
  }
);

// Categories: Text search su name e description
db.categories.createIndex(
  {
    name: 'text',
    description: 'text'
  },
  {
    name: 'categories_text_search',
    default_language: 'italian'
  }
);

// Tags: Text search su name
db.tags.createIndex(
  { name: 'text' },
  {
    name: 'tags_text_search',
    default_language: 'italian'
  }
);

print('✓ Indici text search creati con successo');

// ==================== INDICI SINGLE FIELD ====================

// Users: Indici per ricerche comuni
db.users.createIndex({ role: 1 }, { name: 'users_role' });
db.users.createIndex({ status: 1 }, { name: 'users_status' });
db.users.createIndex({ createdAt: -1 }, { name: 'users_createdAt' });

// Posts: Indici per fields comuni
db.posts.createIndex({ createdAt: -1 }, { name: 'posts_createdAt' });
db.posts.createIndex({ updatedAt: -1 }, { name: 'posts_updatedAt' });

// Categories: Indice per gerarchia
db.categories.createIndex(
  { parentCategory: 1 },
  { name: 'categories_parentCategory', sparse: true }
);

db.categories.createIndex({ order: 1 }, { name: 'categories_order' });
db.categories.createIndex({ postCount: -1 }, { name: 'categories_postCount' });

// Tags: Indice per post count
db.tags.createIndex({ postCount: -1 }, { name: 'tags_postCount' });
db.tags.createIndex({ name: 1 }, { name: 'tags_name' });

print('✓ Indici single field creati con successo');

// ==================== INDICI PER COMMENTI (EMBEDDED) ====================

// Nota: I commenti sono embedded nei posts, ma creiamo indici
// per query che utilizzano operatori sugli array

// Posts: Indice per commenti status
db.posts.createIndex(
  { 'comments.status': 1 },
  { name: 'posts_comments_status', sparse: true }
);

// Posts: Indice per commenti user
db.posts.createIndex(
  { 'comments.user.id': 1 },
  { name: 'posts_comments_user', sparse: true }
);

print('✓ Indici per commenti creati con successo');

// ==================== TTL INDEXES (Opzionale) ====================

// Potenziale indice TTL per eliminare automaticamente i draft vecchi
// db.posts.createIndex(
//   { createdAt: 1 },
//   { expireAfterSeconds: 15778800, name: 'posts_draft_ttl', partialFilterExpression: { status: 'draft' } }
// );

print('⚠ TTL indexes commentati (rimuovere il commento se necessario)');

// ==================== STATISTICHE FINALI ====================

print('\n========================================');
print('SETUP COMPLETATO CON SUCCESSO');
print('========================================\n');

print('DATABASE: ' + DB_NAME);
print('\nCOLLECTIONS:');
print('- users');
print('- posts');
print('- categories');
print('- tags');

print('\nINDICI TOTALI:');
print('Users: ' + db.users.getIndexes().length);
print('Posts: ' + db.posts.getIndexes().length);
print('Categories: ' + db.categories.getIndexes().length);
print('Tags: ' + db.tags.getIndexes().length);

print('\n✓ Database pronto per l\'uso!');
print('\nProssimo passo: Eseguire sample_data.js per popolare il database con dati di esempio.\n');

// ==================== UTILITIES ====================

/**
 * Funzione helper per verificare gli indici creati
 * Eseguire: showIndexes()
 */
function showIndexes() {
  print('\n=== USERS INDEXES ===');
  db.users.getIndexes().forEach(printjson);

  print('\n=== POSTS INDEXES ===');
  db.posts.getIndexes().forEach(printjson);

  print('\n=== CATEGORIES INDEXES ===');
  db.categories.getIndexes().forEach(printjson);

  print('\n=== TAGS INDEXES ===');
  db.tags.getIndexes().forEach(printjson);
}

/**
 * Funzione helper per drop tutti gli indici (tranne _id)
 * Eseguire: dropAllIndexes()
 */
function dropAllIndexes() {
  [db.users, db.posts, db.categories, db.tags].forEach(function(collection) {
    collection.getIndexes().forEach(function(index) {
      if (index.name !== '_id_') {
        collection.dropIndex(index.name);
        print('Dropped: ' + collection.getName() + '.' + index.name);
      }
    });
  });
}

/**
 * Funzione helper per statistiche database
 * Eseguire: dbStats()
 */
function dbStats() {
  print('\n=== DATABASE STATISTICS ===');
  printjson(db.stats());
}
