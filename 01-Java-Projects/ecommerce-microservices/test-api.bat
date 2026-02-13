@echo off
setlocal enabledelayedexpansion

echo ========================================
echo E-Commerce Microservices - API Test
echo ========================================
echo.

:: Test 1: Crea Utente
echo [1] Registrazione Utente...
curl -s -X POST http://localhost:8081/api/users/register ^
  -H "Content-Type: application/json" ^
  -d "{\"username\": \"mario.rossi\", \"email\": \"mario@email.com\", \"password\": \"password123\", \"firstName\": \"Mario\", \"lastName\": \"Rossi\", \"phoneNumber\": \"3331234567\", \"address\": \"Via Roma 1, Milano\"}" > user_response.json
type user_response.json
for /f "tokens=2 delims=:," %%a in ('findstr /C:"\"id\"" user_response.json') do set USER_ID=%%a
set USER_ID=%USER_ID: =%
echo.
echo ✓ Utente creato
echo.

:: Test 2: Crea Prodotto
echo [2] Creazione Prodotto...
curl -s -X POST http://localhost:8082/api/products ^
  -H "Content-Type: application/json" ^
  -d "{\"name\": \"Laptop HP Pavilion\", \"description\": \"Laptop con 16GB RAM\", \"price\": 899.99, \"stockQuantity\": 50, \"sku\": \"LAPT-HP-001\", \"category\": \"Elettronica\"}" > product_response.json
type product_response.json
echo.
echo ✓ Prodotto creato
echo.

echo ========================================
echo ✓ Test completati!
echo ========================================
pause
