from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import os
import uuid

# ---------------------------------------------------------------
# FastAPI Application Instance
# ---------------------------------------------------------------
app = FastAPI(
    title="GC Render-Core API",
    description="API for Grok's image/video rendering and heavy execution tasks.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# ---------------------------------------------------------------
# Root Endpoint for Render health check
# ---------------------------------------------------------------
@app.get("/", summary="Root endpoint health check")
async def read_root():
    """
    Simple root endpoint to confirm API is running.
    Render.com health checks often hit the root URL.
    """
    return {"message": "GC Render-Core API is active"}

# ---------------------------------------------------------------
# Pydantic Models
# ---------------------------------------------------------------
class RenderImageRequest(BaseModel):
    prompt: str
    style: str = "photorealistic"
    resolution: str = "1024x1024"
    num_images: int = 1
    output_format: str = "png"

class RenderImageResponse(BaseModel):
    job_id: str
    status: str   # pending, processing, completed, failed
    output_paths: list[str] = []
    error_message: str | None = None

class StatusResponse(BaseModel):
    status: str = "online"
    message: str = "GC Render-Core is operational and ready to receive tasks."
    version: str = "1.0.0"
    uptime: str = "Not tracked yet"

# ---------------------------------------------------------------
# API Endpoints
# ---------------------------------------------------------------
@app.get("/status", response_model=StatusResponse, summary="Check API status")
async def get_status():
    return StatusResponse()

@app.post("/render-image", response_model=RenderImageResponse, summary="Request an image rendering task")
async def render_image(request: RenderImageRequest):
    simulated_job_id = f"render_job_{uuid.uuid4().hex}"
    print(f"Received render request for prompt '{request.prompt}' -> Job ID: {simulated_job_id}")
    return RenderImageResponse(
        job_id=simulated_job_id,
        status="pending",
        output_paths=[],
        error_message=None
    )

# ---------------------------------------------------------------
# Local Development (ignored in Docker)
# ---------------------------------------------------------------
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
