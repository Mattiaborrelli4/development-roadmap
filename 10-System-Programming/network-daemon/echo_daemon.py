#!/usr/bin/env python3
"""
Echo Network Daemon
===================
Server TCP/UDP echo service per apprendimento socket programming.

Caratteristiche:
- Server TCP echo (connection-oriented)
- Server UDP echo (connectionless)
- Multi-client con multiprocessing
- Signal handling per graceful shutdown
- Daemonization completa
- Configurazione via YAML
- Logging su file con rotation

Concetti insegnati:
- Socket API (socket, bind, listen, accept, recv, send)
- Protocolli TCP vs UDP
- Multiprocessing per concorrenza
- Signal handling in UNIX/Linux
- Daemonizzazione
- PID file management
"""

import sys
import os
import socket
import argparse
import yaml
import signal
from multiprocessing import Process, Queue
from typing import Dict, Any, Optional
from pathlib import Path

# Add utils directory to path
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from utils.daemon import (
    daemonize, create_pid_file, remove_pid_file,
    get_pid_from_file, is_process_running
)
from utils.signal import setup_signal_handlers
from utils.log import setup_logging, log_client_connection, log_server_start


class TCPEchoServer:
    """
    Server TCP Echo.

    TCP (Transmission Control Protocol):
    - Connection-oriented
    - Reliable, ordered delivery
    - Flow control, congestion control
    - Stream-based (no message boundaries)

    Socket lifecycle:
    1. socket() - crea socket endpoint
    2. bind() - associa address:port
    3. listen() - marca come passive, ready for accept
    4. accept() - attendi nuova connessione
    5. recv()/send() - trasferimento dati
    6. close() - chiudi connection
    """

    def __init__(self, config: Dict[str, Any], logger):
        self.host = config['bind_host']
        self.port = config['port']
        self.max_clients = config['max_clients']
        self.buffer_size = config['buffer_size']
        self.client_timeout = config.get('client_timeout', 300)

        self.server_socket: Optional[socket.socket] = None
        self.clients: list[Process] = []
        self.logger = logger
        self.running = False

    def start(self) -> None:
        """Avvia il server TCP."""
        try:
            # Crea TCP socket
            # AF_INET = IPv4
            # SOCK_STREAM = TCP (connection-oriented)
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # SO_REUSEADDR permette riavvio immediato
            # Senza: bind() fallisce con "Address already in use" per TIME_WAIT
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            # Bind socket all'address:port
            self.server_socket.bind((self.host, self.port))

            # Listen: marca socket come passive
            # backlog = max pending connections queue
            self.server_socket.listen(self.max_clients)

            self.running = True
            log_server_start(self.logger, self.host, self.port, "TCP")

        except OSError as e:
            self.logger.error(f"Errore avvio server TCP: {e}")
            raise

    def stop(self) -> None:
        """Ferma il server e tutti i client attivi."""
        self.logger.info("Arresto server TCP...")

        self.running = False

        # Chiudi server socket
        if self.server_socket:
            try:
                self.server_socket.close()
            except OSError as e:
                self.logger.error(f"Errore chiusura server socket: {e}")

        # Termina tutti i processi client
        for client_proc in self.clients:
            if client_proc.is_alive():
                client_proc.terminate()
                client_proc.join(timeout=2)
                if client_proc.is_alive():
                    client_proc.kill()

        self.clients.clear()
        self.logger.info("Server TCP fermato")

    def handle_client(self, client_socket: socket.socket, client_addr: tuple) -> None:
        """
        Gestisce un singolo client TCP (processo separato).

        Protocollo echo:
        1. Ricevi dati dal client
        2. Ritrasmetti gli stessi dati (echo)
        3. Ripeti fino a disconnessione

        Args:
            client_socket: Socket della connessione client
            client_addr: (IP, port) del client
        """
        try:
            # Set timeout per evitare client zombie
            if self.client_timeout > 0:
                client_socket.settimeout(self.client_timeout)

            log_client_connection(self.logger, client_addr, "connected")

            # Echo loop
            while True:
                try:
                    # Ricevi dati (bloccante)
                    data = client_socket.recv(self.buffer_size)

                    if not data:
                        # Client ha chiuso connection (FIN packet)
                        break

                    # Echo: ritrasmessi identici
                    client_socket.sendall(data)

                    # Log data (opzionale, verbose)
                    # self.logger.debug(f"Echoed {len(data)} bytes")

                except socket.timeout:
                    self.logger.warning(f"Client {client_addr} timeout")
                    break
                except OSError as e:
                    self.logger.error(f"Errore I/O client {client_addr}: {e}")
                    break

        finally:
            client_socket.close()
            log_client_connection(self.logger, client_addr, "disconnected")

    def accept_loop(self, signal_handler) -> None:
        """
        Main loop: accetta nuove connessioni.

        Pattern:
        - accept() blocca finché non arriva connessione
        - Fork processo per gestire il client
        - Parent torna ad accept()

        Args:
            signal_handler: Per controllare shutdown
        """
        while self.running and not signal_handler.should_shutdown():
            try:
                # Set timeout su accept per controllare signal periodicamente
                self.server_socket.settimeout(1.0)

                try:
                    # Accetta nuova connessione
                    # Returns: (new_socket, client_address)
                    # new_socket è socket dedicato a questa connessione
                    client_socket, client_addr = self.server_socket.accept()

                    # Verifica limite client
                    # Cleanup processi terminati
                    self.clients = [p for p in self.clients if p.is_alive()]

                    if len(self.clients) >= self.max_clients:
                        self.logger.warning(f"Max clients ({self.max_clients}) reached, rejecting {client_addr}")
                        client_socket.close()
                        continue

                    # Fork processo per gestire client
                    # Ogni client ha processo separato (concorrenza)
                    process = Process(
                        target=self.handle_client,
                        args=(client_socket, client_addr)
                    )
                    process.start()

                    # Parent chiude socket (child ha la sua copia)
                    # Nota: In Unix, file descriptors sono duplicati in fork
                    client_socket.close()

                    self.clients.append(process)

                except socket.timeout:
                    # Timeout normale, ripeti per check signal
                    continue
                except OSError as e:
                    if self.running:
                        self.logger.error(f"Errore accept: {e}")
                    break

            except Exception as e:
                self.logger.error(f"Errore imprevisto: {e}")
                break


