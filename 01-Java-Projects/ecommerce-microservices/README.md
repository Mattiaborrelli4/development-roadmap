# E-Commerce Microservices Backend

Architettura a microservizi per un backend e-commerce con Spring Boot 3.x.

## Architettura

Il progetto consiste in tre microservizi indipendenti che comunicano tra loro tramite REST API:

```
+------------------+       +------------------+       +------------------+
|   User Service   |       | Product Service  |       |   Order Service  |
|     Port: 8081   |<----->|     Port: 8082    |<----->|     Port: 8083   |
+------------------+       +------------------+       +------------------+
       |                            |                            |
       v                            v                            v
   H2 Database                 H2 Database                 H2 Database
```

## Servizi

### 1. User Service (Porta 8081)

Gestione completa degli utenti e autenticazione.

**Funzionalità:**
- Registrazione nuovi utenti
- Login e validazione credenziali
- CRUD profilo utente
- Validazione utenti per altri servizi

**API Endpoints:**

```
GET    /api/users                    - Lista tutti gli utenti
GET    /api/users/{id}               - Ottieni utente per ID
GET    /api/users/username/{username} - Ottieni utente per username
POST   /api/users/register           - Registra nuovo utente
POST   /api/users/login              - Login utente
PUT    /api/users/{id}               - Aggiorna profilo utente
DELETE /api/users/{id}               - Elimina utente
GET    /api/users/validate/{id}      - Valida esistenza utente
```

**Esempio Registrazione Utente:**

```bash
curl -X POST http://localhost:8081/api/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "mario.rossi",
    "email": "mario.rossi@email.com",
    "password": "password123",
    "firstName": "Mario",
    "lastName": "Rossi",
    "phoneNumber": "+39 333 1234567",
    "address": "Via Roma 1, Milano"
  }'
```

**Esempio Login:**

```bash
curl -X POST http://localhost:8081/api/users/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "mario.rossi",
    "password": "password123"
  }'
```

### 2. Product Service (Porta 8082)

Gestione del catalogo prodotti e inventario.

**Funzionalità:**
- CRUD prodotti
- Gestione categorie
- Controllo disponibilità
- Aggiornamento stock
- Attivazione/disattivazione prodotti

**API Endpoints:**

```
GET    /api/products                      - Lista tutti i prodotti
GET    /api/products/active               - Lista prodotti attivi
GET    /api/products/{id}                 - Ottieni prodotto per ID
GET    /api/products/sku/{sku}            - Ottieni prodotto per SKU
GET    /api/products/category/{category}  - Filtra per categoria
POST   /api/products                      - Crea nuovo prodotto
PUT    /api/products/{id}                 - Aggiorna prodotto
PATCH  /api/products/{id}/stock           - Aggiorna stock
DELETE /api/products/{id}                 - Elimina prodotto
GET    /api/products/{id}/availability    - Controlla disponibilità
POST   /api/products/{id}/reserve         - Riserva stock (per ordini)
```

**Esempio Creazione Prodotto:**

```bash
curl -X POST http://localhost:8082/api/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop HP Pavilion",
    "description": "Laptop con 16GB RAM, 512GB SSD",
    "price": 899.99,
    "stockQuantity": 50,
    "sku": "LAPT-HP-001",
    "category": "Elettronica",
    "imageUrl": "https://example.com/laptop.jpg"
  }'
```

**Esempio Controllo Disponibilità:**

```bash
curl http://localhost:8082/api/products/1/availability?quantity=2
```

### 3. Order Service (Porta 8083)

Gestione ordini con comunicazione sincrona con gli altri servizi.

**Funzionalità:**
- Creazione ordini
- Validazione multi-servizio
- Gestione stato ordine
- Storico ordini utente
- Cancellazione con rilascio stock

**Comunicazione Inter-Service:**
- Chiama User Service per validare l'utente
- Chiama Product Service per verificare disponibilità
- Chiama Product Service per riservare stock
- Usa WebClient per chiamate REST sincrone

**API Endpoints:**

```
GET    /api/orders                   - Lista tutti gli ordini
GET    /api/orders/{id}              - Ottieni ordine per ID
GET    /api/orders/number/{number}   - Ottieni ordine per numero
GET    /api/orders/user/{userId}    - Lista ordini utente
POST   /api/orders                   - Crea nuovo ordine
PATCH  /api/orders/{id}/status       - Aggiorna stato ordine
POST   /api/orders/{id}/cancel      - Cancella ordine
```

**Esempio Creazione Ordine:**

```bash
curl -X POST http://localhost:8083/api/orders \
  -H "Content-Type: application/json" \
  -d '{
    "userId": 1,
    "shippingAddress": "Via Roma 1, Milano",
    "items": [
      {
        "productId": 1,
        "quantity": 2
      },
      {
        "productId": 2,
        "quantity": 1
      }
    ]
  }'
```

