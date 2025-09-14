from typing import Dict, List, Optional, Any
import logging
from pathlib import Path

from .base_model import BaseText3DModel, DemoText3DModel

logger = logging.getLogger(__name__)

class ModelManager:
    """Manages multiple text-to-3D models and provides a unified interface"""

    def __init__(self, models_dir: Optional[str] = None):
        self.models_dir = Path(models_dir) if models_dir else Path("models/pretrained")
        self.models_dir.mkdir(parents=True, exist_ok=True)

        self._models: Dict[str, BaseText3DModel] = {}
        self._load_default_models()

    def _load_default_models(self):
        """Load default available models"""
        # Always load demo model
        demo_model = DemoText3DModel()
        self.register_model("demo", demo_model)

        # TODO: Add other models when dependencies are available
        # self._try_load_point_e()
        # self._try_load_shap_e()

        logger.info(f"Loaded {len(self._models)} models: {list(self._models.keys())}")

    def register_model(self, name: str, model: BaseText3DModel):
        """Register a new model"""
        self._models[name] = model
        logger.info(f"Registered model: {name}")

    def get_model(self, name: str) -> Optional[BaseText3DModel]:
        """Get a model by name"""
        return self._models.get(name)

    def get_available_models(self) -> List[Dict[str, Any]]:
        """Get list of available models with their info"""
        models_info = []

        for name, model in self._models.items():
            try:
                info = model.get_model_info()
                info.update({
                    "description": self._get_model_description(name),
                    "supported_formats": ["stl", "obj", "ply"],
                    "estimated_time": self._get_estimated_time(name),
                    "quality": self._get_model_quality(name)
                })
                models_info.append(info)
            except Exception as e:
                logger.error(f"Failed to get info for model {name}: {e}")

        return models_info

    def generate_3d(self, model_name: str, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate 3D model using specified model"""
        model = self.get_model(model_name)
        if not model:
            raise ValueError(f"Model '{model_name}' not found")

        if not model.is_available():
            raise RuntimeError(f"Model '{model_name}' is not available")

        try:
            # Ensure model is loaded
            if not model.is_loaded:
                logger.info(f"Loading model: {model_name}")
                if not model.load_model():
                    raise RuntimeError(f"Failed to load model: {model_name}")

            # Generate 3D model
            result = model.generate_3d(prompt, **kwargs)

            # Add generation metadata
            result["metadata"]["model_used"] = model_name
            result["metadata"]["prompt"] = prompt
            result["metadata"]["generation_params"] = kwargs

            return result

        except Exception as e:
            logger.error(f"Generation failed with model {model_name}: {e}")
            raise

    def _get_model_description(self, name: str) -> str:
        """Get human-readable description for a model"""
        descriptions = {
            "demo": "Demo model that generates simple geometric shapes based on text descriptions",
            "point-e": "OpenAI Point-E model for generating 3D point clouds from text",
            "shap-e": "OpenAI Shap-E model for generating 3D shapes and textures from text",
            "custom": "Custom trained model for specialized 3D generation"
        }
        return descriptions.get(name, f"Text-to-3D model: {name}")

    def _get_estimated_time(self, name: str) -> str:
        """Get estimated generation time for a model"""
        times = {
            "demo": "< 1 second",
            "point-e": "30-60 seconds",
            "shap-e": "60-120 seconds",
            "custom": "Variable"
        }
        return times.get(name, "Unknown")

    def _get_model_quality(self, name: str) -> str:
        """Get quality rating for a model"""
        quality = {
            "demo": "Basic",
            "point-e": "Good",
            "shap-e": "High",
            "custom": "Variable"
        }
        return quality.get(name, "Unknown")

    def unload_model(self, name: str):
        """Unload a specific model to free memory"""
        if name in self._models:
            self._models[name].unload_model()
            logger.info(f"Unloaded model: {name}")

    def unload_all_models(self):
        """Unload all models to free memory"""
        for name in list(self._models.keys()):
            self.unload_model(name)

    def get_model_stats(self) -> Dict[str, Any]:
        """Get statistics about loaded models"""
        stats = {
            "total_models": len(self._models),
            "available_models": sum(1 for m in self._models.values() if m.is_available()),
            "loaded_models": sum(1 for m in self._models.values() if m.is_loaded),
            "models": {}
        }

        for name, model in self._models.items():
            stats["models"][name] = {
                "available": model.is_available(),
                "loaded": model.is_loaded,
                "device": getattr(model, 'device', 'unknown')
            }

        return stats

    # TODO: Implement these when AI model dependencies are available
    def _try_load_point_e(self):
        """Try to load Point-E model"""
        try:
            # from .point_e_model import PointEModel
            # point_e = PointEModel(model_path=self.models_dir / "point_e")
            # if point_e.is_available():
            #     self.register_model("point-e", point_e)
            pass
        except ImportError as e:
            logger.warning(f"Point-E model not available: {e}")
        except Exception as e:
            logger.error(f"Failed to load Point-E model: {e}")

    def _try_load_shap_e(self):
        """Try to load Shap-E model"""
        try:
            # from .shap_e_model import ShapEModel
            # shap_e = ShapEModel(model_path=self.models_dir / "shap_e")
            # if shap_e.is_available():
            #     self.register_model("shap-e", shap_e)
            pass
        except ImportError as e:
            logger.warning(f"Shap-E model not available: {e}")
        except Exception as e:
            logger.error(f"Failed to load Shap-E model: {e}")


# Global model manager instance
_model_manager = None

def get_model_manager() -> ModelManager:
    """Get the global model manager instance"""
    global _model_manager
    if _model_manager is None:
        _model_manager = ModelManager()
    return _model_manager

def generate_3d_model(model_name: str, prompt: str, **kwargs) -> Dict[str, Any]:
    """Convenience function to generate 3D model"""
    manager = get_model_manager()
    return manager.generate_3d(model_name, prompt, **kwargs)

def get_available_models() -> List[Dict[str, Any]]:
    """Convenience function to get available models"""
    manager = get_model_manager()
    return manager.get_available_models()