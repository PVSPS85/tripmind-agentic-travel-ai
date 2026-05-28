from typing import Any, Dict, Optional
from fastapi import HTTPException, status

class TripMindException(HTTPException):
    """Base Exception wrapper for custom errors across business lines."""
    def __init__(
        self, 
        status_code: int, 
        detail: str, 
        headers: Optional[Dict[str, str]] = None
    ) -> None:
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class AgentExecutionException(TripMindException):
    """Thrown when backend AI Agent pipeline fails or runs out of execution limits."""
    def __init__(self, detail: str = "Agentic pipeline generation failure encountered.") -> None:
        super().__init__(status_code=status.HTTP_502_BAD_GATEWAY, detail=detail)


class ResourceNotFoundException(TripMindException):
    """Thrown when a cached trip ID pattern is missing inside the persistent database layer."""
    def __init__(self, detail: str = "Requested resource sequence not found.") -> None:
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class InvalidFormInputException(TripMindException):
    """Thrown when parsed dynamic constraints violate expected operational guidelines."""
    def __init__(self, detail: str = "Supplied dynamic parameters fail business criteria constraints.") -> None:
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)
