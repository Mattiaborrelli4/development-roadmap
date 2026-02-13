# Architettura E-Commerce Microservices

## Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                         Client                                   │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│                      API Gateway (Futuro)                        │
│                    (Non implementato in POC)                     │
└──────────────────────────────────────────────────────────────────┘
         │                    │                    │
         ▼                    ▼                    ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   User       │    │   Product    │    │   Order      │
│   Service    │    │   Service    │    │   Service    │
│  :8081      │    │  :8082       │    │  :8083       │
└──────────────┘    └──────────────┘    └──────────────┘
      │                    │                    │
      ▼                    ▼                    ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  H2: userdb │    │ H2:productdb │    │  H2:orderdb │
└──────────────┘    └──────────────┘    └──────────────┘
```

## Comunicazione Inter-Service

```
Order Service communicates with:
├─→ User Service: Validazione utente
│   └─→ GET /api/users/validate/{id}
│
└─→ Product Service: Gestione prodotti
    ├─→ GET /api/products/{id}/availability
    ├─→ GET /api/products/{id}
    ├─→ POST /api/products/{id}/reserve
    └─→ PATCH /api/products/{id}/stock
```

## Componenti Per Servizio

### User Service (Port 8081)

```
UserServiceApplication.java
├── controller/
│   └── UserController.java
│       ├── GET    /api/users
│       ├── GET    /api/users/{id}
│       ├── GET    /api/users/username/{username}
│       ├── POST   /api/users/register
│       ├── POST   /api/users/login
│       ├── PUT    /api/users/{id}
│       ├── DELETE /api/users/{id}
│       └── GET    /api/users/validate/{id}
│
├── service/
│   └── UserService.java
│       ├── getAllUsers()
│       ├── getUserById()
│       ├── getUserByUsername()
│       ├── registerUser()
│       ├── updateUser()
│       ├── deleteUser()
│       └── validateLogin()
│
├── repository/
│   └── UserRepository.java (JPA)
│
├── model/
│   └── User.java (@Entity)
│
└── dto/
    ├── UserDTO.java
    ├── UserLoginRequest.java
    └── UserRegistrationRequest.java
```

### Product Service (Port 8082)

```
ProductServiceApplication.java
├── controller/
│   └── ProductController.java
│       ├── GET    /api/products
│       ├── GET    /api/products/active
│       ├── GET    /api/products/{id}
│       ├── GET    /api/products/sku/{sku}
│       ├── GET    /api/products/category/{category}
│       ├── POST   /api/products
│       ├── PUT    /api/products/{id}
│       ├── PATCH  /api/products/{id}/stock
│       ├── DELETE /api/products/{id}
│       ├── GET    /api/products/{id}/availability
│       └── POST   /api/products/{id}/reserve
│
├── service/
│   └── ProductService.java
│       ├── getAllProducts()
│       ├── getActiveProducts()
│       ├── getProductById()
│       ├── getProductBySku()
│       ├── getProductsByCategory()
│       ├── createProduct()
│       ├── updateProduct()
│       ├── updateStock()
│       ├── deleteProduct()
│       └── checkAvailability()
│
├── repository/
│   └── ProductRepository.java (JPA)
│
├── model/
│   └── Product.java (@Entity)
│
└── dto/
    ├── ProductDTO.java
    ├── CreateProductRequest.java
    └── UpdateStockRequest.java
```

### Order Service (Port 8083)

```
OrderServiceApplication.java
├── controller/
│   └── OrderController.java
│       ├── GET    /api/orders
│       ├── GET    /api/orders/{id}
│       ├── GET    /api/orders/number/{number}
│       ├── GET    /api/orders/user/{userId}
│       ├── POST   /api/orders
│       ├── PATCH  /api/orders/{id}/status
│       └── POST  /api/orders/{id}/cancel
│
├── service/
│   ├── OrderService.java
│   │   ├── getAllOrders()
│   │   ├── getOrdersByUserId()
│   │   ├── getOrderByOrderNumber()
│   │   ├── createOrder()
│   │   ├── updateOrderStatus()
│   │   └── cancelOrder()
│   │
│   ├── UserServiceClient.java (WebClient)
│   │   ├── validateUser()
│   │   └── getUsername()
│   │
│   └── ProductServiceClient.java (WebClient)
│       ├── checkAvailability()
│       ├── getProductName()
│       ├── getProductPrice()
│       ├── reserveStock()
│       └── releaseStock()
│
├── repository/
│   └── OrderRepository.java (JPA)
│
├── model/
│   ├── Order.java (@Entity)
│   └── OrderItem.java (@Entity)
│
├── dto/
│   ├── OrderDTO.java
│   ├── OrderItemDTO.java
│   ├── CreateOrderRequest.java
│   ├── OrderItemRequest.java
│   └── UpdateOrderStatusRequest.java
│
└── config/
    └── WebClientConfig.java