**Stati Ordine:**
- `PENDING` - In attesa di conferma
- `CONFIRMED` - Confermato
- `SHIPPED` - Spedito
- `DELIVERED` - Consegnato
- `CANCELLED` - Cancellato

## Tecnologic Utilizzate

### Core Framework
- **Spring Boot 3.2.0** - Framework principale
- **Spring Data JPA** - Persistenza dati
- **Spring Web** - REST API
- **Spring WebFlux** - WebClient per chiamate reattive

### Database
- **H2 Database** - Database in-memory per ogni servizio
- **Hibernate** - ORM

### Librerie
- **Lombok** - Riduzione boilerplate code
- **Jakarta Validation** - Validazione input
- **Jackson** - Serializzazione JSON

### Build Tool
- **Maven** - Gestione dipendenze e build

## Pre-Requisiti

- Java 17 o superiore
- Maven 3.6+
- (Opzionale) Postman o curl per testing API

## Setup e Avvio

### 1. Avvio dei Servizi

Apri 3 terminali separati e avvia i servizi:

**Terminale 1 - User Service:**
```bash
cd user-service
mvn spring-boot:run
```

**Terminale 2 - Product Service:**
```bash
cd product-service
mvn spring-boot:run
```

**Terminale 3 - Order Service:**
```bash
cd order-service
mvn spring-boot:run
```

### 2. Verifica Avvio

Ogni servizio mostrerà:
```
===========================================
User Service avviato sulla porta 8081
H2 Console: http://localhost:8081/h2-console
===========================================
```

### 3. Accedi alla H2 Console

Ogni servizio espone una console H2:
- User Service: http://localhost:8081/h2-console
- Product Service: http://localhost:8082/h2-console
- Order Service: http://localhost:8083/h2-console

**JDBC URL:**
- User: `jdbc:h2:mem:userdb`
- Product: `jdbc:h2:mem:productdb`
- Order: `jdbc:h2:mem:orderdb`

**Username:** `sa`
**Password:** (lascia vuoto)

## Scenario di Test Completo

### Step 1: Crea Utenti

```bash
# Utente 1
curl -X POST http://localhost:8081/api/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "mario.rossi",
    "email": "mario@email.com",
    "password": "pass123",
    "firstName": "Mario",
    "lastName": "Rossi",
    "phoneNumber": "3331234567",
    "address": "Via Roma 1, Milano"
  }'

# Utente 2
curl -X POST http://localhost:8081/api/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "luigi.verdi",
    "email": "luigi@email.com",
    "password": "pass456",
    "firstName": "Luigi",
    "lastName": "Verdi",
    "phoneNumber": "3337654321",
    "address": "Via Milano 1, Roma"
  }'
```

### Step 2: Crea Prodotti

```bash
# Prodotto 1
curl -X POST http://localhost:8082/api/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop HP Pavilion",
    "description": "Laptop con 16GB RAM, 512GB SSD",
    "price": 899.99,
    "stockQuantity": 50,
    "sku": "LAPT-HP-001",
    "category": "Elettronica",
    "imageUrl": "https://example.com/laptop.jpg"
  }'

# Prodotto 2
curl -X POST http://localhost:8082/api/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Mouse Wireless",
    "description": "Mouse wireless ergonomico",
    "price": 29.99,
    "stockQuantity": 100,
    "sku": "MOUS-WL-002",
    "category": "Accessori",
    "imageUrl": "https://example.com/mouse.jpg"
  }'

# Prodotto 3
curl -X POST http://localhost:8082/api/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Tastiera Meccanica",
    "description": "Tastiera meccanica RGB",
    "price": 89.99,
    "stockQuantity": 30,
    "sku": "TAST-MEC-003",
    "category": "Accessori",
    "imageUrl": "https://example.com/keyboard.jpg"
  }'
```

### Step 3: Crea Ordini

```bash
# Ordine 1 - Mario Rossi
curl -X POST http://localhost:8083/api/orders \
  -H "Content-Type: application/json" \
  -d '{
    "userId": 1,
    "shippingAddress": "Via Roma 1, Milano",
    "items": [
      {
        "productId": 1,
        "quantity": 1
      },
      {
        "productId": 2,
        "quantity": 2
      }
    ]
  }'

# Ordine 2 - Luigi Verdi
curl -X POST http://localhost:8083/api/orders \
  -H "Content-Type: application/json" \
  -d '{
    "userId": 2,
    "shippingAddress": "Via Milano 1, Roma",
    "items": [
      {
        "productId": 3,
        "quantity": 1
      }
    ]
  }'
```

### Step 4: Verifica Ordini

```bash
# Tutti gli ordini
curl http://localhost:8083/api/orders

# Ordini utente 1
curl http://localhost:8083/api/orders/user/1

# Ordine per numero
curl http://localhost:8083/api/orders/number/ORD-XXXXXXX
```

### Step 5: Aggiorna Stato Ordine

