import os
import uuid
import hashlib
import asyncio
from typing import Optional, Dict, Any, List
from pathlib import Path
import numpy as np
from stl import mesh
import trimesh
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FileManager:
    """Utility class for managing generated files and directories"""

    def __init__(self, base_dir: str = "generated_models"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)

        # Create subdirectories
        (self.base_dir / "models").mkdir(exist_ok=True)
        (self.base_dir / "thumbnails").mkdir(exist_ok=True)
        (self.base_dir / "temp").mkdir(exist_ok=True)

    def generate_unique_filename(self, extension: str = "stl") -> str:
        """Generate a unique filename with timestamp and UUID"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        return f"{timestamp}_{unique_id}.{extension}"

    def get_model_path(self, filename: str) -> Path:
        """Get full path for a model file"""
        return self.base_dir / "models" / filename

    def get_thumbnail_path(self, filename: str) -> Path:
        """Get full path for a thumbnail file"""
        return self.base_dir / "thumbnails" / filename

    def cleanup_temp_files(self, older_than_hours: int = 24):
        """Clean up temporary files older than specified hours"""
        import time
        cutoff_time = time.time() - (older_than_hours * 3600)
        temp_dir = self.base_dir / "temp"

        for file_path in temp_dir.glob("*"):
            if file_path.stat().st_mtime < cutoff_time:
                try:
                    file_path.unlink()
                    logger.info(f"Cleaned up temp file: {file_path}")
                except Exception as e:
                    logger.error(f"Failed to cleanup {file_path}: {e}")

class MeshProcessor:
    """Utility class for 3D mesh processing operations"""

    @staticmethod
    def create_cube(size: float = 1.0) -> mesh.Mesh:
        """Create a simple cube mesh"""
        vertices = np.array([
            [0, 0, 0], [size, 0, 0], [size, size, 0], [0, size, 0],  # bottom
            [0, 0, size], [size, 0, size], [size, size, size], [0, size, size]  # top
        ])

        faces = np.array([
            [0, 1, 2], [0, 2, 3],  # bottom
            [4, 7, 6], [4, 6, 5],  # top
            [0, 4, 5], [0, 5, 1],  # front
            [2, 6, 7], [2, 7, 3],  # back
            [0, 3, 7], [0, 7, 4],  # left
            [1, 5, 6], [1, 6, 2]   # right
        ])

        cube_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
        for i, face in enumerate(faces):
            for j in range(3):
                cube_mesh.vectors[i][j] = vertices[face[j]]

        return cube_mesh

    @staticmethod
    def create_sphere(radius: float = 1.0, resolution: int = 20) -> mesh.Mesh:
        """Create a sphere mesh using trimesh"""
        try:
            sphere = trimesh.creation.icosphere(subdivisions=2, radius=radius)
            return mesh.Mesh(sphere.triangles)
        except Exception as e:
            logger.error(f"Failed to create sphere: {e}")
            # Fallback to cube if sphere creation fails
            return MeshProcessor.create_cube(size=radius * 2)

    @staticmethod
    def create_cylinder(radius: float = 1.0, height: float = 2.0, segments: int = 20) -> mesh.Mesh:
        """Create a cylinder mesh"""
        try:
            cylinder = trimesh.creation.cylinder(radius=radius, height=height, sections=segments)
            return mesh.Mesh(cylinder.triangles)
        except Exception as e:
            logger.error(f"Failed to create cylinder: {e}")
            return MeshProcessor.create_cube(size=radius * 2)

    @staticmethod
    def validate_mesh(mesh_obj: mesh.Mesh) -> Dict[str, Any]:
        """Validate mesh properties for 3D printing"""
        validation_result = {
            "is_manifold": True,
            "is_watertight": True,
            "volume": 0.0,
            "surface_area": 0.0,
            "errors": []
        }

        try:
            # Convert to trimesh for analysis
            tm = trimesh.Trimesh(vertices=mesh_obj.vectors.reshape(-1, 3)[::3],
                               faces=np.arange(len(mesh_obj.vectors)).reshape(-1, 3))

            validation_result["is_manifold"] = tm.is_manifold
            validation_result["is_watertight"] = tm.is_watertight
            validation_result["volume"] = float(tm.volume) if tm.is_watertight else 0.0
            validation_result["surface_area"] = float(tm.area)

            if not tm.is_manifold:
                validation_result["errors"].append("Mesh is not manifold")
            if not tm.is_watertight:
                validation_result["errors"].append("Mesh is not watertight")

        except Exception as e:
            validation_result["errors"].append(f"Validation error: {str(e)}")
            logger.error(f"Mesh validation failed: {e}")

        return validation_result

    @staticmethod
    def optimize_mesh(input_path: str, output_path: str, target_vertices: Optional[int] = None) -> bool:
        """Optimize mesh for 3D printing (placeholder implementation)"""
        try:
            # Load mesh
            original_mesh = mesh.Mesh.from_file(input_path)

            # For now, just copy the mesh (mesh optimization would require more advanced libraries)
            # In a full implementation, you would use libraries like PyMeshLab or Open3D
            original_mesh.save(output_path)

            logger.info(f"Mesh optimization completed: {input_path} -> {output_path}")
            return True

        except Exception as e:
            logger.error(f"Mesh optimization failed: {e}")
            return False

class PromptProcessor:
    """Utility class for processing and analyzing text prompts"""

    @staticmethod
    def clean_prompt(prompt: str) -> str:
        """Clean and normalize text prompt"""
        # Remove extra whitespace
        cleaned = " ".join(prompt.split())

        # Basic filtering for inappropriate content (placeholder)
        inappropriate_words = ["explicit", "inappropriate"]  # Add more as needed
        for word in inappropriate_words:
            if word.lower() in cleaned.lower():
                raise ValueError(f"Inappropriate content detected: {word}")

        return cleaned

    @staticmethod
    def extract_shape_hints(prompt: str) -> Dict[str, Any]:
        """Extract shape hints from text prompt for demo generation"""
        prompt_lower = prompt.lower()

        # Simple keyword matching for demo purposes
        shape_hints = {
            "primary_shape": "cube",  # default
            "size": 1.0,
            "color": "default"
        }

        if any(word in prompt_lower for word in ["sphere", "ball", "round"]):
            shape_hints["primary_shape"] = "sphere"
        elif any(word in prompt_lower for word in ["cylinder", "tube", "pipe"]):
            shape_hints["primary_shape"] = "cylinder"
        elif any(word in prompt_lower for word in ["cube", "box", "square"]):
            shape_hints["primary_shape"] = "cube"

        # Extract size hints
        if any(word in prompt_lower for word in ["small", "tiny", "mini"]):
            shape_hints["size"] = 0.5
        elif any(word in prompt_lower for word in ["large", "big", "huge"]):
            shape_hints["size"] = 2.0

        return shape_hints

    @staticmethod
    def generate_hash(prompt: str) -> str:
        """Generate a hash for prompt-based caching"""
        return hashlib.md5(prompt.encode()).hexdigest()

class AsyncJobManager:
    """Utility class for managing asynchronous generation jobs"""

    def __init__(self):
        self.active_jobs: Dict[str, asyncio.Task] = {}
        self.job_queue: List[str] = []

    def add_job(self, job_id: str, task: asyncio.Task):
        """Add a new job to the manager"""
        self.active_jobs[job_id] = task
        logger.info(f"Added job {job_id} to active jobs")

    def remove_job(self, job_id: str):
        """Remove a completed job from the manager"""
        if job_id in self.active_jobs:
            del self.active_jobs[job_id]
            logger.info(f"Removed job {job_id} from active jobs")

    def cancel_job(self, job_id: str) -> bool:
        """Cancel a running job"""
        if job_id in self.active_jobs:
            task = self.active_jobs[job_id]
            task.cancel()
            self.remove_job(job_id)
            logger.info(f"Cancelled job {job_id}")
            return True
        return False

    def get_job_count(self) -> int:
        """Get the number of active jobs"""
        return len(self.active_jobs)

    def get_queue_length(self) -> int:
        """Get the length of the job queue"""
        return len(self.job_queue)

# Global instances
file_manager = FileManager()
job_manager = AsyncJobManager()

def create_demo_model(prompt: str, job_id: str) -> str:
    """Create a demo 3D model based on prompt analysis"""
    try:
        # Process prompt to determine shape
        shape_hints = PromptProcessor.extract_shape_hints(prompt)

        # Generate appropriate mesh
        if shape_hints["primary_shape"] == "sphere":
            model_mesh = MeshProcessor.create_sphere(radius=shape_hints["size"])
        elif shape_hints["primary_shape"] == "cylinder":
            model_mesh = MeshProcessor.create_cylinder(radius=shape_hints["size"], height=shape_hints["size"] * 2)
        else:
            model_mesh = MeshProcessor.create_cube(size=shape_hints["size"])

        # Save model
        filename = file_manager.generate_unique_filename("stl")
        output_path = file_manager.get_model_path(filename)
        model_mesh.save(str(output_path))

        logger.info(f"Created demo model for prompt '{prompt}': {output_path}")
        return str(output_path)

    except Exception as e:
        logger.error(f"Failed to create demo model: {e}")
        raise

def get_system_stats() -> Dict[str, Any]:
    """Get current system statistics"""
    return {
        "active_jobs": job_manager.get_job_count(),
        "queue_length": job_manager.get_queue_length(),
        "disk_usage": get_disk_usage(),
        "generated_models_count": count_generated_models()
    }

def get_disk_usage() -> Dict[str, float]:
    """Get disk usage statistics"""
    try:
        import shutil
        total, used, free = shutil.disk_usage(file_manager.base_dir)
        return {
            "total_gb": total / (1024**3),
            "used_gb": used / (1024**3),
            "free_gb": free / (1024**3)
        }
    except Exception as e:
        logger.error(f"Failed to get disk usage: {e}")
        return {"total_gb": 0, "used_gb": 0, "free_gb": 0}

def count_generated_models() -> int:
    """Count the number of generated model files"""
    try:
        models_dir = file_manager.base_dir / "models"
        return len(list(models_dir.glob("*.stl"))) + len(list(models_dir.glob("*.obj")))
    except Exception as e:
        logger.error(f"Failed to count models: {e}")
        return 0