class UDPEchoServer:
    """
    Server UDP Echo.

    UDP (User Datagram Protocol):
    - Connectionless (no handshaking)
    - Unreliable, unordered delivery
    - No flow/congestion control
    - Message-based (preserves boundaries)
    - Lightweight, low latency

    Differenze TCP vs UDP:
    - No listen()/accept() in UDP
    - recvfrom()/sendto() invece di recv()/send()
    - No connection state
    - Packet loss possibile
    """

    def __init__(self, config: Dict[str, Any], logger):
        self.host = config['bind_host']
        self.port = config['udp_port']
        self.buffer_size = config['buffer_size']

        self.server_socket: Optional[socket.socket] = None
        self.logger = logger
        self.running = False

    def start(self) -> None:
        """Avvia il server UDP."""
        try:
            # Crea UDP socket
            # SOCK_DGRAM = UDP (datagram-oriented)
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            # SO_REUSEADDR permette più bind sullo stesso port
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            # Bind all'address:port
            self.server_socket.bind((self.host, self.port))

            self.running = True
            log_server_start(self.logger, self.host, self.port, "UDP")

        except OSError as e:
            self.logger.error(f"Errore avvio server UDP: {e}")
            raise

    def stop(self) -> None:
        """Ferma il server UDP."""
        self.logger.info("Arresto server UDP...")
        self.running = False

        if self.server_socket:
            self.server_socket.close()

        self.logger.info("Server UDP fermato")

    def serve_loop(self, signal_handler) -> None:
        """
        Main loop UDP: ricevi e echo datagrammi.

        UDP non ha connessioni:
        - Ogni packet è indipendente
        - recvfrom() restituisce address del sender
        - sendto() invia a specific address

        Args:
            signal_handler: Per controllare shutdown
        """
        while self.running and not signal_handler.should_shutdown():
            try:
                # Set timeout per check signal
                self.server_socket.settimeout(1.0)

                try:
                    # Ricevi datagram + sender address
                    data, client_addr = self.server_socket.recvfrom(self.buffer_size)

                    if data:
                        # Echo: ritrasmessi al sender
                        self.server_socket.sendto(data, client_addr)

                        # Log
                        ip, port = client_addr
                        self.logger.debug(f"UDP: {len(data)} bytes from {ip}:{port}")

                except socket.timeout:
                    continue
                except OSError as e:
                    if self.running:
                        self.logger.error(f"Errore UDP I/O: {e}")
                    break

            except Exception as e:
                self.logger.error(f"Errore imprevisto UDP: {e}")
                break


