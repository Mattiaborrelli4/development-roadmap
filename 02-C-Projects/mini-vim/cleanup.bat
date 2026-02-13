@echo off
REM Mini Vim - Script di pulizia per Windows
REM Rimuove i file oggetto e l'eseguibile

echo Pulizia dei file di compilazione...
echo.

if exist buffer.o del /Q buffer.o
if exist editor.o del /Q editor.o
if exist mini-vim.exe del /Q mini-vim.exe

echo Pulizia completata!
echo.
pause
