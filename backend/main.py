from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import uvicorn
import os
from dotenv import load_dotenv

from .database import engine, Base
from .models import credit_models, user_models
from .routers import credit, users, simulation, recommendations
from .services.ai_models import CreditScoringModel
from .utils.logger import setup_logger

# Load environment variables
load_dotenv()

# Setup logger
logger = setup_logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting AI Credit Assessment Platform...")
    
    # Create database tables
    Base.metadata.create_all(bind=engine)
    
    # Initialize AI models
    try:
        credit_model = CreditScoringModel()
        credit_model.load_models()
        logger.info("AI models loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load AI models: {e}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down AI Credit Assessment Platform...")

# Create FastAPI app
app = FastAPI(
    title="AI Credit Assessment Platform",
    description="Next-generation credit assessment that goes beyond traditional scoring",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(credit.router, prefix="/api/v1/credit", tags=["Credit Assessment"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(simulation.router, prefix="/api/v1/simulation", tags=["Simulation"])
app.include_router(recommendations.router, prefix="/api/v1/recommendations", tags=["Recommendations"])

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "AI Credit Assessment Platform"}

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "AI Credit Assessment Platform API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
