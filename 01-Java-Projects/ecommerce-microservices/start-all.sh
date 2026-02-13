#!/bin/bash

echo "=========================================="
echo "Avvio E-Commerce Microservices"
echo "=========================================="
echo ""

echo "[1/3] Avvio User Service (porta 8081)..."
cd "$(dirname "$0")/user-service"
gnome-terminal -- mvn spring-boot:run
sleep 10

echo "[2/3] Avvio Product Service (porta 8082)..."
cd "$(dirname "$0")/product-service"
gnome-terminal -- mvn spring-boot:run
sleep 10

echo "[3/3] Avvio Order Service (porta 8083)..."
cd "$(dirname "$0")/order-service"
gnome-terminal -- mvn spring-boot:run

echo ""
echo "=========================================="
echo "Tutti i servizi sono stati avviati!"
echo "=========================================="
echo ""
echo "User Service:   http://localhost:8081"
echo "Product Service: http://localhost:8082"
echo "Order Service:  http://localhost:8083"
echo ""
echo "H2 Consoles:"
echo "- User:    http://localhost:8081/h2-console"
echo "- Product: http://localhost:8082/h2-console"
echo "- Order:   http://localhost:8083/h2-console"
