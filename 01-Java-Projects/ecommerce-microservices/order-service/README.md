# Order Service

Microservizio per la gestione degli ordini con comunicazione inter-servizio.

## Porta

8083

## Database

H2 in-memory: `jdbc:h2:mem:orderdb`

## Comunicazione Inter-Service

Il servizio ordini comunica con:

- **User Service** (port 8081): validazione utenti
- **Product Service** (port 8082): verifica disponibilità e riserva stock

## API Endpoints

### Crea Ordine

```http
POST /api/orders
Content-Type: application/json

{
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
}
```

Il servizio:
1. Valida l'utente con User Service
2. Verifica disponibilità prodotti con Product Service
3. Crea l'ordine
4. Riserva lo stock con Product Service

### Lista Tutti gli Ordini

```http
GET /api/orders
```

### Ottieni Ordine per ID

```http
GET /api/orders/{id}
```

### Ottieni Ordine per Numero

```http
GET /api/orders/number/{orderNumber}
```

### Lista Ordini Utente

```http
GET /api/orders/user/{userId}
```

### Aggiorna Stato Ordine

```http
PATCH /api/orders/{id}/status
Content-Type: application/json

{
  "status": "CONFIRMED"
}
```

Stati disponibili: `PENDING`, `CONFIRMED`, `SHIPPED`, `DELIVERED`, `CANCELLED`

### Cancella Ordine

```http
POST /api/orders/{id}/cancel
```

Il servizio:
1. Verifica che l'ordine non sia già spedito
2. Rilascia lo stock con Product Service
3. Segna l'ordine come CANCELLED

## Flusso Ordine

```
1. Client POST /api/orders
       ↓
2. OrderService
   ↓
3. UserServiceClient.validateUser()
   → User Service: GET /api/users/validate/{id}
   ←
   ↓
4. ProductServiceClient.checkAvailability() (per ogni item)
   → Product Service: GET /api/products/{id}/availability
   ←
   ↓
5. Salva Order nel database
   ↓
6. ProductServiceClient.reserveStock() (per ogni item)
   → Product Service: POST /api/products/{id}/reserve
   ←
   ↓
7. Ritorna OrderDTO al client
```

## Avvio

Assicurati che User Service e Product Service siano già avviati, poi:

```bash
mvn spring-boot:run
```

## H2 Console

http://localhost:8083/h2-console

JDBC URL: `jdbc:h2:mem:orderdb`
Username: `sa`
Password: (vuota)

## Configurazione

In `application.properties`:

```properties
user.service.url=http://localhost:8081
product.service.url=http://localhost:8082
```

Modifica queste URL se i servizi girano su host/port diversi.
