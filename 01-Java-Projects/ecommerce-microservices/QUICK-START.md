# Guida Rapida - Quick Start Guide

## Avvio Rapido (Windows)

Doppio click su `start-all.bat` e attendi 30 secondi per il caricamento.

## Avvio Rapido (Linux/Mac)

```bash
chmod +x start-all.sh
./start-all.sh
```

## Avvio Manuale

Apri 3 terminali:

**Terminale 1:**
```bash
cd user-service
mvn spring-boot:run
```

**Terminale 2:**
```bash
cd product-service
mvn spring-boot:run
```

**Terminale 3:**
```bash
cd order-service
mvn spring-boot:run
```

## Test Rapido

Apri un nuovo terminale e usa gli script di test:

**Windows:**
```bash
test-api.bat
```

**Linux/Mac:**
```bash
chmod +x test-api.sh
./test-api.sh
```

## Verifica Funzionamento

Tutti i servizi dovrebbero rispondere:

```bash
curl http://localhost:8081/api/users
curl http://localhost:8082/api/products
curl http://localhost:8083/api/orders
```

## H2 Console

Accedi alle console H2 per visualizzare i dati:

- User:    http://localhost:8081/h2-console
- Product: http://localhost:8082/h2-console
- Order:   http://localhost:8083/h2-console

**Credenziali:**
- JDBC URL: `jdbc:h2:mem:<dbname>`
- Username: `sa`
- Password: (vuoto)

## Esempio di Flusso Completo

### 1. Registra un utente

```bash
curl -X POST http://localhost:8081/api/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@email.com",
    "password": "password123",
    "firstName": "Test",
    "lastName": "User",
    "address": "Test Address"
  }'
```

Salva l'ID restituito (es. `1`).

### 2. Crea un prodotto

```bash
curl -X POST http://localhost:8082/api/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Product",
    "description": "A test product",
    "price": 29.99,
    "stockQuantity": 100,
    "sku": "TEST-001",
    "category": "Test"
  }'
```

Salva l'ID restituito (es. `1`).

### 3. Crea un ordine

```bash
curl -X POST http://localhost:8083/api/orders \
  -H "Content-Type: application/json" \
  -d '{
    "userId": 1,
    "shippingAddress": "My Address",
    "items": [
      {
        "productId": 1,
        "quantity": 2
      }
    ]
  }'
```

### 4. Verifica lo stock

```bash
curl http://localhost:8082/api/products/1
```

Lo stock dovrebbe essere diminuito di 2 unità.

### 5. Cancella l'ordine

```bash
curl -X POST http://localhost:8083/api/orders/1/cancel
```

### 6. Verifica lo stock ripristinato

```bash
curl http://localhost:8082/api/products/1
```

Lo stock dovrebbe essere tornato al valore originale.

## Risoluzione Problemi

### Porta già in uso

Cerca il processo che usa la porta:

```bash
# Windows
netstat -ano | findstr :8081

# Linux/Mac
lsof -i :8081
```

Uccidi il processo o cambia porta in `application.properties`.

### Servizi non si avviano

- Verifica Java 17+: `java -version`
- Verifica Maven 3.6+: `mvn -version`
- Assicurati di avviare prima User e Product service, poi Order service

### Ordini falliscono

- Verifica che l'utente esista
- Verifica che i prodotti esistano
- Verifica che lo stock sia sufficiente

## Next Steps

Leggi il README.md principale per documentazione completa.
