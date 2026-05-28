from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.config import settings
from app.core.exceptions import TripMindException
from app.api.v1.router import api_v1_router

# Initialize standard high-performance production FastAPI app wrapper configuration
app = FastAPI(
    title=settings.APP_NAME,
    description="Multi-Agent Premium Group Travel Orchestration Engine running CrewAI and Groq APIs.",
    version="1.0.0",
    debug=settings.DEBUG
)

# Apply restrictive/flexible routing CORS configurations mapping across trusted design assets
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin).rstrip("/") for origin in settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers mapping internal custom pipeline blocks directly to clean system outputs
@app.exception_handler(TripMindException)
async def tripmind_exception_handler(request: Request, exc: TripMindException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "error": exc.detail}
    )

@app.exception_handler(Exception)
async def global_fallback_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    # Captures unpredictable baseline trace errors preventing structure breaks
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"success": False, "error": "An unexpected server execution anomaly occurred." if not settings.DEBUG else str(exc)}
    )

@app.get("/health", tags=["System Maintenance"], status_code=status.HTTP_200_OK)
async def system_health_status_check() -> dict:
    """Core health check route supporting verification checks."""
    return {
        "status": "operational",
        "service": settings.APP_NAME,
        "environment": settings.ENVIRONMENT
    }

# Register v1 API routes
app.include_router(api_v1_router, prefix=settings.API_V1_STR)

