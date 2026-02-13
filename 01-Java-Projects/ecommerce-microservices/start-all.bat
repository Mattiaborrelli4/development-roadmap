@echo off
echo ==========================================
echo Avvio E-Commerce Microservices
echo ==========================================
echo.

echo [1/3] Avvio User Service (porta 8081)...
start "User Service" cmd /k "cd /d %~dp0user-service && mvn spring-boot:run"
timeout /t 10 /nobreak >nul

echo [2/3] Avvio Product Service (porta 8082)...
start "Product Service" cmd /k "cd /d %~dp0product-service && mvn spring-boot:run"
timeout /t 10 /nobreak >nul

echo [3/3] Avvio Order Service (porta 8083)...
start "Order Service" cmd /k "cd /d %~dp0order-service && mvn spring-boot:run"

echo.
echo ==========================================
echo Tutti i servizi sono stati avviati!
echo ==========================================
echo.
echo User Service:   http://localhost:8081
echo Product Service: http://localhost:8082
echo Order Service:  http://localhost:8083
echo.
echo H2 Consoles:
echo - User:    http://localhost:8081/h2-console
echo - Product: http://localhost:8082/h2-console
echo - Order:   http://localhost:8083/h2-console
echo.
echo Premi un tasto per chiudere questa finestra...
pause >nul
