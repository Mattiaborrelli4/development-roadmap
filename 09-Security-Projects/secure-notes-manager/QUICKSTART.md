# 🚀 Guida Rapida - Secure Notes Manager

## Setup Rapido (2 minuti)

```bash
# 1. Installa le dipendenze
pip install -r requirements.txt

# 2. Inizializza il vault
python main.py init

# 3. Sblocca il vault
python main.py unlock

# 4. Aggiungi una nota nella shell interattiva
> add
```

## Comandi Essenziali

```bash
# Inizializza nuovo vault
python main.py init

# Sblocca vault (apre shell interattiva)
python main.py unlock

# Aggiungi nota (veloce)
python main.py add "Titolo" "Contenuto" --tags "lavoro"

# Lista note
python main.py list

# Visualizza nota
python main.py view 1

# Cerca note
python main.py search "chiave"

# Elimina nota
python main.py delete 1

# Export backup
python main.py export backup.enc

# Import backup
python main.py import-backup backup.enc

# Genera password sicura
python main.py generate
```

## Shell Interattiva

Dopo `unlock`, usa questi comandi:

```
list              # Lista tutte le note
view <id>         # Visualizza una nota
add               # Aggiungi nuova nota
edit <id>         # Modifica nota
delete <id>       # Elimina nota
search <query>    # Cerca note
quit              # Esci
```

## Esempio Completo

```bash
# 1. Crea vault
python main.py init
Password: [inserisci password forte]
Conferma: [reinserisci password]

# 2. Sblocca
python main.py unlock
Password: ****

# 3. Nella shell
> add
Titolo: Password WIFI
Contenuto: WPA3-Key: xY7#kL9@mP2
Tags: wifi,casa

> add
Titolo: Note lavoro
Contenuto: Progetto Zeus - deadline 15/02
Tags: lavoro

> list
> view 1
> search "wifi"
> quit
```

## Consigli per la Sicurezza

✅ **Password Forte**: Minimo 12 caratteri, maiuscole/minuscole/numeri/simboli
✅ **Backup Regolari**: `python main.py export backup_$(date +%Y%m%d).enc`
✅ **Test Restore**: Verifica periodicamente che i backup funzionino
✅ **Update**: Tieni aggiornate le dipendenze

❌ **NO**: Password comuni, riutilizzo password, condivisione credenziali

## Troubleshooting

**Errore: "Vault non trovato"**
→ Usa prima `python main.py init`

**Errore: "Password non valida"**
→ Controlla maiuscole/minuscole, prova a riprovare

**Errore: "Dipendenze mancanti"**
→ Esegui `pip install -r requirements.txt`

## Archivio Files

- `vault.enc` - Vault principale (NON cancellare!)
- `backups/` - Backup automatici
- `backup_*.enc` - Backup manuali

## Supporto

Leggi `README.md` per documentazione completa.
