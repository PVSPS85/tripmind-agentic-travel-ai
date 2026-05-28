"""
API v1 Blueprint Package.
Exposes the main unified central router linking to all core functional interfaces.
"""
from app.api.v1.router import api_v1_router

__all__ = ["api_v1_router"]
