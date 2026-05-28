import secrets
from typing import Optional
from hmac import compare_digest

class SecurityManager:
    """
    Provides standard cryptographic validation helpers for API endpoints 
    and multi-tenant verification checks.
    """
    @staticmethod
    def generate_secure_token() -> str:
        return secrets.token_urlsafe(32)

    @staticmethod
    def verify_static_key(provided_key: str, expected_key: str) -> bool:
        return compare_digest(provided_key, expected_key)
