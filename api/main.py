from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
import os
from typing import List, Optional
import json
import asyncio
import logging
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.text_to_3d.model_manager import get_model_manager
from core.mesh_processing.mesh_utils import MeshProcessor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI 3D Generator API",
    description="Generate 3D models from text descriptions using AI",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

# Pydantic models
class GenerationRequest(BaseModel):
    prompt: str
    model_type: str = "point-e"
    quality: str = "medium"
    format: str = "stl"

class GenerationResponse(BaseModel):
    id: str
    status: str
    message: str
    file_url: Optional[str] = None
    progress: int = 0

class ModelInfo(BaseModel):
    name: str
    description: str
    available: bool

# In-memory storage for demo (replace with database in production)
generation_jobs = {}

# Health check endpoint
@app.get("/")
async def root():
    return {"message": "AI 3D Generator API is running!", "status": "healthy"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "0.1.0"}

# Model information endpoints
@app.get("/models", response_model=List[ModelInfo])
async def get_available_models():
    """Get list of available AI models for 3D generation"""
    try:
        model_manager = get_model_manager()
        models_data = model_manager.get_available_models()

        models = []
        for model_data in models_data:
            models.append(ModelInfo(
                name=model_data["name"],
                description=model_data["description"],
                available=model_data["available"]
            ))

        return models
    except Exception as e:
        logger.error(f"Failed to get models: {e}")
        # Fallback to basic model info
        return [
            ModelInfo(
                name="demo",
                description="Demo model that generates simple geometric shapes",
                available=True
            )
        ]

# 3D generation endpoints
@app.post("/generate", response_model=GenerationResponse)
async def generate_3d_model(request: GenerationRequest):
    """Generate a 3D model from text description"""
    import uuid

    job_id = str(uuid.uuid4())

    # Validate model type
    if request.model_type not in ["point-e", "shap-e", "demo"]:
        raise HTTPException(status_code=400, detail="Invalid model type")

    # Store generation job
    generation_jobs[job_id] = {
        "id": job_id,
        "prompt": request.prompt,
        "model_type": request.model_type,
        "status": "queued",
        "progress": 0,
        "created_at": "2024-01-01T00:00:00Z"  # Replace with actual timestamp
    }

    # Start async generation (placeholder)
    asyncio.create_task(process_generation(job_id, request))

    return GenerationResponse(
        id=job_id,
        status="queued",
        message=f"3D generation started for: {request.prompt}",
        progress=0
    )

async def process_generation(job_id: str, request: GenerationRequest):
    """Process the 3D generation (placeholder implementation)"""
    try:
        # Update status to processing
        generation_jobs[job_id]["status"] = "processing"
        await manager.broadcast(json.dumps({
            "job_id": job_id,
            "status": "processing",
            "progress": 10
        }))

        # Simulate processing time
        for progress in [25, 50, 75, 90]:
            await asyncio.sleep(1)
            generation_jobs[job_id]["progress"] = progress
            await manager.broadcast(json.dumps({
                "job_id": job_id,
                "status": "processing",
                "progress": progress
            }))

        # Generate 3D model using AI
        try:
            output_file = await create_ai_generated_model(
                request.prompt,
                job_id,
                request.model_type,
                request.format
            )

            generation_jobs[job_id].update({
                "status": "completed",
                "progress": 100,
                "file_path": output_file
            })

            await manager.broadcast(json.dumps({
                "job_id": job_id,
                "status": "completed",
                "progress": 100,
                "message": f"Generated 3D model for: {request.prompt}"
            }))

        except Exception as model_error:
            logger.error(f"Model generation failed for {job_id}: {model_error}")
            generation_jobs[job_id].update({
                "status": "failed",
                "progress": 0,
                "error": str(model_error)
            })

            await manager.broadcast(json.dumps({
                "job_id": job_id,
                "status": "failed",
                "progress": 0,
                "message": f"Generation failed: {str(model_error)}"
            }))

    except Exception as e:
        generation_jobs[job_id].update({
            "status": "failed",
            "progress": 0,
            "error": str(e)
        })

        await manager.broadcast(json.dumps({
            "job_id": job_id,
            "status": "failed",
            "progress": 0,
            "message": f"Generation failed: {str(e)}"
        }))

