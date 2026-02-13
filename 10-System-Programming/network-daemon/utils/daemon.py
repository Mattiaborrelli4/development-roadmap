#!/usr/bin/env python3
"""
Utilità di Daemonizzazione
=========================
Modulo per la conversione di un processo in daemon UNIX/Linux.

Concetti insegnati:
- fork(): Creazione di nuovi processi
- setsid(): Creazione di una nuova sessione
- chdir(): Cambiamento directory di lavoro
- umask(): Modifica maschera permessi file
- Redirezione standard file descriptors
"""

import os
import sys
import signal
from typing import Optional


def daemonize(work_dir: str = "/") -> int:
    """
    Converte il processo corrente in un daemon.

    Processo di daemonizzazione a doppio fork:
    1. Primo fork e exit del parent - disassocia dal terminal
    2. setsid() - crea nuova sessione, diventa leader sessione
    3. Secondo fork e exit - previene acquisizione terminal (TTY)
    4. Cambia directory radice per non bloccare filesystem
    5. Imposta umask per permessi prevedibili
    6. Redirige standard file descriptors

    Args:
        work_dir: Directory di lavoro del daemon (default: /)

    Returns:
        PID del processo daemon

    Raises:
        OSError: Se fork fallisce
    """
    try:
        # Primo fork
        pid = os.fork()
        if pid > 0:
            # Parent exit - il processo diventa orfano
            # Init (PID 1) lo adotta
            sys.exit(0)
    except OSError as e:
        sys.stderr.write(f"Primo fork fallito: {e}\n")
        sys.exit(1)

    # Decoupling dal parent environment
    # Crea nuova sessione, diventa leader sessione e process group
    # Perde il controlling terminal
    os.setsid()

    try:
        # Secondo fork
        # Garantisce che il daemon non acquisisca mai un TTY
        # Anche se apre un terminal device in futuro
        pid = os.fork()
        if pid > 0:
            # Secondo parent exit
            sys.exit(0)
    except OSError as e:
        sys.stderr.write(f"Secondo fork fallito: {e}\n")
        sys.exit(1)

    # Il processo è ora un daemon completo
    # Cambia directory radice per non bloccare filesystem unmount
    try:
        os.chdir(work_dir)
    except OSError as e:
        sys.stderr.write(f"Impossibile cambiare directory in {work_dir}: {e}\n")
        sys.exit(1)

    # Imposta umask permittendo lettura/scrittura a tutti
    # I file creati dal daemon hanno permessi prevedibili
    os.umask(0)

    # Chiudi tutti i file descriptors aperti
    # Evita resource leak e interference con parent
    try:
        maxfd = os.sysconf("SC_OPEN_MAX")
    except (AttributeError, ValueError):
        maxfd = 256  # Fallback

    for fd in range(0, maxfd):
        try:
            os.close(fd)
        except OSError:
            pass  # Ignora fd già chiusi

    # Redirigi standard file descriptors
    # Il daemon non può usare stdin/stdout/stderr del parent
    os.open(os.devnull, os.O_RDWR)  # stdin
    os.dup2(0, 1)  # stdout -> stdin
    os.dup2(0, 2)  # stderr -> stdin

    return os.getpid()


def create_pid_file(pid_file: str) -> bool:
    """
    Crea un file PID per tracciare il daemon in esecuzione.

    Il file PID contiene il PID del processo daemon.
    Utile per:
    - Verificare se il daemon è in esecuzione
    - Inviare segnali al daemon
    - Evitare duplicati (PID lock)

    Args:
        pid_file: Path del file PID

    Returns:
        True se successo, False se già in esecuzione

    Raises:
        OSError: Se errore I/O
    """
    import fcntl

    # Verifica se il file esiste già
    if os.path.exists(pid_file):
        try:
            with open(pid_file, 'r') as f:
                old_pid = int(f.read().strip())

            # Verifica se il processo è ancora in esecuzione
            try:
                os.kill(old_pid, 0)  # Signal 0 = check esistenza
                print(f"Daemon già in esecuzione con PID {old_pid}")
                return False
            except OSError:
                # Processo non esiste, rimuovi file PID obsoleto
                os.remove(pid_file)
        except (ValueError, OSError):
            os.remove(pid_file)

    # Crea nuovo file PID con lock esclusivo
    try:
        # Crea directory se non esiste
        pid_dir = os.path.dirname(pid_file)
        if pid_dir and not os.path.exists(pid_dir):
            os.makedirs(pid_dir, mode=0o755)

        fd = os.open(pid_file, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
        with os.fdopen(fd, 'w') as f:
            f.write(str(os.getpid()))

        # Imposta lock sul file
        #fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)

        return True
    except OSError as e:
        sys.stderr.write(f"Impossibile creare file PID {pid_file}: {e}\n")
        return False


def remove_pid_file(pid_file: str) -> None:
    """
    Rimuove il file PID al termine del daemon.

    Args:
        pid_file: Path del file PID
    """
    try:
        if os.path.exists(pid_file):
            os.remove(pid_file)
    except OSError as e:
        sys.stderr.write(f"Avvertimento: impossibile rimuovere {pid_file}: {e}\n")


def get_pid_from_file(pid_file: str) -> Optional[int]:
    """
    Legge il PID dal file.

    Args:
        pid_file: Path del file PID

    Returns:
        PID se trovato, None altrimenti
    """
    try:
        if os.path.exists(pid_file):
            with open(pid_file, 'r') as f:
                return int(f.read().strip())
    except (ValueError, OSError):
        pass
    return None


def is_process_running(pid: int) -> bool:
    """
    Verifica se un processo è in esecuzione.

    Args:
        pid: Process ID da verificare

    Returns:
        True se in esecuzione, False altrimenti
    """
    try:
        os.kill(pid, 0)  # Signal 0 non termina, solo check
        return True
    except OSError:
        return False
