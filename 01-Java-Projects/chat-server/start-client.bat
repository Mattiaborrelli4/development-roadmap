@echo off
set NICKNAME=%1
set HOST=%2
set PORT=%3

if "%NICKNAME%"=="" set NICKNAME=User%RANDOM%
if "%HOST%"=="" set HOST=localhost
if "%PORT%"=="" set PORT=9999

echo Avvio del Chat Client...
echo.
cd src\client
java client.ChatClient %NICKNAME% %HOST% %PORT%