```

## Data Models

### User
```java
User {
    Long id
    String username
    String email
    String password
    String firstName
    String lastName
    String phoneNumber
    String address
    LocalDateTime createdAt
    LocalDateTime updatedAt
}
```

### Product
```java
Product {
    Long id
    String name
    String description
    BigDecimal price
    Integer stockQuantity
    String sku (unique)
    String category
    String imageUrl
    Boolean active
    LocalDateTime createdAt
    LocalDateTime updatedAt
}
```

### Order
```java
Order {
    Long id
    Long userId
    String orderNumber (unique)
    BigDecimal totalAmount
    OrderStatus status (PENDING, CONFIRMED, SHIPPED, DELIVERED, CANCELLED)
    LocalDateTime orderDate
    String shippingAddress
    List<OrderItem> items
}

OrderItem {
    Long id
    Order order
    Long productId
    String productName
    Integer quantity
    BigDecimal unitPrice
    BigDecimal subtotal
}
```

## Flusso di Creazione Ordine

```
Client Request
      ↓
OrderController.createOrder()
      ↓
OrderService.createOrder()
      ↓
      ├─→ UserServiceClient.validateUser(userId)
      │       ↓
      │   UserController.validateUser()
      │       ↓
      │   UserRepository.existsById()
      │       ↓
      │   Return: Boolean
      │
      ├─→ ProductServiceClient.checkAvailability() (for each item)
      │       ↓
      │   ProductController.checkAvailability()
      │       ↓
      │   ProductService.checkAvailability()
      │       ↓
      │   ProductRepository.findById()
      │       ↓
      │   Return: Boolean
      │
      ├─→ Create Order entity
      │   ├─→ Calculate total amount
      │   └─→ Create OrderItems
      │
      ├─→ OrderRepository.save(order)
      │       ↓
      │   H2 Database
      │
      └─→ ProductServiceClient.reserveStock() (for each item)
              ↓
          ProductController.reserveStock()
              ↓
          ProductService.updateStock(-quantity)
              ↓
          ProductRepository.save()
              ↓
          Return: Updated ProductDTO

Return: OrderDTO to Client
```

## Transazioni e Gestione Errori

### Caso di Successo
1. Validazione utente ✓
2. Verifica disponibilità ✓
3. Salva ordine ✓
4. Riserva stock ✓
5. Return OrderDTO

### Caso di Fallimento
1. Validazione utente ✗ → Errore "Utente non valido"
2. Verifica disponibilità ✗ → Errore "Prodotto non disponibile"
3. Salvataggio ordine ✗ → Rollback transazione
4. Riserva stock ✗ → Rollback ordine, rilascio stock
5. Cancellazione ordine → Rilascio stock per tutti gli item

## Database Schema

### User Service - H2
```sql
CREATE TABLE users (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    phone_number VARCHAR(50),
    address VARCHAR(500),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

### Product Service - H2
```sql
CREATE TABLE products (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    stock_quantity INT NOT NULL,
    sku VARCHAR(100) UNIQUE NOT NULL,
    category VARCHAR(100),
    image_url VARCHAR(500),
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

### Order Service - H2
```sql
CREATE TABLE orders (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    order_number VARCHAR(50) UNIQUE NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) NOT NULL,
    order_date TIMESTAMP,
    shipping_address VARCHAR(500)
);

CREATE TABLE order_items (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    order_id BIGINT NOT NULL,
    product_id BIGINT NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id)
);
```

## Configurazione

### application.properties per servizio

**User Service:**
```properties
server.port=8081
spring.application.name=user-service
spring.datasource.url=jdbc:h2:mem:userdb
```

**Product Service:**
```properties
server.port=8082
spring.application.name=product-service
spring.datasource.url=jdbc:h2:mem:productdb
```

**Order Service:**
```properties
server.port=8083
spring.application.name=order-service
spring.datasource.url=jdbc:h2:mem:orderdb
user.service.url=http://localhost:8081
product.service.url=http://localhost:8082
```

## Tecnologie

| Stack | Tecnologia |
|-------|-----------|
| Linguaggio | Java 17 |
| Framework | Spring Boot 3.2.0 |
| Database | H2 (In-Memory) |
| ORM | Hibernate / JPA |
| REST | Spring Web |
| Async | Spring WebFlux / WebClient |
| Build | Maven |
| LombCode Generation | Lombok |

## Principi Architetturali

### ✓ Implementati
- **Single Responsibility**: Ogni servizio ha un dominio specifico
- **Database per Servizio**: Ogni servizio ha il proprio database
- **API REST**: Comunicazione tramite REST standard
- **Stateless Services**: Nessuno stato condiviso tra richieste
- **Independent Deployment**: Ogni servizio può essere avviato indipendentemente

### ○ Non Implementati (Future)
- **Service Discovery**: Nessun Eureka/Consul
- **API Gateway**: Accesso diretto ai servizi
- **Circuit Breaker**: Nessuna Resilience4j
- **Distributed Tracing**: Nessun Zipkin/Jaeger
- **Message Queue**: Sincrono, no Kafka/RabbitMQ
- **Configuration Server**: Configurazione locale
- **Container Orchestration**: No Kubernetes
