// Setup Script - Real-time Analytics MongoDB
// Questo script crea le collezioni, gli indici e la configurazione iniziale

const { MongoClient, ObjectId } = require('mongodb');

// Configurazione connessione
const MONGO_URI = process.env.MONGO_URI || 'mongodb://localhost:27017';
const DB_NAME = 'realtime_analytics';

async function setupDatabase() {
  const client = new MongoClient(MONGO_URI);

  try {
    console.log('🔗 Connessione a MongoDB...');
    await client.connect();
    console.log('✅ Connesso con successo');

    const db = client.db(DB_NAME);

    // ============================================================
    // CREAZIONE DELLE COLLECTIONS
    // ============================================================

    console.log('\n📦 Creazione delle collections...');

    // Collection: events
    const eventsCollection = await db.createCollection('events', {
      // Opzioni per ottimizzare le time-series queries
      // capped: false, // Non capped collection per dati time-series
    });
    console.log('✅ Collection "events" creata');

    // Collection: sessions
    const sessionsCollection = await db.createCollection('sessions');
    console.log('✅ Collection "sessions" creata');

    // Collection: daily_stats
    const dailyStatsCollection = await db.createCollection('daily_stats');
    console.log('✅ Collection "daily_stats" creata');

    // ============================================================
    // INDICI PER LA COLLECTION "events"
    // ============================================================

    console.log('\n📇 Creazione indici per "events"...');

    // 1. Indice composto su timestamp e eventType (per time-series queries)
    await eventsCollection.createIndex(
      { timestamp: -1, eventType: 1 },
      { name: 'idx_timestamp_eventType' }
    );
    console.log('  ✅ Indice timestamp_eventType creato');

    // 2. Indice su sessionId (per recuperare eventi di una sessione)
    await eventsCollection.createIndex(
      { sessionId: 1 },
      { name: 'idx_sessionId' }
    );
    console.log('  ✅ Indice sessionId creato');

    // 3. Indice su userId (per analisi comportamento utenti)
    await eventsCollection.createIndex(
      { userId: 1, timestamp: -1 },
      { name: 'idx_userId_timestamp', sparse: true } // sparse perché userId può essere null
    );
    console.log('  ✅ Indice userId_timestamp creato');

    // 4. Indice TTL per eliminare automaticamente i vecchi eventi (90 giorni)
    await eventsCollection.createIndex(
      { timestamp: 1 },
      {
        name: 'idx_ttl_events',
        expireAfterSeconds: 90 * 24 * 60 * 60 // 90 giorni in secondi
      }
    );
    console.log('  ✅ Indice TTL (90 giorni) creato');

    // 5. Indice su environment (per separare production e staging)
    await eventsCollection.createIndex(
      { environment: 1, timestamp: -1 },
      { name: 'idx_environment_timestamp' }
    );
    console.log('  ✅ Indice environment_timestamp creato');

    // 6. Indice su platform (per analisi per piattaforma)
    await eventsCollection.createIndex(
      { platform: 1, timestamp: -1 },
      { name: 'idx_platform_timestamp' }
    );
    console.log('  ✅ Indice platform_timestamp creato');

    // 7. Indice su properties.url (per analisi delle pagine)
    await eventsCollection.createIndex(
      { 'properties.url': 1 },
      { name: 'idx_properties_url' }
    );
    console.log('  ✅ Indice properties.url creato');

    // 8. Indice su properties.ip (per analisi geografica)
    await eventsCollection.createIndex(
      { 'properties.ip': 1 },
      { name: 'idx_properties_ip' }
    );
    console.log('  ✅ Indice properties.ip creato');

    // 9. Indice su properties.device (per analisi device)
    await eventsCollection.createIndex(
      { 'properties.device': 1 },
      { name: 'idx_properties_device' }
    );
    console.log('  ✅ Indice properties.device creato');

    // 10. Indice composto per query dashboard real-time
    await eventsCollection.createIndex(
      { environment: 1, timestamp: -1, eventType: 1 },
      { name: 'idx_dashboard_realtime' }
    );
    console.log('  ✅ Indice dashboard_realtime creato');

    // ============================================================
    // INDICI PER LA COLLECTION "sessions"
    // ============================================================

    console.log('\n📇 Creazione indici per "sessions"...');

    // 1. Indice unico su sessionId
    await sessionsCollection.createIndex(
      { sessionId: 1 },
      { name: 'idx_sessionId_unique', unique: true }
    );
    console.log('  ✅ Indice sessionId (unique) creato');

    // 2. Indice su userId
    await sessionsCollection.createIndex(
      { userId: 1, startTime: -1 },
      { name: 'idx_userId_startTime', sparse: true }
    );
    console.log('  ✅ Indice userId_startTime creato');

    // 3. Indice su startTime (per analisi temporale)
    await sessionsCollection.createIndex(
      { startTime: -1 }
    );
    console.log('  ✅ Indice startTime creato');

    // 4. Indice su duration (per analisi durata)
    await sessionsCollection.createIndex(
      { duration: -1 }
    );
    console.log('  ✅ Indice duration creato');

    // 5. Indice geografico
    await sessionsCollection.createIndex(
      { 'location.country': 1, 'location.city': 1 },
      { name: 'idx_location' }
    );
    console.log('  ✅ Indice location creato');

    // 6. Indice su device
    await sessionsCollection.createIndex(
      { device: 1 }
    );
    console.log('  ✅ Indice device creato');

    // 7. Indice su browser
    await sessionsCollection.createIndex(
      { browser: 1 }
    );
    console.log('  ✅ Indice browser creato');

    // ============================================================
    // INDICI PER LA COLLECTION "daily_stats"
    // ============================================================

    console.log('\n📇 Creazione indici per "daily_stats"...');

    // 1. Indice unico su date e eventType
    await dailyStatsCollection.createIndex(
      { date: 1, eventType: 1 },
      { name: 'idx_date_eventType_unique', unique: true }
    );
    console.log('  ✅ Indice date_eventType (unique) creato');

    // 2. Indice su date
    await dailyStatsCollection.createIndex(
      { date: -1 }
    );
    console.log('  ✅ Indice date creato');

    // 3. Indice su eventType
    await dailyStatsCollection.createIndex(
      { eventType: 1, date: -1 }
    );
    console.log('  ✅ Indice eventType_date creato');

    // 4. Indice su count
    await dailyStatsCollection.createIndex(
      { count: -1 }
    );
    console.log('  ✅ Indice count creato');

    // ============================================================
    // INSERIMENTO DATI INIZIALI
    // ============================================================

    console.log('\n📊 Inserimento dati di esempio iniziali...');

    // Inseriamo alcune statistiche giornaliere vuote per gli ultimi 7 giorni
    const eventTypes = ['pageview', 'click', 'purchase', 'signup', 'logout', 'error'];
    const today = new Date();

    for (let i = 6; i >= 0; i--) {
      const date = new Date(today);
      date.setDate(date.getDate() - i);
      date.setHours(0, 0, 0, 0);

      for (const eventType of eventTypes) {
        await dailyStatsCollection.updateOne(
          { date, eventType },
          {
            $setOnInsert: {
              date,
              eventType,
              count: 0,
              uniqueUsers: 0,
              uniqueSessions: 0
            }
          },
          { upsert: true }
        );
      }
    }
    console.log('✅ Statistiche giornaliere iniziali inserite');

    // ============================================================
    // VERIFICA DEGLI INDICI
    // ============================================================

    console.log('\n📋 Verifica degli indici creati:\n');

    console.log('Collection "events":');
    const eventsIndexes = await eventsCollection.indexes();
    eventsIndexes.forEach(index => {
      console.log(`  - ${index.name}: ${JSON.stringify(index.key)}`);
    });

    console.log('\nCollection "sessions":');
    const sessionsIndexes = await sessionsCollection.indexes();
    sessionsIndexes.forEach(index => {
      console.log(`  - ${index.name}: ${JSON.stringify(index.key)}`);
    });

    console.log('\nCollection "daily_stats":');
    const dailyStatsIndexes = await dailyStatsCollection.indexes();
    dailyStatsIndexes.forEach(index => {
      console.log(`  - ${index.name}: ${JSON.stringify(index.key)}`);
    });

    // ============================================================
    // STATISTICHE FINALI
    // ============================================================

    console.log('\n📊 Statistiche del database:');
    const eventsCount = await eventsCollection.estimatedDocumentCount();
    const sessionsCount = await sessionsCollection.estimatedDocumentCount();
    const dailyStatsCount = await dailyStatsCollection.estimatedDocumentCount();

    console.log(`  - events: ${eventsCount} documenti`);
    console.log(`  - sessions: ${sessionsCount} documenti`);
    console.log(`  - daily_stats: ${dailyStatsCount} documenti`);

    console.log('\n🎉 Setup completato con successo!');
    console.log('\n💡 Prossimi passi:');
    console.log('   1. Esegui node sample_data.js per generare dati di esempio');
    console.log('   2. Esegui node queries.js per testare le query di aggregazione');
    console.log('   3. Esegui node aggregation_examples.js per vedere esempi di pipeline');

  } catch (error) {
    console.error('❌ Errore durante il setup:', error);
    process.exit(1);
  } finally {
    await client.close();
    console.log('\n🔌 Connessione chiusa');
  }
}

// Esecuzione dello script
if (require.main === module) {
  setupDatabase();
}

module.exports = { setupDatabase };