class EchoDaemon:
    """
    Main Daemon class.

    Coordina:
    - Caricamento configurazione
    - Daemonizzazione
    - Server TCP e UDP
    - Signal handling
    - PID file management
    """

    def __init__(self, config_file: str):
        self.config_file = config_file
        self.config = self._load_config()
        self.logger = None
        self.signal_handler = None

        self.tcp_server: Optional[TCPEchoServer] = None
        self.udp_server: Optional[UDPEchoServer] = None
        self.tcp_process: Optional[Process] = None
        self.udp_process: Optional[Process] = None

    def _load_config(self) -> Dict[str, Any]:
        """Carica configurazione da file YAML."""
        try:
            with open(self.config_file, 'r') as f:
                config = yaml.safe_load(f)
                return config
        except FileNotFoundError:
            print(f"Errore: file config non trovato: {self.config_file}")
            sys.exit(1)
        except yaml.YAMLError as e:
            print(f"Errore parsing YAML: {e}")
            sys.exit(1)

    def _setup_logging(self) -> None:
        """Configura il logging."""
        log_file = self.config['log_file']
        log_level = self.config['log_level']
        console = not self.config.get('daemonize', True)

        # Su Windows, usa path relativi se /var non disponibile
        if os.name == 'nt':
            log_file = log_file.replace('/var/log/', './logs/')
            log_file = log_file.replace('/var/run/', './')

        max_size = self.config.get('max_log_size', 10 * 1024 * 1024)
        backup_count = self.config.get('log_backup_count', 5)

        self.logger = setup_logging(
            log_file=log_file,
            log_level=log_level,
            console=console,
            max_bytes=max_size,
            backup_count=backup_count
        )

    def daemonize_if_needed(self) -> None:
        """Daemonizza il processo se richiesto dalla config."""
        if self.config.get('daemonize', True):
            self.logger.info("Daemonizzazione in corso...")

            pid_file = self.config['pid_file']

            # Su Windows, adatta path
            if os.name == 'nt':
                pid_file = pid_file.replace('/var/run/', './')

            # Crea PID file
            if not create_pid_file(pid_file):
                self.logger.error("Daemon già in esecuzione")
                sys.exit(1)

            # Daemonizza
            daemonize()

            self.logger.info(f"Daemon avviato con PID {os.getpid()}")
            self.logger.info(f"PID file: {pid_file}")
        else:
            self.logger.info("Esecuzione in foreground (non-daemon)")

    def start(self) -> None:
        """Avvia il daemon."""
        # Setup logging
        self._setup_logging()

        self.logger.info("=" * 50)
        self.logger.info("Echo Daemon avvio")
        self.logger.info("=" * 50)

        # Setup signal handlers
        self.signal_handler = setup_signal_handlers(self.logger)

        # Daemonizza se richiesto
        self.daemonize_if_needed()

        # Crea server
        self.tcp_server = TCPEchoServer(self.config, self.logger)
        self.udp_server = UDPEchoServer(self.config, self.logger)

        # Avvia TCP e UDP in processi separati
        self.tcp_process = Process(target=self._run_tcp_server)
        self.udp_process = Process(target=self._run_udp_server)

        self.tcp_process.start()
        self.udp_process.start()

        self.logger.info("Server TCP e UDP attivi")

        # Attendi segnale di shutdown
        self._wait_for_shutdown()

        # Cleanup
        self._cleanup()

    def _run_tcp_server(self) -> None:
        """Wrapper per eseguire TCP server con signal handler."""
        # Setup logging nel processo child
        self._setup_logging()

        # Setup signal handlers nel child
        self.signal_handler = setup_signal_handlers(self.logger)

        # Avvia server
        self.tcp_server.start()
        self.tcp_server.accept_loop(self.signal_handler)
        self.tcp_server.stop()

    def _run_udp_server(self) -> None:
        """Wrapper per eseguire UDP server con signal handler."""
        # Setup logging nel processo child
        self._setup_logging()

        # Setup signal handlers nel child
        self.signal_handler = setup_signal_handlers(self.logger)

        # Avvia server
        self.udp_server.start()
        self.udp_server.serve_loop(self.signal_handler)
        self.udp_server.stop()

    def _wait_for_shutdown(self) -> None:
        """Attende segnale di shutdown."""
        self.logger.info("Daemon in esecuzione. Premi Ctrl+C per fermare.")

        while not self.signal_handler.should_shutdown():
            try:
                signal.pause()  # Attende segnali
            except KeyboardInterrupt:
                break

    def _cleanup(self) -> None:
        """Pulizia risorse."""
        self.logger.info("Cleanup in corso...")

        # Termina processi server
        if self.tcp_process and self.tcp_process.is_alive():
            self.tcp_process.terminate()
            self.tcp_process.join()

        if self.udp_process and self.udp_process.is_alive():
            self.udp_process.terminate()
            self.udp_process.join()

        # Rimuovi PID file
        pid_file = self.config['pid_file']
        if os.name == 'nt':
            pid_file = pid_file.replace('/var/run/', './')

        remove_pid_file(pid_file)

        self.logger.info("Daemon terminato")


