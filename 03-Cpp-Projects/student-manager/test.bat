@echo off
REM Script di test per Student Management System
REM Questo script crea un test automatico delle funzionalità principali

echo ==========================================
echo  TEST SISTEMA GESTIONE STUDENTI
echo ==========================================
echo.

REM Creazione di un file di test
echo 1,Mario,Rossi,20,Informatica,28.5 > test_students.txt
echo 2,Laura,Bianchi,21,Matematica,29.0 >> test_students.txt
echo 3,Giuseppe,Verdi,22,Fisica,27.5 >> test_students.txt

echo File di test creato: test_students.txt
echo.

echo Esecuzione del programma...
echo.
echo Prova a:
echo 1. Caricare i dati dal file (opzione 9) - usa "test_students.txt"
echo 2. Visualizzare tutti gli studenti (opzione 2)
echo 3. Aggiungere un nuovo studente (opzione 1)
echo 4. Cercare per ID (opzione 3)
echo 5. Aggiornare uno studente (opzione 6)
echo 6. Salvare su file (opzione 8)
echo.

pause
