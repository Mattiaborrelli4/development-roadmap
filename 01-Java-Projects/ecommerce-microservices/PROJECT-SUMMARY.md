# E-Commerce Microservices - Riepilogo Progetto

## Informazioni Generali

**Nome Progetto:** E-Commerce Backend Microservices
**Tecnologia:** Spring Boot 3.2.0 + Java 17
**Architettura:** Microservizi REST
**Database:** H2 In-Memory (per servizio)
**Totale Servizi:** 3
**Data Creazione:** Febbraio 2026

## Servizi Implementati

### 1. User Service (Porta 8081)
- **File Java:** 6
- **Endpoint:** 8
- **Funzionalità:** Gestione utenti, registrazione, login, profilo
- **Database:** `userdb`

### 2. Product Service (Porta 8082)
- **File Java:** 6
- **Endpoint:** 11
- **Funzionalità:** CRUD prodotti, inventario, categorie
- **Database:** `productdb`

### 3. Order Service (Porta 8083)
- **File Java:** 10
- **Endpoint:** 7
- **Funzionalità:** Gestione ordini, comunicazione inter-servizio
- **Database:** `orderdb`
- **Integrazioni:** User Service, Product Service

## Struttura Progetto

```
ecommerce-microservices/
├── user-service/          [Microservizio utenti]
│   ├── pom.xml
│   ├── README.md
│   └── src/main/
│       ├── java/com/ecommerce/user/
│       │   ├── UserServiceApplication.java
│       │   ├── controller/UserController.java
│       │   ├── service/UserService.java
│       │   ├── repository/UserRepository.java
│       │   ├── model/User.java
│       │   └── dto/UserDTO.java
│       └── resources/
│           └── application.properties
│
├── product-service/       [Microservizio prodotti]
│   ├── pom.xml
│   ├── README.md
│   └── src/main/
│       ├── java/com/ecommerce/product/
│       │   ├── ProductServiceApplication.java
│       │   ├── controller/ProductController.java
│       │   ├── service/ProductService.java
│       │   ├── repository/ProductRepository.java
│       │   ├── model/Product.java
│       │   └── dto/ProductDTO.java
│       └── resources/
│           └── application.properties
│
├── order-service/         [Microservizio ordini]
│   ├── pom.xml
│   ├── README.md
│   └── src/main/
│       ├── java/com/ecommerce/order/
│       │   ├── OrderServiceApplication.java
│       │   ├── controller/OrderController.java
│       │   ├── service/
│       │   │   ├── OrderService.java
│       │   │   ├── UserServiceClient.java
│       │   │   └── ProductServiceClient.java
│       │   ├── repository/OrderRepository.java
│       │   ├── model/
│       │   │   ├── Order.java
│       │   │   └── OrderItem.java
│       │   ├── dto/OrderDTO.java
│       │   └── config/WebClientConfig.java
│       └── resources/
│           └── application.properties
│
├── README.md             [Documentazione principale]
├── ARCHITECTURE.md       [Documentazione architettura]
├── QUICK-START.md       [Guida rapida]
├── .gitignore
├── start-all.bat        [Script avvio Windows]
├── start-all.sh        [Script avvio Linux/Mac]
├── test-api.bat        [Script test Windows]
└── test-api.sh         [Script test Linux/Mac]
```

## Totale File per Categoria

| Categoria | Quantità |
|-----------|----------|
| Servizi | 3 |
| File Java | 22 |
| File Properties | 3 |
| File POM | 3 |
| File README | 4 |
| Script | 4 |
| Totale File | 36+ |

## Endpoint API Totali

### User Service: 8 endpoint
```
GET    /api/users
GET    /api/users/{id}
GET    /api/users/username/{username}
POST   /api/users/register
POST   /api/users/login
PUT    /api/users/{id}
DELETE /api/users/{id}
GET    /api/users/validate/{id}
```

### Product Service: 11 endpoint
```
GET    /api/products
GET    /api/products/active
GET    /api/products/{id}
GET    /api/products/sku/{sku}
GET    /api/products/category/{category}
POST   /api/products
PUT    /api/products/{id}
PATCH  /api/products/{id}/stock
DELETE /api/products/{id}
GET    /api/products/{id}/availability
POST   /api/products/{id}/reserve
```

### Order Service: 7 endpoint
```
GET    /api/orders
GET    /api/orders/{id}
GET    /api/orders/number/{number}
GET    /api/orders/user/{userId}
POST   /api/orders
PATCH  /api/orders/{id}/status
POST   /api/orders/{id}/cancel
```

**TOTALE ENDPOINT:** 26

## Funzionalità Chiave

