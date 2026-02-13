#!/usr/bin/env python3
"""
Gestione Segnali UNIX/Linux
===========================
Modulo per la gestione dei segnali di sistema per shutdown controllato.

Concetti insegnati:
- Signal handling in UNIX/Linux
- Signal masks e blocking
- Graceful shutdown con cleanup
- Race conditions tra signal handlers
- Atomi operations per flag globali
"""

import signal
import logging
import sys
from typing import Callable, Optional


class SignalHandler:
    """
    Gestore centralizzato dei segnali per il daemon.

    Segnali gestiti:
    - SIGTERM (15): Termination signal - shutdown ordinato
    - SIGINT (2): Interrupt from keyboard (Ctrl+C)
    - SIGHUP (1): Hangup detected - spesso per reload config

    Pattern: Signal-safe flag + polling loop
    I signal handlers devono essere minimali e signal-safe.
    Evitare operazioni complesse nel handler!
    """

    def __init__(self):
        """Inizializza il gestore segnali."""
        self.shutdown_requested = False
        self.reload_requested = False
        self.logger = logging.getLogger(__name__)

        # Callbacks custom
        self.shutdown_callback: Optional[Callable] = None
        self.reload_callback: Optional[Callable] = None

    def handle_shutdown_signal(self, signum: int, frame) -> None:
        """
        Handler per segnali di shutdown (SIGTERM, SIGINT).

        NOTA: Questo deve essere MINIMALISTA e signal-safe!
        Operazioni permesse:
        - Write to self-pipe (signal-safe)
        - Modificare variabili volatile/atomic
        - Chiamare _exit()

        OPERAZIONI VIETATE nel handler:
        - Logging (non signal-safe!)
        - Print/printf (non signal-safe!)
        - Operazioni I/O complesse
        - Allocation memoria
        - Lock operations

        Pattern usato:
        1. Imposta flag atomico
        2. Il main loop polla il flag
        3. Cleanup avviene nel main context, non nel handler

        Args:
            signum: Numero del segnale ricevuto
            frame: Stack frame corrente (non usato)
        """
        # Signal-safe: sola modifica flag atomico
        self.shutdown_requested = True

        # NOTA: NON usare logging qui! Non è signal-safe.
        # Il log verrà scritto nel main loop dopo il check del flag.

        # Il kernel garantisce che le scritture a singolo byte siano atomiche
        # Per codice production, usare self-pipe pattern
        # import os
        # os.write(self.signal_pipe[1], b'X')

    def handle_reload_signal(self, signum: int, frame) -> None:
        """
        Handler per segnale di reload (SIGHUP).

        Tipicamente usato per:
        - Reload configurazione
        - Reopen log files (logrotate)
        - Refresh cache/resources

        Args:
            signum: Numero del segnale ricevuto
            frame: Stack frame corrente (non usato)
        """
        # Signal-safe: sola modifica flag atomico
        self.reload_requested = True

    def register_signals(self) -> None:
        """
        Registra i signal handlers con il sistema.

        Usa signal.signal() per associare handlers ai segnali.
        Signal masks possono bloccare segnali durante sezioni critiche.
        """
        # SIGTERM - Termination signal standard
        # Inviato da: systemctl stop, kill, service managers
        signal.signal(signal.SIGTERM, self.handle_shutdown_signal)

        # SIGINT - Interrupt da keyboard
        # Inviato da: Ctrl+C nel terminal
        signal.signal(signal.SIGINT, self.handle_shutdown_signal)

        # SIGHUP - Hangup (terminal disconnection)
        # Inviato da: shell quando logout, logrotate
        signal.signal(signal.SIGHUP, self.handle_reload_signal)

        # Ignora SIGPIPE - Broken pipe
        # Previene termination su write a socket chiuso
        signal.signal(signal.SIGPIPE, signal.SIG_IGN)

        self.logger.info("Signal handlers registrati: SIGTERM, SIGINT, SIGHUP")

    def block_signals_during_fork(self) -> None:
        """
        Blocca temporaneamente i segnali durante fork.

        Importante per processi multi-threaded:
        - Solo il thread che chiama fork() esiste nel child
        - Se signal arriva subito dopo fork, può essere perso
        - Block signals prima, unblock dopo fork

        Questo previene race conditions nella creazione processi.
        """
        # Crea signal mask con tutti i segnali
        # (In produzione, bloccare solo quelli specifici)
        # blocked = signal.pthread_sigmask(...)
        pass

    def should_shutdown(self) -> bool:
        """
        Verifica se è stato richiesto lo shutdown.

        Da chiamare nel main loop.

        Returns:
            True se shutdown richiesto
        """
        return self.shutdown_requested

    def should_reload(self) -> bool:
        """
        Verifica se è stato richiesto il reload.

        Returns:
            True se reload richiesto
        """
        return self.reload_requested

    def clear_reload_flag(self) -> None:
        """Resetta flag reload dopo averlo gestito."""
        self.reload_requested = False


class GracefulShutdown:
    """
    Context manager per shutdown controllato.

    Uso:
        with GracefulShutdown(signal_handler, cleanup_func):
            # Main loop
            while not signal_handler.should_shutdown():
                # ... codice daemon ...

    Garantisce cleanup anche su exception.
    """

    def __init__(self, signal_handler: SignalHandler, cleanup_callback: Callable):
        self.signal_handler = signal_handler
        self.cleanup_callback = cleanup_callback

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Esegue cleanup all'uscita del context."""
        self.cleanup_callback()

        # Log se terminato da segnale
        if self.signal_handler.shutdown_requested:
            logging.info("Shutdown completato su segnale")

        return False  # Non sopprime eccezioni


def ignore_sigpipe() -> None:
    """
    Ignora SIGPIPE per prevenire crash su write a socket chiuso.

    Importante per server con molti client:
    - Client può chiudere connection inaspettatamente
    - Write su socket chiuso genera SIGPIPE (default: terminate process)
    - Con SIG_IGN, write ritorna EPIPE error invece di crash

    Alternativa: usare MSG_NOSIGNAL su send()
    """
    signal.signal(signal.SIGPIPE, signal.SIG_IGN)


def setup_signal_handlers(logger: logging.Logger) -> SignalHandler:
    """
    Factory function per creare e configurare SignalHandler.

    Args:
        logger: Logger configurato

    Returns:
        SignalHandler configurato e registrato
    """
    handler = SignalHandler()
    handler.logger = logger
    handler.register_signals()
    ignore_sigpipe()

    return handler
