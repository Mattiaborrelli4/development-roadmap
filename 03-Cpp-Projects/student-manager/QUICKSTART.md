# 🚀 Quick Start - Student Management System

## Avvio Rapido (30 secondi)

### Windows
```batch
# Compila (solo la prima volta)
build.bat

# Esegui
student_manager.exe
```

### Con Make
```bash
make run
```

## Prime Operazioni da Provare

1. **Carica dati di esempio**
   - Menu: `9`
   - File: `sample_data.txt`

2. **Visualizza studenti**
   - Menu: `2`

3. **Aggiungi uno studente**
   - Menu: `1`
   - Inserisci: Mario, Rossi, 20, Informatica, 28.5

4. **Cerca per ID**
   - Menu: `3`
   - ID: `1`

5. **Salva ed esci**
   - Menu: `0`
   - Conferma salvataggio: `s`

## Comandi Menu Rapidi

| Comando | Funzione |
|---------|----------|
| `1` | Aggiungi studente |
| `2` | Mostra tutti |
| `3` | Cerca per ID |
| `4` | Cerca per nome |
| `5` | Cerca per cognome |
| `6` | Aggiorna studente |
| `7` | Elimina studente |
| `8` | Salva su file |
| `9` | Carica da file |
| `0` | Esci |

## Formato Database CSV

```
id,nome,cognome,età,corso,media
es: 1,Mario,Rossi,20,Informatica,28.5
```

## Risoluzione Problemi

**Non compila?**
- Verifica g++ installato
- Usa `build.bat` su Windows

**Dati persi?**
- Carica `sample_data.txt`
- Menu: `9`

**Errore input?**
- Premi solo INVIO per mantenere valori esistenti
- Inserisci numeri validi per età/media

## File Importanti

- `README.md` - Documentazione completa
- `USAGE.md` - Esempi dettagliati
- `sample_data.txt` - 5 studenti di esempio

---
**Leggi USAGE.md per esempi completi!** 📚
