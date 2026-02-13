# Contributing to Web Vulnerability Scanner

Grazie per il tuo interesse nel contribuire a questo progetto educativo!

## 📋 Linee Guida per i Contributi

### Scopo del Progetto

Questo scanner è uno strumento **EDUCATIVO e DIFENSIVO**. Tutti i contributi devono:

- ✅ Essere orientati all'apprendimento
- ✅ Migliorare le capacità defensive
- ✅ Essere sicuri e non distruttivi
- ✅ Includere documentazione chiara

### 🤝 Come Contribuire

#### 1. Reporting Bug

Crea una issue su GitHub con:

- **Titolo:** Descrizione breve del problema
- **Ambiente:** OS, Python version
- **Passi:** Passaggi per riprodurre
- **Comportamento:** Cosa succede vs cosa dovresti aspettarti
- **Log:** Error logs se presenti

#### 2. Suggerire Features

Le nuove features devono:

- Essere rilevanti per la sicurezza web educativa
- Non includere payload distruttivi
- Avere documentazione chiara
- Essere facili da capire

#### 3. Pull Requests

**Process:**

1. Fork il repository
2. Crea un branch: `git checkout -b feature/nome-feature`
3. Commit i cambiamenti: `git commit -m 'Aggiunta feature X'`
4. Push: `git push origin feature/nome-feature`
5. Apri Pull Request

**Code Style:**

- Segui PEP 8
- Aggiungi docstrings
- Includi tests per nuove funzionalità
- Aggiorna la documentazione

### ⚠️ Cosa NON Aggiungere

Non contribuire:

- ❌ Payload distruttivi (DROP, DELETE, etc.)
- ❌ Exploit per attacchi reali
- ❌ Bypass di controlli di sicurezza
- ❌ Funzionalità malevole
- ❌ Codice senza documentazione

### 📝 Documentazione

Tutti i contributi devono includere:

- Docstrings Python
- Commenti nel codice
- Aggiornamento README se necessario
- Esempi di utilizzo

### 🧪 Testing

- Scrivi unit tests per nuove funzionalità
- Assicurati che tutti i test passino
- Testa su più ambienti se possibile

```bash
# Esegui tests
pytest tests/ -v

# Con coverage
pytest tests/ --cov=. --cov-report=html
```

### 🎨 Codice di Condotta

- Sii rispettoso
- Accetta feedback costruttivo
- Aiuta altri a imparare
- Mantieni un ambiente inclusivo

### 📧 Contatto

Per domande:
- Apri una issue su GitHub
- Contatta il maintainer
- Partecipa alle discussioni

---

Ricorda: Questo è un progetto educativo. I contributi dovrebbero aiutare le persone a imparare la sicurezza web in modo responsabile! 🎓🔒
