#!/usr/bin/env python3
"""
Test Client per Echo Daemon
============================
Client per testare i server TCP e UDP.

Funzionalità:
- Test TCP echo client
- Test UDP echo client
- Test multiple clients
- Test timeout
- Test payload grandi

Uso:
    python tests/client.py --protocol tcp
    python tests/client.py --protocol udp
    python tests/client.py --count 5
"""

import socket
import argparse
import time
import sys
from pathlib import Path

# Add parent directory to path
SCRIPT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(SCRIPT_DIR))

import yaml


def load_config(config_file: str = 'config/config.yaml') -> dict:
    """Carica configurazione."""
    with open(config_file, 'r') as f:
        return yaml.safe_load(f)


class EchoClient:
    """Client generico per echo server."""

    def __init__(self, host: str, port: int, protocol: str = 'tcp'):
        self.host = host
        self.port = port
        self.protocol = protocol.lower()

    def test_echo(self, message: str) -> bool:
        """
        Invia messaggio e verifica echo response.

        Args:
            message: Messaggio da inviare

        Returns:
            True se echo corretto, False altrimenti
        """
        if self.protocol == 'tcp':
            return self._test_tcp(message)
        else:
            return self._test_udp(message)

    def _test_tcp(self, message: str) -> bool:
        """Test TCP echo."""
        try:
            # Crea socket TCP
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5.0)

            # Connect al server
            sock.connect((self.host, self.port))

            print(f"[TCP] Connesso a {self.host}:{self.port}")

            # Invia dati
            sock.sendall(message.encode())

            # Ricevi response
            response = sock.recv(4096)

            sock.close()

            # Verifica
            if response.decode() == message:
                print(f"[TCP] Echo OK: '{message}'")
                return True
            else:
                print(f"[TCP] Echo FAIL: atteso '{message}', ricevuto '{response.decode()}'")
                return False

        except Exception as e:
            print(f"[TCP] Errore: {e}")
            return False

    def _test_udp(self, message: str) -> bool:
        """Test UDP echo."""
        try:
            # Crea socket UDP
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(5.0)

            # Invia datagram
            sock.sendto(message.encode(), (self.host, self.port))

            print(f"[UDP] Inviato a {self.host}:{self.port}")

            # Ricevi response
            response, addr = sock.recvfrom(4096)

            sock.close()

            # Verifica
            if response.decode() == message:
                print(f"[UDP] Echo OK: '{message}'")
                return True
            else:
                print(f"[UDP] Echo FAIL: atteso '{message}', ricevuto '{response.decode()}'")
                return False

        except Exception as e:
            print(f"[UDP] Errore: {e}")
            return False

    def test_multiple_messages(self, count: int = 5) -> bool:
        """Test con multiple messaggi sequenziali."""
        print(f"\n--- Test {count} messaggi ---")

        all_ok = True
        for i in range(count):
            message = f"Message {i+1}"
            if not self.test_echo(message):
                all_ok = False

        return all_ok

    def test_large_payload(self, size: int = 8192) -> bool:
        """Test con payload grande."""
        print(f"\n--- Test payload grande ({size} bytes) ---")

        # Crea payload ripetuto
        message = "A" * size
        return self.test_echo(f"LARGE:{message}")

    def test_continuous(self, duration: int = 10) -> None:
        """Test continuo per N secondi."""
        print(f"\n--- Test continuo per {duration} secondi ---")

        start_time = time.time()
        count = 0

        while time.time() - start_time < duration:
            message = f"Ping {count}"
            self.test_echo(message)
            count += 1
            time.sleep(0.5)

        print(f"Completati {count} messaggi in {duration} secondi")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Echo Test Client")
    parser.add_argument('--host', '-H', default='localhost',
                       help='Server host')
    parser.add_argument('--port', '-p', type=int,
                       help='Server port (default: from config)')
    parser.add_argument('--protocol', '-P', choices=['tcp', 'udp'],
                       default='tcp', help='Protocol (default: tcp)')
    parser.add_argument('--config', '-c', default='config/config.yaml',
                       help='Config file path')
    parser.add_argument('--message', '-m', default='Hello, Echo!',
                       help='Message to send')
    parser.add_argument('--count', '-n', type=int, default=5,
                       help='Number of messages')
    parser.add_argument('--large', action='store_true',
                       help='Test large payload')
    parser.add_argument('--continuous', type=int, metavar='SECONDS',
                       help='Continuous test for N seconds')
    parser.add_argument('--all', action='store_true',
                       help='Run all tests')

    args = parser.parse_args()

    # Load config for default port
    config = load_config(args.config)

    if args.port is None:
        if args.protocol == 'tcp':
            args.port = config['port']
        else:
            args.port = config['udp_port']

    print("=" * 50)
    print(f"Echo Test Client - {args.protocol.upper()}")
    print("=" * 50)
    print(f"Server: {args.host}:{args.port}")

    # Create client
    client = EchoClient(args.host, args.port, args.protocol)

    # Run tests
    if args.all:
        print("\nRunning ALL tests...")

        # Test singolo messaggio
        client.test_echo(args.message)

        # Test multipli
        client.test_multiple_messages(args.count)

        # Test payload grande
        if args.protocol == 'tcp':
            client.test_large_payload()

        # Test continuo
        if args.protocol == 'tcp':
            client.test_continuous(5)

        print("\n" + "=" * 50)
        print("Tutti i test completati!")

    elif args.continuous:
        client.test_continuous(args.continuous)

    elif args.large:
        client.test_large_payload()

    else:
        # Test singolo o multiplo
        if args.count > 1:
            client.test_multiple_messages(args.count)
        else:
            client.test_echo(args.message)


if __name__ == '__main__':
    main()