def load_config(config_file: str) -> Dict[str, Any]:
    """Carica configurazione da file YAML."""
    try:
        with open(config_file, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Errore: file config non trovato: {config_file}")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Errore parsing YAML: {e}")
        sys.exit(1)


def cmd_start(args) -> None:
    """Avvia il daemon."""
    daemon = EchoDaemon(args.config)
    daemon.start()


def cmd_stop(args) -> None:
    """Ferma il daemon in esecuzione."""
    config = load_config(args.config)
    pid_file = config['pid_file']

    if os.name == 'nt':
        pid_file = pid_file.replace('/var/run/', './')

    pid = get_pid_from_file(pid_file)

    if not pid:
        print("Daemon non in esecuzione (nessun PID file)")
        return

    if not is_process_running(pid):
        print(f"Daemon non in esecuzione (PID {pid} non trovato)")
        print(f"Pulisco PID file obsoleto...")
        remove_pid_file(pid_file)
        return

    print(f"Invio SIGTERM al daemon (PID {pid})...")
    try:
        os.kill(pid, signal.SIGTERM)
        print("Daemon fermato")
    except OSError as e:
        print(f"Errore invio segnale: {e}")


def cmd_status(args) -> None:
    """Mostra stato del daemon."""
    config = load_config(args.config)
    pid_file = config['pid_file']

    if os.name == 'nt':
        pid_file = pid_file.replace('/var/run/', './')

    pid = get_pid_from_file(pid_file)

    if not pid:
        print("Status: STOPPED")
        return

    if is_process_running(pid):
        print(f"Status: RUNNING (PID {pid})")
    else:
        print(f"Status: STOPPED (PID file obsoleto)")
        print(f"Pulisco PID file obsoleto...")
        remove_pid_file(pid_file)


def main():
    """Entry point."""
    parser = argparse.ArgumentParser(description="Echo Network Daemon")
    parser.add_argument('--config', '-c',
                       default='config/config.yaml',
                       help='File di configurazione')

    subparsers = parser.add_subparsers(dest='command', help='Comandi')

    # Subcomando start
    parser_start = subparsers.add_parser('start', help='Avvia daemon')
    parser_start.set_defaults(func=cmd_start)

    # Subcomando stop
    parser_stop = subparsers.add_parser('stop', help='Ferma daemon')
    parser_stop.set_defaults(func=cmd_stop)

    # Subcomando status
    parser_status = subparsers.add_parser('status', help='Mostra stato')
    parser_status.set_defaults(func=cmd_status)

    args = parser.parse_args()

    if args.command == 'start':
        cmd_start(args)
    elif args.command == 'stop':
        cmd_stop(args)
    elif args.command == 'status':
        cmd_status(args)
    else:
        # Default: start
        cmd_start(args)


if __name__ == '__main__':
    main()
