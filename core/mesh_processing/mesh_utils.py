import numpy as np
from typing import Tuple, Dict, Any, Optional
import logging
from pathlib import Path
from stl import mesh
import trimesh

logger = logging.getLogger(__name__)

class MeshProcessor:
    """Advanced mesh processing utilities for 3D models"""

    @staticmethod
    def create_mesh_from_arrays(vertices: np.ndarray, faces: np.ndarray) -> mesh.Mesh:
        """Create STL mesh from vertex and face arrays"""
        try:
            # Validate input
            if vertices.shape[1] != 3:
                raise ValueError(f"Vertices must have shape (N, 3), got {vertices.shape}")
            if faces.shape[1] != 3:
                raise ValueError(f"Faces must have shape (N, 3), got {faces.shape}")

            # Create mesh
            stl_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))

            for i, face in enumerate(faces):
                for j in range(3):
                    stl_mesh.vectors[i][j] = vertices[face[j]]

            return stl_mesh

        except Exception as e:
            logger.error(f"Failed to create mesh: {e}")
            raise

    @staticmethod
    def save_mesh(mesh_obj: mesh.Mesh, file_path: str, format: str = "stl") -> bool:
        """Save mesh to file in specified format"""
        try:
            file_path = Path(file_path)
            file_path.parent.mkdir(parents=True, exist_ok=True)

            if format.lower() == "stl":
                mesh_obj.save(str(file_path))
                return True
            elif format.lower() in ["obj", "ply"]:
                # Convert to trimesh for other formats
                tm = MeshProcessor._stl_to_trimesh(mesh_obj)
                tm.export(str(file_path))
                return True
            else:
                raise ValueError(f"Unsupported format: {format}")

        except Exception as e:
            logger.error(f"Failed to save mesh: {e}")
            return False

    @staticmethod
    def _stl_to_trimesh(stl_mesh: mesh.Mesh) -> trimesh.Trimesh:
        """Convert STL mesh to trimesh"""
        vertices = []
        faces = []

        # Extract unique vertices and build face indices
        vertex_map = {}
        vertex_index = 0

        for triangle in stl_mesh.vectors:
            face = []
            for vertex in triangle:
                vertex_tuple = tuple(vertex)
                if vertex_tuple not in vertex_map:
                    vertex_map[vertex_tuple] = vertex_index
                    vertices.append(vertex)
                    vertex_index += 1
                face.append(vertex_map[vertex_tuple])
            faces.append(face)

        return trimesh.Trimesh(vertices=np.array(vertices), faces=np.array(faces))

    @staticmethod
    def validate_mesh(vertices: np.ndarray, faces: np.ndarray) -> Dict[str, Any]:
        """Validate mesh geometry and return analysis"""
        validation = {
            "is_valid": True,
            "errors": [],
            "warnings": [],
            "stats": {}
        }

        try:
            # Basic shape validation
            if vertices.ndim != 2 or vertices.shape[1] != 3:
                validation["errors"].append(f"Invalid vertex shape: {vertices.shape}")
                validation["is_valid"] = False

            if faces.ndim != 2 or faces.shape[1] != 3:
                validation["errors"].append(f"Invalid face shape: {faces.shape}")
                validation["is_valid"] = False

            if len(vertices) == 0:
                validation["errors"].append("No vertices found")
                validation["is_valid"] = False

            if len(faces) == 0:
                validation["errors"].append("No faces found")
                validation["is_valid"] = False

            # Face index validation
            max_vertex_index = len(vertices) - 1
            if np.any(faces > max_vertex_index):
                validation["errors"].append("Face indices exceed vertex count")
                validation["is_valid"] = False

            if np.any(faces < 0):
                validation["errors"].append("Negative face indices found")
                validation["is_valid"] = False

            # Calculate statistics
            validation["stats"] = {
                "vertex_count": len(vertices),
                "face_count": len(faces),
                "bounding_box": MeshProcessor._calculate_bounding_box(vertices),
                "surface_area": MeshProcessor._estimate_surface_area(vertices, faces),
                "volume": MeshProcessor._estimate_volume(vertices, faces)
            }

            # Advanced validation using trimesh if possible
            try:
                tm = trimesh.Trimesh(vertices=vertices, faces=faces)
                validation["stats"]["is_manifold"] = tm.is_manifold
                validation["stats"]["is_watertight"] = tm.is_watertight

                if not tm.is_manifold:
                    validation["warnings"].append("Mesh is not manifold")

                if not tm.is_watertight:
                    validation["warnings"].append("Mesh is not watertight")

            except Exception as e:
                validation["warnings"].append(f"Advanced validation failed: {e}")

        except Exception as e:
            validation["errors"].append(f"Validation error: {e}")
            validation["is_valid"] = False

        return validation

    @staticmethod
    def _calculate_bounding_box(vertices: np.ndarray) -> Dict[str, Any]:
        """Calculate mesh bounding box"""
        if len(vertices) == 0:
            return {"min": [0, 0, 0], "max": [0, 0, 0], "size": [0, 0, 0]}

        min_coords = np.min(vertices, axis=0)
        max_coords = np.max(vertices, axis=0)
        size = max_coords - min_coords

        return {
            "min": min_coords.tolist(),
            "max": max_coords.tolist(),
            "size": size.tolist(),
            "center": ((min_coords + max_coords) / 2).tolist()
        }

    @staticmethod
    def _estimate_surface_area(vertices: np.ndarray, faces: np.ndarray) -> float:
        """Estimate mesh surface area"""
        total_area = 0.0

        try:
            for face in faces:
                if len(face) >= 3:
                    v0, v1, v2 = vertices[face[:3]]
                    # Area of triangle using cross product
                    edge1 = v1 - v0
                    edge2 = v2 - v0
                    cross = np.cross(edge1, edge2)
                    area = np.linalg.norm(cross) / 2.0
                    total_area += area

        except Exception as e:
            logger.warning(f"Surface area calculation failed: {e}")
            return 0.0

        return float(total_area)

    @staticmethod
    def _estimate_volume(vertices: np.ndarray, faces: np.ndarray) -> float:
        """Estimate mesh volume using signed tetrahedra"""
        volume = 0.0

        try:
            for face in faces:
                if len(face) >= 3:
                    v0, v1, v2 = vertices[face[:3]]
                    # Volume of tetrahedron from origin
                    volume += np.dot(v0, np.cross(v1, v2)) / 6.0

        except Exception as e:
            logger.warning(f"Volume calculation failed: {e}")
            return 0.0

        return abs(float(volume))

    @staticmethod
    def optimize_mesh(vertices: np.ndarray, faces: np.ndarray, target_faces: Optional[int] = None) -> Tuple[np.ndarray, np.ndarray]:
        """Optimize mesh by simplification or other operations"""
        try:
            # For now, just return the original mesh
            # In a full implementation, you would use libraries like:
            # - PyMeshLab for mesh simplification
            # - Open3D for various mesh operations
            # - Custom algorithms for optimization

            if target_faces and len(faces) > target_faces:
                logger.info(f"Mesh optimization requested: {len(faces)} -> {target_faces} faces")
                # TODO: Implement mesh simplification
                # For now, just log the request

            return vertices, faces

        except Exception as e:
            logger.error(f"Mesh optimization failed: {e}")
            return vertices, faces

    @staticmethod
    def repair_mesh(vertices: np.ndarray, faces: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Repair common mesh issues"""
        try:
            # Remove duplicate vertices
            vertices, faces = MeshProcessor._remove_duplicate_vertices(vertices, faces)

            # Remove degenerate faces
            faces = MeshProcessor._remove_degenerate_faces(vertices, faces)

            return vertices, faces

        except Exception as e:
            logger.error(f"Mesh repair failed: {e}")
            return vertices, faces

    @staticmethod
    def _remove_duplicate_vertices(vertices: np.ndarray, faces: np.ndarray, tolerance: float = 1e-6) -> Tuple[np.ndarray, np.ndarray]:
        """Remove duplicate vertices and update face indices"""
        try:
            unique_vertices = []
            vertex_mapping = {}
            new_faces = []

            for i, vertex in enumerate(vertices):
                found = False
                for j, unique_vertex in enumerate(unique_vertices):
                    if np.allclose(vertex, unique_vertex, atol=tolerance):
                        vertex_mapping[i] = j
                        found = True
                        break

                if not found:
                    vertex_mapping[i] = len(unique_vertices)
                    unique_vertices.append(vertex)

            # Update face indices
            for face in faces:
                new_face = [vertex_mapping[vertex_idx] for vertex_idx in face]
                new_faces.append(new_face)

            return np.array(unique_vertices), np.array(new_faces)

        except Exception as e:
            logger.error(f"Duplicate vertex removal failed: {e}")
            return vertices, faces

    @staticmethod
    def _remove_degenerate_faces(vertices: np.ndarray, faces: np.ndarray) -> np.ndarray:
        """Remove faces with zero area or invalid indices"""
        valid_faces = []

        for face in faces:
            if len(set(face)) == 3:  # All vertices are different
                try:
                    v0, v1, v2 = vertices[face[:3]]
                    edge1 = v1 - v0
                    edge2 = v2 - v0
                    cross = np.cross(edge1, edge2)
                    area = np.linalg.norm(cross)

                    if area > 1e-10:  # Non-zero area
                        valid_faces.append(face)
                except (IndexError, ValueError):
                    # Skip invalid faces
                    continue

        return np.array(valid_faces) if valid_faces else faces

    @staticmethod
    def center_mesh(vertices: np.ndarray) -> np.ndarray:
        """Center mesh at origin"""
        if len(vertices) == 0:
            return vertices

        center = np.mean(vertices, axis=0)
        return vertices - center

    @staticmethod
    def scale_mesh(vertices: np.ndarray, scale_factor: float) -> np.ndarray:
        """Scale mesh uniformly"""
        return vertices * scale_factor

    @staticmethod
    def normalize_mesh_size(vertices: np.ndarray, target_size: float = 2.0) -> np.ndarray:
        """Normalize mesh to fit within a target size"""
        if len(vertices) == 0:
            return vertices

        # Calculate current bounding box
        min_coords = np.min(vertices, axis=0)
        max_coords = np.max(vertices, axis=0)
        current_size = np.max(max_coords - min_coords)

        if current_size > 0:
            scale_factor = target_size / current_size
            return vertices * scale_factor

        return vertices