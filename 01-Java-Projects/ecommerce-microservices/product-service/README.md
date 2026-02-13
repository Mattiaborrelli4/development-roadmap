# Product Service

Microservizio per la gestione del catalogo prodotti.

## Porta

8082

## Database

H2 in-memory: `jdbc:h2:mem:productdb`

## API Endpoints

### Crea Prodotto

```http
POST /api/products
Content-Type: application/json

{
  "name": "Laptop HP Pavilion",
  "description": "Laptop con 16GB RAM, 512GB SSD",
  "price": 899.99,
  "stockQuantity": 50,
  "sku": "LAPT-HP-001",
  "category": "Elettronica",
  "imageUrl": "https://example.com/laptop.jpg"
}
```

### Lista Tutti i Prodotti

```http
GET /api/products
```

### Lista Prodotti Attivi

```http
GET /api/products/active
```

### Ottieni Prodotto per ID

```http
GET /api/products/{id}
```

### Ottieni Prodotto per SKU

```http
GET /api/products/sku/{sku}
```

### Filtra per Categoria

```http
GET /api/products/category/{category}
```

### Aggiorna Prodotto

```http
PUT /api/products/{id}
Content-Type: application/json

{
  "name": "Updated Name",
  "description": "Updated description",
  "price": 999.99,
  "stockQuantity": 45,
  "category": "Elettronica"
}
```

### Aggiorna Stock

```http
PATCH /api/products/{id}/stock
Content-Type: application/json

{
  "quantity": -5  // Negative to reduce, positive to increase
}
```

### Controlla Disponibilità

```http
GET /api/products/{id}/availability?quantity=2
```

Ritorna `true` se il prodotto è disponibile nella quantità richiesta.

### Riserva Stock (per ordini)

```http
POST /api/products/{id}/reserve
Content-Type: application/json

{
  "quantity": 2
}
```

Riduce lo stock della quantità specificata.

### Elimina Prodotto

```http
DELETE /api/products/{id}
```

## Avvio

```bash
mvn spring-boot:run
```

## H2 Console

http://localhost:8082/h2-console

JDBC URL: `jdbc:h2:mem:productdb`
Username: `sa`
Password: (vuota)
