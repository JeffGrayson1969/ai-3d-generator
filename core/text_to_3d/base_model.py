from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
import numpy as np
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class BaseText3DModel(ABC):
    """Abstract base class for text-to-3D generation models"""

    def __init__(self, model_name: str, model_path: Optional[str] = None):
        self.model_name = model_name
        self.model_path = model_path
        self.is_loaded = False
        self.model = None
        self.device = "cpu"  # Default to CPU

    @abstractmethod
    def load_model(self) -> bool:
        """Load the AI model into memory"""
        pass

    @abstractmethod
    def generate_3d(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """
        Generate 3D model from text prompt

        Args:
            prompt: Text description of the 3D model
            **kwargs: Additional generation parameters

        Returns:
            Dict containing generated data (vertices, faces, metadata)
        """
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Check if the model is available and can be used"""
        pass

    def preprocess_prompt(self, prompt: str) -> str:
        """Preprocess the text prompt before generation"""
        # Basic cleaning
        cleaned_prompt = prompt.strip().lower()

        # Remove excessive whitespace
        cleaned_prompt = " ".join(cleaned_prompt.split())

        # Basic content filtering (extend as needed)
        banned_words = ["explicit", "inappropriate", "nsfw"]
        for word in banned_words:
            if word in cleaned_prompt:
                raise ValueError(f"Inappropriate content detected: {word}")

        return cleaned_prompt

    def postprocess_geometry(self, vertices: np.ndarray, faces: np.ndarray) -> Dict[str, Any]:
        """Postprocess generated geometry"""
        try:
            # Ensure proper shape
            if vertices.ndim != 2 or vertices.shape[1] != 3:
                raise ValueError(f"Invalid vertices shape: {vertices.shape}")

            if faces.ndim != 2 or faces.shape[1] != 3:
                raise ValueError(f"Invalid faces shape: {faces.shape}")

            # Basic validation
            if len(vertices) == 0 or len(faces) == 0:
                raise ValueError("Empty geometry generated")

            # Calculate basic statistics
            bbox_min = np.min(vertices, axis=0)
            bbox_max = np.max(vertices, axis=0)
            bbox_size = bbox_max - bbox_min

            metadata = {
                "vertex_count": len(vertices),
                "face_count": len(faces),
                "bounding_box": {
                    "min": bbox_min.tolist(),
                    "max": bbox_max.tolist(),
                    "size": bbox_size.tolist()
                },
                "volume_estimate": self._estimate_volume(vertices, faces)
            }

            return {
                "vertices": vertices,
                "faces": faces,
                "metadata": metadata
            }

        except Exception as e:
            logger.error(f"Geometry postprocessing failed: {e}")
            raise

    def _estimate_volume(self, vertices: np.ndarray, faces: np.ndarray) -> float:
        """Estimate mesh volume using signed volume of tetrahedra"""
        try:
            # Simple volume estimation
            volume = 0.0
            for face in faces:
                if len(face) >= 3:
                    v0, v1, v2 = vertices[face[:3]]
                    # Volume of tetrahedron from origin
                    volume += np.abs(np.dot(v0, np.cross(v1, v2))) / 6.0
            return float(volume)
        except Exception:
            return 0.0

    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the model"""
        return {
            "name": self.model_name,
            "loaded": self.is_loaded,
            "available": self.is_available(),
            "device": self.device,
            "model_path": str(self.model_path) if self.model_path else None
        }

    def unload_model(self):
        """Unload the model to free memory"""
        self.model = None
        self.is_loaded = False
        logger.info(f"Unloaded model: {self.model_name}")


class DemoText3DModel(BaseText3DModel):
    """Demo implementation that creates simple geometric shapes"""

    def __init__(self):
        super().__init__("demo")
        self.is_loaded = True  # Demo model is always "loaded"

    def load_model(self) -> bool:
        """Demo model doesn't need actual loading"""
        self.is_loaded = True
        return True

    def is_available(self) -> bool:
        """Demo model is always available"""
        return True

    def generate_3d(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate simple 3D shapes based on prompt keywords"""
        try:
            cleaned_prompt = self.preprocess_prompt(prompt)

            # Extract shape from prompt
            shape_type = self._extract_shape_type(cleaned_prompt)
            size = self._extract_size(cleaned_prompt)

            # Generate geometry based on shape type
            if shape_type == "sphere":
                vertices, faces = self._create_sphere(size)
            elif shape_type == "cylinder":
                vertices, faces = self._create_cylinder(size)
            elif shape_type == "pyramid":
                vertices, faces = self._create_pyramid(size)
            else:
                vertices, faces = self._create_cube(size)

            result = self.postprocess_geometry(vertices, faces)
            result["metadata"]["shape_type"] = shape_type
            result["metadata"]["generation_method"] = "demo"

            return result

        except Exception as e:
            logger.error(f"Demo generation failed: {e}")
            raise

    def _extract_shape_type(self, prompt: str) -> str:
        """Extract shape type from prompt"""
        if any(word in prompt for word in ["sphere", "ball", "round", "orb"]):
            return "sphere"
        elif any(word in prompt for word in ["cylinder", "tube", "pipe", "rod"]):
            return "cylinder"
        elif any(word in prompt for word in ["pyramid", "triangle", "cone"]):
            return "pyramid"
        else:
            return "cube"

    def _extract_size(self, prompt: str) -> float:
        """Extract size hint from prompt"""
        if any(word in prompt for word in ["small", "tiny", "mini"]):
            return 0.5
        elif any(word in prompt for word in ["large", "big", "huge", "giant"]):
            return 2.0
        else:
            return 1.0

    def _create_cube(self, size: float = 1.0) -> tuple[np.ndarray, np.ndarray]:
        """Create cube geometry"""
        s = size / 2
        vertices = np.array([
            [-s, -s, -s], [s, -s, -s], [s, s, -s], [-s, s, -s],  # bottom
            [-s, -s, s], [s, -s, s], [s, s, s], [-s, s, s]       # top
        ], dtype=np.float32)

        faces = np.array([
            [0, 1, 2], [0, 2, 3],  # bottom
            [4, 7, 6], [4, 6, 5],  # top
            [0, 4, 5], [0, 5, 1],  # front
            [2, 6, 7], [2, 7, 3],  # back
            [0, 3, 7], [0, 7, 4],  # left
            [1, 5, 6], [1, 6, 2]   # right
        ], dtype=np.uint32)

        return vertices, faces

    def _create_sphere(self, size: float = 1.0) -> tuple[np.ndarray, np.ndarray]:
        """Create sphere geometry using UV sphere method"""
        radius = size / 2
        lat_segments = 16
        lon_segments = 32

        vertices = []
        faces = []

        # Generate vertices
        for i in range(lat_segments + 1):
            lat = np.pi * (-0.5 + float(i) / lat_segments)
            for j in range(lon_segments + 1):
                lon = 2 * np.pi * float(j) / lon_segments

                x = radius * np.cos(lat) * np.cos(lon)
                y = radius * np.sin(lat)
                z = radius * np.cos(lat) * np.sin(lon)

                vertices.append([x, y, z])

        # Generate faces
        for i in range(lat_segments):
            for j in range(lon_segments):
                first = i * (lon_segments + 1) + j
                second = first + lon_segments + 1

                faces.append([first, second, first + 1])
                faces.append([second, second + 1, first + 1])

        return np.array(vertices, dtype=np.float32), np.array(faces, dtype=np.uint32)

    def _create_cylinder(self, size: float = 1.0) -> tuple[np.ndarray, np.ndarray]:
        """Create cylinder geometry"""
        radius = size / 2
        height = size
        segments = 16

        vertices = []
        faces = []

        # Bottom center
        vertices.append([0, -height/2, 0])
        # Top center
        vertices.append([0, height/2, 0])

        # Bottom and top ring vertices
        for i in range(segments):
            angle = 2 * np.pi * i / segments
            x = radius * np.cos(angle)
            z = radius * np.sin(angle)

            vertices.append([x, -height/2, z])  # bottom ring
            vertices.append([x, height/2, z])   # top ring

        # Bottom faces
        for i in range(segments):
            next_i = (i + 1) % segments
            faces.append([0, 2 + i * 2, 2 + next_i * 2])

        # Top faces
        for i in range(segments):
            next_i = (i + 1) % segments
            faces.append([1, 3 + next_i * 2, 3 + i * 2])

        # Side faces
        for i in range(segments):
            next_i = (i + 1) % segments

            # Bottom triangle
            faces.append([2 + i * 2, 3 + i * 2, 2 + next_i * 2])
            # Top triangle
            faces.append([3 + i * 2, 3 + next_i * 2, 2 + next_i * 2])

        return np.array(vertices, dtype=np.float32), np.array(faces, dtype=np.uint32)

    def _create_pyramid(self, size: float = 1.0) -> tuple[np.ndarray, np.ndarray]:
        """Create pyramid geometry"""
        s = size / 2
        h = size

        vertices = np.array([
            # Base vertices
            [-s, -h/2, -s],
            [s, -h/2, -s],
            [s, -h/2, s],
            [-s, -h/2, s],
            # Apex
            [0, h/2, 0]
        ], dtype=np.float32)

        faces = np.array([
            # Base
            [0, 1, 2], [0, 2, 3],
            # Sides
            [0, 4, 1], [1, 4, 2], [2, 4, 3], [3, 4, 0]
        ], dtype=np.uint32)

        return vertices, faces