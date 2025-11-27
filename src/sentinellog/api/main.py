from fastapi import FastAPI
from fastapi.responses import JSONResponse
from sentinellog.api.routes.scan_routes import router as scan_router

app = FastAPI(
    title="SentinelLog API",
    version="1.0.0",
    description="Lightweight log threat detection API for security threat detection and analysis"
)

app.include_router(scan_router, prefix="/api/v1")


@app.get("/health")
def health_check():
    """Health check endpoint for load balancers and orchestrators."""
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "service": "sentinellog",
            "version": "1.0.0"
        }
    )


@app.get("/")
def root():
    """Root endpoint with API metadata and documentation link."""
    return JSONResponse(
        status_code=200,
        content={
            "service": "SentinelLog API",
            "version": "1.0.0",
            "description": "Security threat detection engine for log files",
            "endpoints": {
                "health": "/health",
                "docs": "/docs",
                "openapi_schema": "/openapi.json",
                "scan": "/api/v1/scan",
                "rules_reload": "/api/v1/rules/reload",
                "rules_list": "/api/v1/rules/list"
            }
        }
    )


@app.get("/api/v1/info")
def api_info():
    """API info and capabilities."""
    return JSONResponse(
        status_code=200,
        content={
            "service_name": "SentinelLog",
            "api_version": "1.0.0",
            "capabilities": [
                "log_scanning",
                "threat_detection",
                "rule_management",
                "dynamic_rule_loading"
            ],
            "endpoints": [
                {"path": "/api/v1/scan", "method": "POST", "description": "Scan logs for threats"},
                {"path": "/api/v1/rules/reload", "method": "POST", "description": "Reload rules from disk"},
                {"path": "/api/v1/rules/list", "method": "GET", "description": "List active rules"}
            ]
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("sentinellog.api.main:app", host="0.0.0.0", port=8000, reload=True)