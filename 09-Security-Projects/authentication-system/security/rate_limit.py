"""
Rate Limiting per prevenire brute force attacks
Implementa limiting su IP e endpoint
"""

from functools import wraps
from flask import request, jsonify, g
from collections import defaultdict
import time

# ============================================================================
# IN-MEMORY RATE LIMITER (per sviluppo)
# ============================================================================

class RateLimiter:
    """
    Rate limiter in-memory.

    IMPORTANZA DEL RATE LIMITING:
    - Previene brute force attacks su login
    - Protegge da DOS attacks
    - Limita l'uso intensivo delle API
    - Dovrebbe essere implementato con Redis in produzione

    Per produzione, usare:
    - Flask-Limiter con Redis
    - Redis con expired keys
    - Nginx rate limiting
    """

    def __init__(self):
        # {endpoint: {ip: [(timestamp, count), ...]}}
        self.requests = defaultdict(lambda: defaultdict(list))
        self.blocked_ips = {}  # {ip: unblock_timestamp}

    def is_allowed(
        self,
        endpoint: str,
        ip: str,
        limit: int,
        period: int
    ) -> tuple:
        """
        Verifica se una richiesta è permessa.

        STRATEGIE:
        1. Fixed Window: contatore che reset ogni periodo
        2. Sliding Window Log: rimuovi richieste vecchie
        3. Token Bucket: permette burst
        4. Leaky Bucket: rate costante

        Qui usiamo Sliding Window Log.

        Args:
            endpoint: Nome endpoint
            ip: IP address
            limit: Max richieste
            period: Periodo in secondi

        Returns:
            Tuple (allowed, retry_after)
        """
        # Verifica se IP è bloccato
        if ip in self.blocked_ips:
            unblock_time = self.blocked_ips[ip]
            if time.time() < unblock_time:
                retry_after = int(unblock_time - time.time())
                return False, retry_after
            else:
                del self.blocked_ips[ip]

        # Ottieni timestamp corrente
        now = time.time()
        window_start = now - period

        # Rimuovi richieste vecchie
        self.requests[endpoint][ip] = [
            (ts, count) for ts, count in self.requests[endpoint][ip]
            if ts > window_start
        ]

        # Conta richieste nella finestra
        total_requests = sum(count for _, count in self.requests[endpoint][ip])

        if total_requests >= limit:
            # Blocca IP temporaneamente
            self.blocked_ips[ip] = now + period
            retry_after = period
            return False, retry_after

        # Registra richiesta
        self.requests[endpoint][ip].append((now, 1))

        return True, 0

    def reset(self, endpoint: str = None, ip: str = None):
        """Resetta il rate limiter"""
        if endpoint and ip:
            if endpoint in self.requests:
                if ip in self.requests[endpoint]:
                    del self.requests[endpoint][ip]
        elif endpoint:
            if endpoint in self.requests:
                del self.requests[endpoint]
        elif ip:
            for endpoint_requests in self.requests.values():
                if ip in endpoint_requests:
                    del endpoint_requests[ip]
        else:
            self.requests.clear()


# Istanza globale del rate limiter
rate_limiter = RateLimiter()


def rate_limit(endpoint: str, limit: int, period: int):
    """
    Decorator per il rate limiting.

    USAGE:
        @rate_limit('login', limit=5, period=60)  # 5 richieste/minuto
        def login():
            ...

    BEST PRACTICES:
    - Login: 5-10 tentativi per 5-15 minuti
    - Registrazione: 3-5 per ora
    - Reset password: 3 per ora
    - API generali: 100-1000 per ora

    Args:
        endpoint: Nome endpoint per identificare
        limit: Massimo numero di richieste
        period: Periodo in secondi

    Returns:
        Decorator function
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Ottieni IP
            ip = request.remote_addr

            # Verifica rate limit
            allowed, retry_after = rate_limiter.is_allowed(
                endpoint=endpoint,
                ip=ip,
                limit=limit,
                period=period
            )

            if not allowed:
                # Log del rate limit
                g.rate_limited = True

                return jsonify({
                    'error': 'Troppe richieste. Riprova tra poco.',
                    'retry_after': retry_after
                }), 429

            return f(*args, **kwargs)

        return decorated_function

    return decorator


# ============================================================================
# RATE LIMITING CONFIGURAZIONE
# ============================================================================

RATE_LIMITS = {
    'login': {'limit': 5, 'period': 300},      # 5 tentativi / 5 minuti
    'register': {'limit': 5, 'period': 3600},  # 5 registrazioni / ora
    'password_reset': {'limit': 3, 'period': 3600},  # 3 richieste / ora
    '2fa': {'limit': 10, 'period': 300},      # 10 tentativi / 5 minuti
    'api': {'limit': 100, 'period': 3600},     # 100 richieste / ora
}


def get_rate_limit_config(endpoint: str) -> dict:
    """
    Ottieni la configurazione del rate limit per un endpoint.

    Args:
        endpoint: Nome dell'endpoint

    Returns:
        Dict con limit e period
    """
    return RATE_LIMITS.get(endpoint, {'limit': 100, 'period': 3600})


# ============================================================================
# RATE LIMITING CON REDIS (per produzione)
# ============================================================================

class RedisRateLimiter:
    """
    Rate limiter usando Redis.

    VANTAGGI:
    - Condivide lo stato tra più server
    - Persistenza
    - Performance migliori
    - Atomic operations

    Richiede redis-py: pip install redis
    """

    def __init__(self, redis_client):
        """
        Inizializza il rate limiter Redis.

        Args:
            redis_client: Istanza di Redis client
        """
        self.redis = redis_client

    def is_allowed(
        self,
        key: str,
        limit: int,
        period: int
    ) -> tuple:
        """
        Verifica se una richiesta è permessa usando Redis.

        Usa Redis INCR con expiration per implementare
        un rate limiting sliding window.

        Args:
            key: Chiave univoca (es: "login:192.168.1.1")
            limit: Max richieste
            period: Periodo in secondi

        Returns:
            Tuple (allowed, retry_after)
        """
        pipeline = self.redis.pipeline()

        # Incrementa contatore
        pipeline.incr(key)
        # Imposta expiration se nuova chiave
        pipeline.expire(key, period)

        results = pipeline.execute()
        current = results[0]

        if current > limit:
            # Calcola retry_after
            ttl = self.redis.ttl(key)
            return False, ttl

        return True, 0

    def reset(self, key: str):
        """Resetta il contatore per una chiave"""
        self.redis.delete(key)
