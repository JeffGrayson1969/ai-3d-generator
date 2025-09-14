from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum
import datetime

class ModelType(str, Enum):
    POINT_E = "point-e"
    SHAP_E = "shap-e"
    DEMO = "demo"
    CUSTOM = "custom"

class QualityLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    ULTRA = "ultra"

class OutputFormat(str, Enum):
    STL = "stl"
    OBJ = "obj"
    PLY = "ply"
    GLTF = "gltf"

class GenerationStatus(str, Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

# Request models
class GenerationRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=1000, description="Text description of the 3D model to generate")
    model_type: ModelType = Field(default=ModelType.DEMO, description="AI model to use for generation")
    quality: QualityLevel = Field(default=QualityLevel.MEDIUM, description="Quality level for generation")
    format: OutputFormat = Field(default=OutputFormat.STL, description="Output file format")
    parameters: Optional[Dict[str, Any]] = Field(default=None, description="Additional model-specific parameters")

class OptimizationRequest(BaseModel):
    model_id: str = Field(..., description="ID of the generated model to optimize")
    target_vertices: Optional[int] = Field(default=None, description="Target number of vertices for mesh simplification")
    manifold_repair: bool = Field(default=True, description="Repair non-manifold edges")
    smooth_iterations: int = Field(default=0, ge=0, le=10, description="Number of smoothing iterations")

# Response models
class GenerationResponse(BaseModel):
    id: str = Field(..., description="Unique identifier for the generation job")
    status: GenerationStatus = Field(..., description="Current status of the generation")
    message: str = Field(..., description="Human-readable status message")
    progress: int = Field(default=0, ge=0, le=100, description="Progress percentage (0-100)")
    file_url: Optional[str] = Field(default=None, description="URL to download the generated file")
    thumbnail_url: Optional[str] = Field(default=None, description="URL to the model thumbnail")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata about the generation")
    created_at: Optional[datetime.datetime] = Field(default=None, description="Timestamp when generation was created")
    completed_at: Optional[datetime.datetime] = Field(default=None, description="Timestamp when generation completed")
    error: Optional[str] = Field(default=None, description="Error message if generation failed")

class ModelInfo(BaseModel):
    name: str = Field(..., description="Model name")
    description: str = Field(..., description="Model description")
    available: bool = Field(..., description="Whether the model is currently available")
    version: Optional[str] = Field(default=None, description="Model version")
    parameters: Optional[Dict[str, Any]] = Field(default=None, description="Supported parameters")
    formats: List[OutputFormat] = Field(default=[OutputFormat.STL], description="Supported output formats")

class GalleryItem(BaseModel):
    id: str = Field(..., description="Unique identifier")
    prompt: str = Field(..., description="Original text prompt")
    thumbnail_url: str = Field(..., description="URL to thumbnail image")
    model_url: str = Field(..., description="URL to 3D model file")
    model_type: ModelType = Field(..., description="AI model used for generation")
    created_at: datetime.datetime = Field(..., description="Creation timestamp")
    likes: int = Field(default=0, ge=0, description="Number of likes")
    downloads: int = Field(default=0, ge=0, description="Number of downloads")

class SystemStatus(BaseModel):
    status: str = Field(..., description="Overall system status")
    version: str = Field(..., description="API version")
    models_available: int = Field(..., description="Number of available AI models")
    active_generations: int = Field(..., description="Number of active generation jobs")
    queue_length: int = Field(..., description="Number of queued generation jobs")

# WebSocket message models
class WebSocketMessage(BaseModel):
    type: str = Field(..., description="Message type")
    data: Dict[str, Any] = Field(..., description="Message data")

class GenerationUpdate(BaseModel):
    job_id: str = Field(..., description="Generation job ID")
    status: GenerationStatus = Field(..., description="Current status")
    progress: int = Field(..., ge=0, le=100, description="Progress percentage")
    message: Optional[str] = Field(default=None, description="Status message")
    error: Optional[str] = Field(default=None, description="Error message if applicable")

# Internal models for job management
class GenerationJob(BaseModel):
    id: str
    prompt: str
    model_type: ModelType
    quality: QualityLevel
    format: OutputFormat
    status: GenerationStatus
    progress: int = 0
    created_at: datetime.datetime
    started_at: Optional[datetime.datetime] = None
    completed_at: Optional[datetime.datetime] = None
    file_path: Optional[str] = None
    thumbnail_path: Optional[str] = None
    error: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None