```bash
curl -X PATCH http://localhost:8083/api/orders/1/status \
  -H "Content-Type: application/json" \
  -d '{
    "status": "CONFIRMED"
  }'
```

### Step 6: Cancella Ordine

```bash
curl -X POST http://localhost:8083/api/orders/1/cancel
```

### Step 7: Verifica Stock Aggiornato

```bash
# Dopo aver creato l'ordine, lo stock sarà diminuito
curl http://localhost:8082/api/products/1

# Dopo aver cancellato l'ordine, lo stock sarà ripristinato
curl http://localhost:8082/api/products/1
```

## Struttura Progetto

```
ecommerce-microservices/
├── user-service/
│   ├── pom.xml
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
├── product-service/
│   ├── pom.xml
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
└── order-service/
    ├── pom.xml
    └── src/main/
        ├── java/com/ecommerce/order/
        │   ├── OrderServiceApplication.java
        │   ├── controller/OrderController.java
        │   ├── service/
        │   │   ├── OrderService.java
        │   │   ├── UserServiceClient.java
        │   │   └── ProductServiceClient.java
        │   ├── repository/OrderRepository.java
        │   ├── model/
        │   │   ├── Order.java
        │   │   └── OrderItem.java
        │   ├── dto/OrderDTO.java
        │   └── config/WebClientConfig.java
        └── resources/
            └── application.properties
```

## Dettagli Architetturali

### Comunicazione Inter-Service

L'Order Service utilizza **WebClient** per comunicare con gli altri servizi in modo sincrono:

**UserServiceClient:**
- `validateUser(userId)` - Verifica esistenza utente
- `getUsername(userId)` - Recupera username

**ProductServiceClient:**
- `checkAvailability(productId, quantity)` - Verifica disponibilità
- `getProductName(productId)` - Recupera nome prodotto
- `getProductPrice(productId)` - Recupera prezzo
- `reserveStock(productId, quantity)` - Riserva stock
- `releaseStock(productId, quantity)` - Rilascia stock

### Transazioni

Il servizio ordini gestisce:
1. Validazione utente (tramite User Service)
2. Verifica disponibilità prodotti (tramite Product Service)
3. Creazione ordine nel database locale
4. Riserva stock (tramite Product Service)

In caso di errore, lo stock viene rilasciato.

### Database Indipendenti

Ogni servizio ha il proprio database H2:
- **Isolamento completo** - ogni servizio gestisce i propri dati
- **Indipendenza** - può essere migrato su database diversi
- **No shared database** - principio fondamentale dei microservizi

## Possibili Miglioramenti

### Architetturali
- [ ] Service Registry (Eureka/Consul)
- [ ] API Gateway (Spring Cloud Gateway)
- [ ] Config Server (Spring Cloud Config)
- [ ] Distributed Tracing (Zipkin/Jaeger)
- [ ] Circuit Breaker (Resilience4j)

### Security
- [ ] JWT per autenticazione
- [ ] OAuth2 / OpenID Connect
- [ ] HTTPS/SSL
- [ ] Role-Based Access Control

### Funzionalità
- [ ] Ricerca avanzata prodotti
- [ ] Carrello della spesa
- [ ] Gestione pagamenti
- [ ] Notifiche email
- [ ] Sistema di review

### DevOps
- [ ] Containerizzazione Docker
- [ ] Orchestrazione Kubernetes
- [ ] CI/CD Pipeline
- [ ] Monitoring & Alerting (Prometheus/Grafana)
- [ ] Centralized Logging (ELK Stack)

### Database
- [ ] Migrazione a PostgreSQL/MySQL
- [ ] Event Sourcing per ordini
- [ ] Caching distribuito (Redis)

## Troubleshooting

### Porta già in uso

Se ricevi un errore "Port 8081 is already in use":

1. Trova il processo:
   ```bash
   netstat -ano | findstr :8081
   ```

2. Termina il processo o cambia porta in `application.properties`

### Servizio non raggiungibile

Se l'Order Service non raggiunge gli altri servizi:

1. Verifica che tutti i servizi siano avviati
2. Controlla le URL in `application.properties`
3. Verifica firewall

### Errori di connessione H2

Se la console H2 non funziona:
- JDBC URL deve essere esattamente `jdbc:h2:mem:userdb` (non `mem:userdb` con slash extra)

## Note di Produzione

Questo progetto è un **proof-of-concept**. Per produzione considera:

1. **Password Hashing**: Utilizza BCrypt per le password
2. **Validazione Input**: Aggiungi validazione più robusta
3. **Error Handling**: Implementa gestori errori globali
4. **Logging**: Structured logging con correlation IDs
5. **Testing**: Unit e integration tests
6. **Documentation**: OpenAPI/Swagger documentation
7. **Health Checks**: Spring Boot Actuator health endpoints
8. **Metrics**: Micrometer per monitoring

## Autori

Progetto dimostrativo per portfolio personale.

## Licenza

MIT License - Sentiti libero di utilizzare questo progetto per scopi educativi.
