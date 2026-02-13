#!/usr/bin/env python3
"""
Sistema di Logging per Daemon
=============================
Modulo per la configurazione del logging su file e console.

Concetti insegnati:
- Logging levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Log rotation per prevenire file overflow
- Formattazione log con timestamp
- Thread-safe logging
- Logging in ambiente daemon (no stdout/stderr)
"""

import logging
import logging.handlers
import sys
import os
from typing import Optional


def setup_logging(
    log_file: str,
    log_level: str = "INFO",
    console: bool = False,
    max_bytes: int = 10 * 1024 * 1024,  # 10 MB
    backup_count: int = 5
) -> logging.Logger:
    """
    Configura il sistema di logging per il daemon.

    Features:
    - Rotazione automatica log file (size-based)
    - Backup files con numerazione
    - Formato dettagliato con timestamp, level, PID
    - Opzionale output console (per debug non-daemon)

    Args:
        log_file: Path del file di log
        log_level: Level minimo (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        console: Se True, log anche su console
        max_bytes: Dimensione max file prima rotation
        backup_count: Numero di backup files da mantenere

    Returns:
        Logger configurato
    """
    # Crea directory log se non esiste
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        try:
            os.makedirs(log_dir, mode=0o755)
        except OSError as e:
            sys.stderr.write(f"Impossibile creare directory log: {e}\n")
            # Fallback a /tmp
            log_file = f"/tmp/echo-daemon-{os.getuid()}.log"

    # Configura root logger
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    # Formatter con info dettagliate
    # Format: timestamp | level | PID | message
    formatter = logging.Formatter(
        fmt='%(asctime)s | %(levelname)-8s | PID:%(process)d | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # File handler con rotation
    # RotatingFileHandler:
    # - Chiude file, rinomina con .1, .2, etc.
    # - Crea nuovo file vuoto
    # - Mantiene backup_count files
    try:
        file_handler = logging.handlers.RotatingFileHandler(
            filename=log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            mode='a'  # Append mode
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(getattr(logging, log_level.upper(), logging.INFO))
        logger.addHandler(file_handler)
    except OSError as e:
        sys.stderr.write(f"Impossibile aprire file log {log_file}: {e}\n")
        # Fallback a /tmp
        fallback_log = f"/tmp/echo-daemon-{os.getuid()}.log"
        try:
            file_handler = logging.handlers.RotatingFileHandler(
                filename=fallback_log,
                maxBytes=max_bytes,
                backupCount=backup_count
            )
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except OSError:
            sys.stderr.write("Impossibile creare file log in /tmp\n")

    # Opzionale: log su console (utile per debug)
    # Non usare quando daemonized (nessun terminal!)
    if console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        console_handler.setLevel(getattr(logging, log_level.upper(), logging.INFO))
        logger.addHandler(console_handler)

    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Ottieni un logger con nome specifico.

    Best practice: usare named loggers invece di root logger.

    Args:
        name: Nome del logger (tipicamente __name__ del modulo)

    Returns:
        Logger instance
    """
    return logging.getLogger(name)


class LoggerAdapter:
    """
    Adapter per aggiungere context extra ai log.

    Uso:
        adapter = LoggerAdapter(logger, {'client': '192.168.1.1'})
        adapter.info("Connection accepted")
        # Output: ... | client=192.168.1.1 | Connection accepted
    """

    def __init__(self, logger: logging.Logger, extra: dict):
        self.logger = logger
        self.extra = extra

    def _log(self, level: int, msg: str, *args, **kwargs):
        # Aggiunge context extra
        extra_str = " | ".join(f"{k}={v}" for k, v in self.extra.items())
        if extra_str:
            msg = f"{extra_str} | {msg}"

        self.logger.log(level, msg, *args, **kwargs)

    def debug(self, msg: str, *args, **kwargs):
        self._log(logging.DEBUG, msg, *args, **kwargs)

    def info(self, msg: str, *args, **kwargs):
        self._log(logging.INFO, msg, *args, **kwargs)

    def warning(self, msg: str, *args, **kwargs):
        self._log(logging.WARNING, msg, *args, **kwargs)

    def error(self, msg: str, *args, **kwargs):
        self._log(logging.ERROR, msg, *args, **kwargs)

    def critical(self, msg: str, *args, **kwargs):
        self._log(logging.CRITICAL, msg, *args, **kwargs)


def log_client_connection(logger: logging.Logger, client_addr: tuple, action: str):
    """
    Helper per loggare connessioni client in modo consistente.

    Args:
        logger: Logger instance
        client_addr: Tuple (ip, port) del client
        action: Azione (accepted, closed, error)
    """
    ip, port = client_addr
    logger.info(f"Client {ip}:{port} - {action}")


def log_server_start(logger: logging.Logger, host: str, port: int, protocol: str):
    """
    Helper per loggare l'avvio del server.

    Args:
        logger: Logger instance
        host: Host di bind
        port: Porta TCP/UDP
        protocol: "TCP" o "UDP"
    """
    logger.info(f"Server {protocol} avviato su {host}:{port}")
    logger.info(f"Pronto ad accettare connessioni...")
