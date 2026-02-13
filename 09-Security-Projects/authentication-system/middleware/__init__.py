"""
Middleware di sicurezza per Flask
"""
from .security_headers import init_security_headers

__all__ = ['init_security_headers']