async def create_ai_generated_model(prompt: str, job_id: str, model_type: str, format: str = "stl") -> str:
    """Generate 3D model using AI and save to file"""
    try:
        # Create output directory
        output_dir = "generated_models"
        os.makedirs(output_dir, exist_ok=True)

        # Get model manager and generate 3D model
        model_manager = get_model_manager()
        logger.info(f"Generating 3D model with {model_type}: {prompt}")

        # Generate 3D geometry
        result = model_manager.generate_3d(model_type, prompt)

        # Extract geometry data
        vertices = result["vertices"]
        faces = result["faces"]
        metadata = result.get("metadata", {})

        # Validate and process mesh
        validation = MeshProcessor.validate_mesh(vertices, faces)
        if not validation["is_valid"]:
            logger.warning(f"Mesh validation issues: {validation['errors']}")

        # Create STL mesh
        stl_mesh = MeshProcessor.create_mesh_from_arrays(vertices, faces)

        # Save to file
        output_file = f"{output_dir}/{job_id}_{model_type}_{metadata.get('shape_type', 'model')}.{format}"
        success = MeshProcessor.save_mesh(stl_mesh, output_file, format)

        if not success:
            raise Exception(f"Failed to save mesh to {output_file}")

        logger.info(f"Successfully generated 3D model: {output_file}")
        logger.info(f"Model stats: {validation['stats']}")

        return output_file

    except Exception as e:
        logger.error(f"AI model generation failed: {e}")
        raise

@app.get("/generate/{job_id}")
async def get_generation_status(job_id: str):
    """Get status of a 3D generation job"""
    if job_id not in generation_jobs:
        raise HTTPException(status_code=404, detail="Generation job not found")

    job = generation_jobs[job_id]
    return GenerationResponse(
        id=job_id,
        status=job["status"],
        message=f"Generation status: {job['status']}",
        progress=job["progress"],
        file_url=f"/download/{job_id}" if job.get("file_path") else None
    )

@app.get("/download/{job_id}")
async def download_generated_model(job_id: str):
    """Download generated 3D model file"""
    if job_id not in generation_jobs:
        raise HTTPException(status_code=404, detail="Generation job not found")

    job = generation_jobs[job_id]
    if job["status"] != "completed" or "file_path" not in job:
        raise HTTPException(status_code=400, detail="Model not ready for download")

    from fastapi.responses import FileResponse
    file_path = job["file_path"]

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Generated file not found")

    return FileResponse(
        path=file_path,
        filename=f"generated_model_{job_id}.stl",
        media_type="application/octet-stream"
    )

# WebSocket endpoint for real-time updates
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive and handle any client messages
            data = await websocket.receive_text()
            # Echo received message (can be extended for client commands)
            await manager.send_personal_message(f"Received: {data}", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Gallery endpoints (placeholder)
@app.get("/gallery")
async def get_gallery():
    """Get gallery of example 3D generations"""
    return {
        "examples": [
            {
                "id": "example_1",
                "prompt": "A small red cube",
                "thumbnail": "/static/thumbnails/cube.jpg",
                "model_url": "/static/models/cube.stl"
            },
            {
                "id": "example_2",
                "prompt": "A blue sphere",
                "thumbnail": "/static/thumbnails/sphere.jpg",
                "model_url": "/static/models/sphere.stl"
            }
        ]
    }

# Mount static files (for serving generated models and assets)
os.makedirs("generated_models", exist_ok=True)
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/generated", StaticFiles(directory="generated_models"), name="generated")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )