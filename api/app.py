from fastapi import FastAPI

app = FastAPI(
    title="EduPulse AI — Enterprise Multi-Agent Governance API",
    description="Enterprise Distributed Multi-Agent Governance & Crisis Intervention Platform Backend",
    version="0.1.0",
)


@app.get("/")
def read_root():
    """
    Root endpoint serving application metadata and health status.
    Prevents 404 Not Found responses on cloud web service home route.
    """
    return {
        "system": "EduPulse AI",
        "status": "ONLINE",
        "version": "0.1.0",
        "documentation": "/docs",
        "health_check": "/health",
        "message": "Welcome to EduPulse AI Enterprise Backend API",
    }


@app.get("/health")
def health():
    """Health check endpoint for Render cloud service and container orchestration."""
    return {"status": "HEALTHY"}
