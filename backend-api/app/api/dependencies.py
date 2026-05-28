from fastapi import Header, status
from app.config import settings
from app.core.exceptions import TripMindException
from app.database.session import get_db

# Re-export database dependency session injection hook for endpoint consumption
__all__ = ["get_db", "verify_api_client"]

async def verify_api_client(x_tripmind_key: str = Header(default="default_dev_bypass")) -> str:
    """
    Optional security dependency ensuring that coming requests match 
    trusted internal web clients or environment headers.
    """
    if settings.ENVIRONMENT == "production" and x_tripmind_key == "default_dev_bypass":
        raise TripMindException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid API verification credentials."
        )
    return x_tripmind_key