### Gestione Utenti
- Registrazione con validazione
- Login con credenziali
- Profilo completo (nome, email, telefono, indirizzo)
- Aggiornamento profilo
- Eliminazione account
- Validazione per altri servizi

### Gestione Prodotti
- Catalogo completo
- Categorie
- SKU univoci
- Controllo inventario
- Attivazione/disattivazione
- Aggiornamento stock
- Controllo disponibilità

### Gestione Ordini
- Creazione con validazione multi-servizio
- Calcolo automatico totale
- Gestione stato (Pending → Delivered)
- Cancellazione con rilascio stock
- Storico ordini per utente
- Numero ordine univoco

## Comunicazione Inter-Service

L'Order Service effettua chiamate REST sincrone usando WebClient:

**→ User Service:**
- Validazione esistenza utente
- Recupero username

**→ Product Service:**
- Verifica disponibilità
- Recupero dettagli prodotto
- Riserva stock
- Rilascio stock

## Come Avviare

### Opzione 1: Script Automatico
```bash
# Windows
start-all.bat

# Linux/Mac
./start-all.sh
```

### Opzione 2: Manuale
```bash
# Terminale 1
cd user-service && mvn spring-boot:run

# Terminale 2
cd product-service && mvn spring-boot:run

# Terminale 3
cd order-service && mvn spring-boot:run
```

## Come Testare

### Script Automatico
```bash
# Windows
test-api.bat

# Linux/Mac
./test-api.sh
```

### Manuale
Seguire gli esempi nel README.md

## Requisiti di Sistema

- **Java:** 17 o superiore
- **Maven:** 3.6+
- **RAM:** 2GB+ consigliati
- **Porte:** 8081, 8082, 8083 libere

## Stack Tecnologico

| Componente | Tecnologia |
|-----------|-----------|
| Framework | Spring Boot 3.2.0 |
| Linguaggio | Java 17 |
| Database | H2 (In-Memory) |
| ORM | Hibernate / JPA |
| REST | Spring Web |
| Async Client | Spring WebFlux / WebClient |
| Validation | Jakarta Validation |
| Code Generation | Lombok |
| Build Tool | Maven |

## Punti di Forza

✓ **Architettura Pulita** - Separazione chiara dei domini
✓ **Database Isolati** - Ogni servizio ha il proprio DB
✓ **REST Standard** - API RESTful ben progettate
✓ **Documentazione Completa** - README, Architettura, Quick Start
✓ **Facile Testing** - Script di test automatizzati
✓ **Comunicazione Sincrona** - WebClient per chiamate inter-servizio
✓ **H2 Console** - Debug facile tramite web UI
✓ **Codice Pulito** - Lombok riduce boilerplate

## Possibili Miglioramenti

### Breve Termine
- [ ] JWT per autenticazione
- [ ] Input Validation più robusta
- [ ] Global Exception Handler
- [ ] Unit Tests
- [ ] Integration Tests
- [ ] Actuator per health checks

### Medio Termino
- [ ] Docker containers
- [ ] Docker Compose per setup rapido
- [ ] API Gateway (Spring Cloud Gateway)
- [ ] Service Discovery (Eureka)
- [ ] Config Server (Spring Cloud Config)

### Lungo Termino
- [ ] Database reali (PostgreSQL/MySQL)
- [ ] Distributed Tracing (Zipkin)
- [ ] Circuit Breaker (Resilience4j)
- [ ] Kubernetes deployment
- [ ] CI/CD Pipeline
- [ ] Monitoring (Prometheus/Grafana)

## Note Importanti

### ⚠️ Non per Produzione
Questo è un progetto dimostrativo (POC). Per produzione:
- Implementare password hashing (BCrypt)
- Usare database persistenti
- Aggiungere HTTPS/TLS
- Implementare rate limiting
- Aggiungere logging strutturato
- Gestione errori più robusta

### 💡 Architettura Attuale
- Nessun service registry (comunicazione diretta)
- Nessun API gateway (accesso diretto ai servizi)
- Nessun circuit breaker (no fallback)
- Database in-memory (persita dati al restart)
- Nessuna distributed tracing

## Risorse

- **Documentazione Principale:** README.md
- **Architettura:** ARCHITECTURE.md
- **Guida Rapida:** QUICK-START.md
- **Documentazione Servizi:*/user-service/README.md, /product-service/README.md, /order-service/README.md

## Lingua

Tutta la documentazione è in **Italiano** come richiesto.

## Licenza

MIT License - Libero utilizzo per scopi educativi e portfolio personale.

---

**Creato per:** Portfolio Progetti Java
**Data:** Febbraio 2026
**Versione:** 1.0.0
