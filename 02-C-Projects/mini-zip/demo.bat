@echo off
REM Mini-Zip Demo Script
REM Demonstra le funzionalita' di compressione RLE

echo ==========================================
echo Mini-Zip - Demo Compressione RLE
echo ==========================================
echo.

REM Crea un file di test semplice
echo Creazione file di test...
echo AAAAAAAAAAAAABBBBBCCCCCCCCCCCCDDDDDDDDD > demo.txt
echo XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX >> demo.txt
echo YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY >> demo.txt
echo.

echo File originale:
type demo.txt
echo.
echo ==========================================
echo.

REM Mostra informazioni sul file
echo Dimensione del file originale:
dir demo.txt | find "demo.txt"
echo.

REM Comprimi il file
echo Compressione in corso...
mini-zip.exe c demo.txt
echo.

REM Decomprimi il file
echo Decompressione in corso...
mini-zip.exe d demo.txt.rle demo-restored.txt
echo.

REM Verifica l'integrita'
echo Verifica integrita' dei file:
fc demo.txt demo-restored.txt >nul
if errorlevel 1 (
    echo ERRORE: I file sono diversi!
) else (
    echo SUCCESSO: I file sono identici!
)
echo.

REM Mostra i risultati
echo Confronto dimensioni:
echo.
echo Originale:
dir demo.txt | find "demo.txt"
echo.
echo Compresso:
dir demo.txt.rle | find "demo.txt"
echo.
echo Ripristinato:
dir demo-restored.txt | find "demo-restored"
echo.

echo ==========================================
echo Demo completata!
echo ==========================================
echo.
