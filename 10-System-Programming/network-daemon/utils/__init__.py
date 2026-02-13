"""
Utils Package per Echo Daemon
==============================
Moduli di utilità per daemonizzazione, signal handling e logging.
"""

from .daemon import (
    daemonize,
    create_pid_file,
    remove_pid_file,
    get_pid_from_file,
    is_process_running
)

from .signal import (
    SignalHandler,
    GracefulShutdown,
    setup_signal_handlers
)

from .log import (
    setup_logging,
    get_logger,
    LoggerAdapter,
    log_client_connection,
    log_server_start
)

__all__ = [
    # Daemon utilities
    'daemonize',
    'create_pid_file',
    'remove_pid_file',
    'get_pid_from_file',
    'is_process_running',

    # Signal handling
    'SignalHandler',
    'GracefulShutdown',
    'setup_signal_handlers',

    # Logging
    'setup_logging',
    'get_logger',
    'LoggerAdapter',
    'log_client_connection',
    'log_server_start',
]
