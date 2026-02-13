/**
 * Blog Platform MongoDB - Sample Data Generator
 *
 * Questo script popola il database con dati di esempio per testing.
 *
 * Uso:
 * 1. Assicurarsi di aver eseguito setup.js prima
 * 2. Eseguire: node sample_data.js
 *    oppure nella shell MongoDB: load('sample_data.js')
 */

// ==================== CONFIGURAZIONE ====================
const DB_NAME = 'blog_platform';

// ==================== UTILITY FUNCTIONS ====================

/**
 * Genera un ObjectId casuale
 */
function randomId() {
  return new ObjectId();
}

/**
 * Genera un numero casuale tra min e max
 */
function randomInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

/**
 * Seleziona un elemento casuale da un array
 */
function randomChoice(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

/**
 * Seleziona n elementi casuali da un array
 */
function randomChoices(arr, n) {
  const shuffled = [...arr].sort(() => 0.5 - Math.random());
  return shuffled.slice(0, n);
}

/**
 * Genera una data casuale negli ultimi 365 giorni
 */
function randomDate() {
  const now = new Date();
  const past = new Date(now.getTime() - 365 * 24 * 60 * 60 * 1000);
  return new Date(past.getTime() + Math.random() * (now.getTime() - past.getTime()));
}

/**
 * Genera uno slug da una stringa
 */
function generateSlug(text) {
  return text
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

/**
 * Genera un excerpt dal content
 */
function generateExcerpt(content, length = 150) {
  return content.length > length
    ? content.substring(0, length) + '...'
    : content;
}

// ==================== DATA CONSTANTS ====================

const ROLES = ['author', 'editor', 'admin'];
const STATUSES = ['active', 'inactive', 'pending'];
const POST_STATUSES = ['draft', 'published', 'archived'];
const CATEGORIES = [
  { name: 'Tecnologia', description: 'Articoli su tecnologia e innovazione' },
  { name: 'Programmazione', description: 'Guide e tutorial di programmazione' },
  { name: 'Web Development', description: 'Sviluppo web moderno' },
  { name: 'Mobile', description: 'Sviluppo mobile app' },
  { name: 'DevOps', description: 'DevOps e CI/CD' },
  { name: 'Database', description: 'Database e modellazione dati' },
  { name: 'AI & Machine Learning', description: 'Intelligenza artificiale e ML' },
  { name: 'Cybersecurity', description: 'Sicurezza informatica' },
  { name: 'Career', description: 'Consigli per la carriera tech' },
  { name: 'Tutorial', description: 'Tutorial passo-passo' },
  { name: 'JavaScript', description: 'Programmazione JavaScript' },
  { name: 'Python', description: 'Programmazione Python' },
  { name: 'React', description: 'Framework React' },
  { name: 'Node.js', description: 'Node.js e backend development' }
];

const TAGS = [
  'javascript', 'python', 'java', 'csharp', 'php', 'typescript',
  'react', 'vue', 'angular', 'svelte', 'nextjs', 'nuxt',
  'nodejs', 'express', 'nest', 'django', 'flask', 'fastapi',
  'mongodb', 'postgresql', 'mysql', 'redis', 'elasticsearch',
  'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'terraform',
  'git', 'github', 'gitlab', 'cicd', 'jenkins', 'github-actions',
  'html', 'css', 'sass', 'tailwind', 'bootstrap', 'mui',
  'api', 'rest', 'graphql', 'websocket', 'grpc',
  'testing', 'jest', 'cypress', 'playwright', 'selenium',
  'frontend', 'backend', 'fullstack', 'devops', 'mobile',
  'ai', 'machine-learning', 'deep-learning', 'nlp', 'cv',
  'security', 'performance', 'optimization', 'architecture',
  'tutorial', 'tips', 'best-practices', 'patterns', 'algoritmi'
];

const TITLES = [
  'Introduzione a MongoDB: Guida Completa',
  'Come Costruire REST API con Node.js e Express',
  'React vs Vue: Confronto Dettagliato nel 2024',
  '10 Best Practices per TypeScript in Produzione',
  'Tutorial: Creare una App Mobile con React Native',
  'Docker per Principianti: Containerizzazione Semplificata',
  'Python per Data Science: Le Librerie Essenziali',
  'Sicurezza delle API: Autenticazione JWT Implementata',
  'GraphQL vs REST: Quando Scegliere Quale',
  'Kubernetes: Orchestrazione di Container in Produzione',
  'Tutorial: Deploy Applicazione su AWS con Terraform',
  'JavaScript Async/Await: Gestione Promesse Avanzata',
  'Design Patterns in Node.js: Singleton, Factory, Observer',
  'Next.js 14: Server Components e App Router',
  'Python Type Hints: Scrivere Codice più Pulito',
  'Redis per Caching: Ottimizzazione Performance',
  'Cybersecurity Basics: Proteggere le Applicazioni Web',
  'Git Workflow: Branching Strategy per Team',
  'CSS Grid vs Flexbox: Quando Usarli',
  'Machine Learning con Python: Scikit-learn Tutorial',
  'Microservizi vs Monolite: Architettura a Confronto',
  'PostgreSQL vs MongoDB: Database Showdown',
  'Vue 3 Composition API: Guida Completa',
  'Angular 17: Standalone Components e Signals',
  'Tailwind CSS: Styling Rapido e Responsive',
  'Testing con Jest: Unit Testing Best Practices',
  'Elasticsearch: Motore di Ricerca Potente',
  'CI/CD con GitHub Actions: Automatizzare il Deploy',
  'WebSockets: Comunicazione Real-time con Socket.io',
  'SQL vs NoSQL: Quando Scegliere il Database Giusto',
  'TypeScript Generics: Codice Flessibile e Type-Safe',
  'React Hooks: useState, useEffect, useContext',
  'Node.js Performance: Ottimizzazione e Profiling',
  'Python Decorators: Metaprogrammazione Semplificata',
  'MongoDB Aggregation Pipeline: Data Processing',
  'React Query: Server State Management',
  'Prisma ORM: Type-Safe Database Access',
  'SvelteKit: Full-stack Framework Moderno',
  'NestJS: Architettura Enterprise Node.js',
  'Django REST Framework: API Pythoniche',
  'FastAPI: Python High-Performance API',
  'CSS-in-JS: Styled Components vs Emotion',
  'Webpack 5: Bundling Configuration Guide',
  'Vite: Build Tool Istantaneo per Frontend',
  'Redux Toolkit: State Management Semplificato',
  'Zustand vs Redux: State Confronto',
  'Puppeteer: Web Scraping e Automation',
  'Three.js: 3D Graphics nel Browser',
  'WebAssembly: Performance Native nel Web',
  'Serverless: AWS Lambda Function Deployment',
  'Terraform: Infrastructure as Code Guide',
  'Ansible: Configuration Automation'
];

const CONTENTS = [
  `In questo articolo esploreremo in dettaglio questo argomento fondamentale per ogni sviluppatore moderno. Iniziamo con i concetti base e poi approfondiamo gli aspetti più avanzati.

La tecnologia si evolve rapidamente e rimanere aggiornati è essenziale. Vediamo come implementare le best practices nei nostri progetti quotidiani.

## Sezione 1: Fondamenti

Comprendiamo prima i concetti fondamentali. Queste basi sono cruciali per costruire una solida conoscenza.

## Sezione 2: Implementazione Pratica

Ora passiamo alla pratica con esempi concreti di codice che puoi utilizzare immediatamente nei tuoi progetti.

## Conclusione

Abbiamo coperto gli aspetti principali di questo argomento. Continua a sperimentare e approfondire per diventare un esperto.`,

  `Benvenuti in questa guida completa. Oggi impariamo come padroneggiare questa tecnologia fondamentale per lo sviluppo moderno.

Iniziamo con una panoramica completa, poi scendiamo nei dettagli tecnici con esempi pratici.

## Perché è Importante?

Comprendere questo argomento ti darà un vantaggio competitivo nel mercato del lavoro e ti permetterà di costruire applicazioni migliori.

## Esempi Pratici

Vediamo alcuni esempi di codice reali che puoi utilizzare subito:

\`\`\`javascript
// Esempio di implementazione
const example = {
  key: 'value',
  method: function() {
    return 'result';
  }
};
\`\`\`

## Best Practices

Segui queste best practices per ottenere i migliori risultati:
- Pianifica prima di implementare
- Scrivi codice pulito e leggibile
- Testa tutto il tuo codice
- Documenta il tuo lavoro

Continua a imparare e sperimentare!`,

  `Questa è una guida pratica per chi vuole approfondire questo argomento cruciale. Seguiamo un approccio passo-passo.

## Introduzione

Partiamo dalle basi e costruiamo la nostra conoscenza gradualmente. Ogni sezione si basa sulla precedente.

## Passo 1: Configurazione

La configurazione corretta è fondamentale per il successo. Vediamo come impostare tutto correttamente.

## Passo 2: Implementazione

Ora implementiamo la soluzione passo dopo passo, assicurandoci di comprendere ogni parte.

## Passo 3: Testing

Il testing è essenziale. Vediamo come testare la nostra implementazione.

## Troubleshooting

Problemi comuni e come risolverli:
- Errore X: Soluzione
- Warning Y: Come gestirlo
- Performance: Ottimizzazioni

## Risorse Utili

Ecco alcune risorse aggiuntive per approfondire:
- Documentazione ufficiale
- Community e forum
- Tutorial e video

Buono studio!`,

  `Oggi esploriamo uno degli argomenti più richiesti nello sviluppo software moderno. Preparati per una guida completa!

## Overview

Prima di tutto, capiamo perché questo argomento è così importante e come si applica allo sviluppo reale.

## Concetti Chiave

I concetti chiave che devi comprendere:
1. Architettura e design
2. Implementazione pratica
3. Best practices
4. Testing e debugging
5. Ottimizzazione performance

## Deep Dive

Ora approfondiamo ogni concetto con esempi pratici e spiegazioni dettagliate.

## Casi d'Uso Reali

Vediamo come questo viene utilizzato in produzione da aziende leader nel settore.

## Conclusioni

Siamo giunti alla fine di questa guida. Hai ora tutte le conoscenze necessarie per iniziare a utilizzare questa tecnologia nei tuoi progetti.`,

  `Sei pronto per portare le tue competenze al livello successivo? Questo articolo è esattamente quello che ti serve!

## Perché Questa Guida?

Ho creato questa guida basandomi su anni di esperienza nel campo. Copre tutto quello che avrei voluto sapere quando ho iniziato.

## Roadmap

Segui questa roadmap per massimizzare il tuo apprendimento:
1. Fondamenti (2 settimane)
2. Intermedio (1 mese)
3. Avanzato (2 mesi)
4. Esperto (continuo)

## Progetti Pratici

Impara facendo. Ecco alcuni progetti per mettere in pratica:
- Project 1: Beginner friendly
- Project 2: Intermediate level
- Project 3: Advanced challenge

## Community

Unisciti alla community per:
- Supporto e aiuto
- Networking
- Opportunità di lavoro

## Continua a Imparare

Il learning non finisce mai. Ecco come rimanere aggiornato:
- Newsletter
- Podcast
- Conferences
- Workshop`
];

const BIOS = [
  'Sviluppatore full-stack con 5+ anni di esperienza. Appassionato di open source.',
  'Tech lead specializzato in frontend development. Amo React e TypeScript.',
  'Backend engineer con focus su performance e scalabilità. MongoDB expert.',
  'Sviluppatore JavaScript/MERN stack. Creator di diversi progetti open source.',
  'DevOps engineer con esperienza in cloud e containerizzazione.',
  'Data Scientist con background in matematica. Python enthusiast.',
  'Mobile developer (React Native). Ho pubblicato diverse app.',
  'Full-stack developer, tech writer e speaker. Amo condividere conoscenze.',
  'Software architect con 10+ anni di esperienza. Ex-Google, ex-Microsoft.',
  'Sviluppatore web freelance. Specializzato in e-commerce e CMS.',
  'UI/UX developer con occhio per il design. React e CSS expert.',
  'Backend engineer, lover of clean code e best practices.',
  'Machine Learning engineer. PhD in Computer Science.',
  'Senior developer, mentor e content creator. YouTube tech channel.',
  'Cloud architect, AWS certified. Specializzato in serverless.',
  'Frontend developer, Vue.js core team contributor.',
  'Database administrator con expertise in SQL e NoSQL.',
  'Cybersecurity specialist. Ethical hacker e security researcher.',
  'Game developer con Unity e Unreal Engine.',
  'IoT developer. Maker e electronics enthusiast.',
  'Blockchain developer. Smart contracts e DeFi.',
  'QA engineer con focus su automation testing.',
  'Technical writer e developer advocate. Ex-documentazione MongoDB.',
  'Engineering manager con background in development.',
  'Startup CTO. Ho scalato diverse aziende da 0 a 1M+ users.'
];

// ==================== GENERAZIONE CATEGORIES ====================

print('📁 Generazione categories...');

const categoriesData = [];
const categoriesMap = new Map();

// Crea categorie principali
CATEGORIES.slice(0, 10).forEach((cat, index) => {
  const slug = generateSlug(cat.name);
  const category = {
    _id: randomId(),
    name: cat.name,
    slug: slug,
    description: cat.description,
    parentCategory: null,
    order: index,
    postCount: 0
  };
  categoriesData.push(category);
  categoriesMap.set(slug, category._id);
});

// Crea sottocategorie (nested)
CATEGORIES.slice(10).forEach((cat, index) => {
  const parentCategory = randomChoice([...categoriesData.values()]);
  const slug = generateSlug(cat.name);
  const category = {
    _id: randomId(),
    name: cat.name,
    slug: slug,
    description: cat.description,
    parentCategory: parentCategory._id,
    order: index,
    postCount: 0
  };
  categoriesData.push(category);
  categoriesMap.set(slug, category._id);
});

db.categories.insertMany(categoriesData);
print('✓ Categories create: ' + categoriesData.length);

// ==================== GENERAZIONE TAGS ====================

print('\n🏷️  Generazione tags...');

const tagsData = TAGS.map(tag => ({
  _id: randomId(),
  name: tag,
  slug: generateSlug(tag),
  postCount: 0
}));

db.tags.insertMany(tagsData);
print('✓ Tags creati: ' + tagsData.length);

// ==================== GENERAZIONE USERS ====================

print('\n👤 Generazione users...');

const usersData = [];
const usernames = [];
const emails = [];
const firstNames = ['Mario', 'Luca', 'Giulia', 'Anna', 'Marco', 'Sofia', 'Alessandro', 'Francesca', 'Lorenzo', 'Chiara', 'Davide', 'Elena', 'Matteo', 'Sara', 'Federico', 'Valentina', 'Riccardo', 'Martina', 'Andrea', 'Paolo'];
const lastNames = ['Rossi', 'Bianchi', 'Verdi', 'Ferrari', 'Romano', 'Colombo', 'Ricci', 'Marino', 'Greco', 'Bruno', 'Gallo', 'Conti', 'Costa', 'Giordano', 'Mancini', 'Rizzo', 'Lombardi', 'Moretti', 'Barbieri', 'Santoro'];

for (let i = 0; i < 25; i++) {
  const firstName = firstNames[i];
  const lastName = lastNames[i];
  const username = firstName.toLowerCase() + lastName.toLowerCase() + randomInt(1, 999);
  const email = firstName.toLowerCase() + '.' + lastName.toLowerCase() + randomInt(1, 999) + '@example.com';

  usernames.push(username);
  emails.push(email);

  const user = {
    _id: randomId(),
    username: username,
    email: email,
    password_hash: '$2b$10$abcdefghijklmnopqrstuvwxyz123456', // Hash fittizio
    profile: {
      firstName: firstName,
      lastName: lastName,
      bio: BIOS[i % BIOS.length],
      avatar: `https://i.pravatar.cc/150?img=${i + 1}`
    },
    role: ROLES[Math.floor(Math.random() * ROLES.length)],
    status: STATUSES[Math.floor(Math.random() * STATUSES.length)],
    createdAt: randomDate(),
    lastLogin: randomDate()
  };

  usersData.push(user);
}

db.users.insertMany(usersData);
print('✓ Users creati: ' + usersData.length);

// ==================== GENERAZIONE POSTS ====================

print('\n📝 Generazione posts...');

const postsData = [];
const usedSlugs = new Set();

for (let i = 0; i < 60; i++) {
  // Genera slug univoco
  let slug;
  do {
    const titleIndex = i % TITLES.length;
    slug = generateSlug(TITLES[titleIndex]);
    if (usedSlugs.has(slug)) {
      slug = slug + '-' + randomInt(1, 999);
    }
  } while (usedSlugs.has(slug));
  usedSlugs.add(slug);

  const title = TITLES[i % TITLES.length];
  const content = CONTENTS[i % CONTENTS.length];
  const author = randomChoice(usersData);
  const category = randomChoice(categoriesData);
  const postTags = randomChoices(TAGS, randomInt(3, 8));
  const status = POST_STATUSES[Math.floor(Math.random() * POST_STATUSES.length)];

  const createdAt = randomDate();
  const publishedAt = status === 'published' ? createdAt : null;

  const post = {
    _id: randomId(),
    title: title,
    slug: slug,
    content: content,
    excerpt: generateExcerpt(content, 160),
    author: {
      id: author._id,
      username: author.username,
      avatar: author.profile.avatar
    },
    category: {
      _id: category._id,
      name: category.name,
      slug: category.slug
    },
    tags: postTags,
    status: status,
    featured: Math.random() > 0.8, // 20% featured
    views: randomInt(0, 5000),
    metadata: {
      seoTitle: title + ' | Blog Platform',
      seoDescription: generateExcerpt(content, 155),
      keywords: postTags.slice(0, 5)
    },
    comments: [],
    createdAt: createdAt,
    updatedAt: new Date(createdAt.getTime() + randomInt(0, 7 * 24 * 60 * 60 * 1000)),
    publishedAt: publishedAt
  };

  // Aggiungi commenti ai post pubblicati
  if (status === 'published') {
    const numComments = randomInt(0, 15);
    for (let j = 0; j < numComments; j++) {
      const commentAuthor = randomChoice(usersData);
      const commentStatuses = ['approved', 'pending', 'spam'];
      const comment = {
        _id: randomId(),
        user: {
          id: commentAuthor._id,
          username: commentAuthor.username,
          avatar: commentAuthor.profile.avatar
        },
        content: generateExcerpt(CONTENTS[j % CONTENTS.length], 200),
        createdAt: new Date(createdAt.getTime() + randomInt(0, 30 * 24 * 60 * 60 * 1000)),
        status: commentStatuses[Math.floor(Math.random() * commentStatuses.length)]
      };
      post.comments.push(comment);
    }
  }

  postsData.push(post);
}

db.posts.insertMany(postsData);
print('✓ Posts creati: ' + postsData.length);

// ==================== AGGIORNAMENTO POST COUNTS ====================

print('\n🔄 Aggiornamento post counts...');

// Aggiorna postCount nelle categorie
categoriesData.forEach(category => {
  const count = db.posts.countDocuments({
    'category._id': category._id,
    status: 'published'
  });
  db.categories.updateOne(
    { _id: category._id },
    { $set: { postCount: count } }
  );
});

// Aggiorna postCount nei tags
tagsData.forEach(tag => {
  const count = db.posts.countDocuments({
    tags: tag.name,
    status: 'published'
  });
  db.tags.updateOne(
    { _id: tag._id },
    { $set: { postCount: count } }
  );
});

print('✓ Post counts aggiornati');

// ==================== STATISTICHE FINALI ====================

print('\n========================================');
print('DATA POPULATION COMPLETATA');
print('========================================\n');

print('DATABASE: ' + DB_NAME);
print('\nDOCUMENTI INSERITI:');
print('- Users: ' + db.users.countDocuments());
print('- Posts: ' + db.posts.countDocuments());
print('- Categories: ' + db.categories.countDocuments());
print('- Tags: ' + db.tags.countDocuments());

print('\nBREAKDOWN POSTS:');
print('- Published: ' + db.posts.countDocuments({ status: 'published' }));
print('- Draft: ' + db.posts.countDocuments({ status: 'draft' }));
print('- Archived: ' + db.posts.countDocuments({ status: 'archived' }));
print('- Featured: ' + db.posts.countDocuments({ featured: true }));

print('\nCOMMENTI TOTALI:');
const totalComments = db.posts.aggregate([
  { $match: { status: 'published' } },
  { $project: { count: { $size: '$comments' } } },
  { $group: { _id: null, total: { $sum: '$count' } } }
]).toArray();
print('- Total: ' + (totalComments[0]?.total || 0));

print('\nVIEWS TOTALI:');
const totalViews = db.posts.aggregate([
  { $group: { _id: null, total: { $sum: '$views' } } }
]).toArray();
print('- Total: ' + (totalViews[0]?.total || 0));

print('\n✓ Database popolato con successo!');
print('\nProssimo passo: Eseguire queries.js per vedere esempi di query.\n');

// ==================== FUNCTIONS HELPER ====================

/**
 * Mostra statistiche dettagliate del database
 */
function showStats() {
  print('\n=== DATABASE STATISTICS ===\n');

  print('USERS:');
  print('  Total: ' + db.users.countDocuments());
  print('  Authors: ' + db.users.countDocuments({ role: 'author' }));
  print('  Editors: ' + db.users.countDocuments({ role: 'editor' }));
  print('  Admins: ' + db.users.countDocuments({ role: 'admin' }));

  print('\nPOSTS:');
  print('  Total: ' + db.posts.countDocuments());
  print('  Published: ' + db.posts.countDocuments({ status: 'published' }));
  print('  Draft: ' + db.posts.countDocuments({ status: 'draft' }));
  print('  Archived: ' + db.posts.countDocuments({ status: 'archived' }));
  print('  Featured: ' + db.posts.countDocuments({ featured: true }));

  print('\nCATEGORIES:');
  print('  Total: ' + db.categories.countDocuments());
  print('  Root: ' + db.categories.countDocuments({ parentCategory: null }));
  print('  Subcategories: ' + db.categories.countDocuments({ parentCategory: { $exists: true } }));

  print('\nTAGS:');
  print('  Total: ' + db.tags.countDocuments());
  print('  Most used: ' + db.tags.findOne({ $sort: { postCount: -1 } })?.name);
}

/**
 * Reset del database (elimina tutti i dati)
 */
function resetDatabase() {
  print('\n⚠️  Eliminazione di tutti i dati...\n');
  db.users.deleteMany({});
  db.posts.deleteMany({});
  db.categories.deleteMany({});
  db.tags.deleteMany({});
  print('✓ Database resettato. Esegui di nuovo sample_data.js per ripopolare.\n');
}
