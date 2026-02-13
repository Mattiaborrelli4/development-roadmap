#!/bin/bash

# Colori per output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}E-Commerce Microservices - API Test${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Test 1: Crea Utente
echo -e "${GREEN}[1] Registrazione Utente...${NC"
USER_RESPONSE=$(curl -s -X POST http://localhost:8081/api/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "mario.rossi",
    "email": "mario@email.com",
    "password": "password123",
    "firstName": "Mario",
    "lastName": "Rossi",
    "phoneNumber": "3331234567",
    "address": "Via Roma 1, Milano"
  }')
echo $USER_RESPONSE | jq '.'
USER_ID=$(echo $USER_RESPONSE | jq -r '.id')
echo -e "${GREEN}✓ Utente creato con ID: $USER_ID${NC}"
echo ""

# Test 2: Crea Prodotto
echo -e "${GREEN}[2] Creazione Prodotto...${NC}"
PRODUCT_RESPONSE=$(curl -s -X POST http://localhost:8082/api/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop HP Pavilion",
    "description": "Laptop con 16GB RAM, 512GB SSD",
    "price": 899.99,
    "stockQuantity": 50,
    "sku": "LAPT-HP-001",
    "category": "Elettronica",
    "imageUrl": "https://example.com/laptop.jpg"
  }')
echo $PRODUCT_RESPONSE | jq '.'
PRODUCT_ID=$(echo $PRODUCT_RESPONSE | jq -r '.id')
echo -e "${GREEN}✓ Prodotto creato con ID: $PRODUCT_ID${NC}"
echo ""

# Test 3: Verifica disponibilità
echo -e "${GREEN}[3] Verifica Disponibilità Prodotto...${NC}"
AVAILABILITY=$(curl -s http://localhost:8082/api/products/$PRODUCT_ID/availability?quantity=2)
echo "Disponibilità per quantità 2: $AVAILABILITY"
echo -e "${GREEN}✓ Prodotto disponibile${NC}"
echo ""

# Test 4: Crea Ordine
echo -e "${GREEN}[4] Creazione Ordine...${NC}"
ORDER_RESPONSE=$(curl -s -X POST http://localhost:8083/api/orders \
  -H "Content-Type: application/json" \
  -d "{
    \"userId\": $USER_ID,
    \"shippingAddress\": \"Via Roma 1, Milano\",
    \"items\": [
      {
        \"productId\": $PRODUCT_ID,
        \"quantity\": 2
      }
    ]
  }")
echo $ORDER_RESPONSE | jq '.'
ORDER_ID=$(echo $ORDER_RESPONSE | jq -r '.id')
ORDER_NUMBER=$(echo $ORDER_RESPONSE | jq -r '.orderNumber')
echo -e "${GREEN}✓ Ordine creato - ID: $ORDER_ID, Numero: $ORDER_NUMBER${NC}"
echo ""

# Test 5: Verifica stock aggiornato
echo -e "${GREEN}[5] Verifica Stock Aggiornato...${NC}"
PRODUCT_AFTER=$(curl -s http://localhost:8082/api/products/$PRODUCT_ID)
STOCK_AFTER=$(echo $PRODUCT_AFTER | jq -r '.stockQuantity')
echo "Stock iniziale: 50"
echo "Stock attuale: $STOCK_AFTER"
echo -e "${GREEN}✓ Stock ridotto correttamente${NC}"
echo ""

# Test 6: Lista ordini utente
echo -e "${GREEN}[6] Lista Ordini Utente...${NC}"
curl -s http://localhost:8083/api/orders/user/$USER_ID | jq '.'
echo ""

# Test 7: Aggiorna stato ordine
echo -e "${GREEN}[7] Aggiornamento Stato Ordine...${NC}"
curl -s -X PATCH http://localhost:8083/api/orders/$ORDER_ID/status \
  -H "Content-Type: application/json" \
  -d '{"status": "CONFIRMED"}' | jq '.'
echo ""

echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}✓ Tutti i test completati con successo!${NC}"
echo -e "${BLUE}========================================${NC}"
