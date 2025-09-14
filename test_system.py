#!/usr/bin/env python3
"""
Test script to verify AI 3D Generator system functionality
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.text_to_3d.model_manager import get_model_manager
from core.mesh_processing.mesh_utils import MeshProcessor
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_model_manager():
    """Test the model manager functionality"""
    print("🧪 Testing Model Manager...")

    manager = get_model_manager()

    # Test available models
    models = manager.get_available_models()
    print(f"✅ Available models: {len(models)}")
    for model in models:
        print(f"   - {model['name']}: {model['description']} (available: {model['available']})")

    # Test model stats
    stats = manager.get_model_stats()
    print(f"✅ Model stats: {stats}")

    return True

def test_generation():
    """Test 3D model generation"""
    print("\n🎨 Testing 3D Generation...")

    manager = get_model_manager()

    test_prompts = [
        ("a red cube", "cube"),
        ("a blue sphere", "sphere"),
        ("a green cylinder", "cylinder"),
        ("a yellow pyramid", "pyramid")
    ]

    for prompt, expected_shape in test_prompts:
        try:
            print(f"   Generating: '{prompt}'")
            result = manager.generate_3d("demo", prompt)

            vertices = result["vertices"]
            faces = result["faces"]
            metadata = result["metadata"]

            print(f"   ✅ Generated {metadata.get('shape_type', 'unknown')} with {len(vertices)} vertices, {len(faces)} faces")

            # Validate mesh
            validation = MeshProcessor.validate_mesh(vertices, faces)
            if validation["is_valid"]:
                print(f"      ✅ Mesh is valid")
            else:
                print(f"      ❌ Mesh validation failed: {validation['errors']}")

        except Exception as e:
            print(f"   ❌ Generation failed: {e}")
            return False

    return True

def test_mesh_processing():
    """Test mesh processing utilities"""
    print("\n🔧 Testing Mesh Processing...")

    manager = get_model_manager()

    # Generate a simple cube for testing
    result = manager.generate_3d("demo", "a simple cube")
    vertices = result["vertices"]
    faces = result["faces"]

    # Test mesh creation
    try:
        stl_mesh = MeshProcessor.create_mesh_from_arrays(vertices, faces)
        print("   ✅ STL mesh creation successful")
    except Exception as e:
        print(f"   ❌ STL mesh creation failed: {e}")
        return False

    # Test mesh validation
    try:
        validation = MeshProcessor.validate_mesh(vertices, faces)
        print(f"   ✅ Mesh validation: {validation['is_valid']}")
        print(f"      Stats: {validation['stats']}")
    except Exception as e:
        print(f"   ❌ Mesh validation failed: {e}")
        return False

    # Test mesh operations
    try:
        centered_vertices = MeshProcessor.center_mesh(vertices.copy())
        scaled_vertices = MeshProcessor.scale_mesh(vertices.copy(), 2.0)
        normalized_vertices = MeshProcessor.normalize_mesh_size(vertices.copy())

        print("   ✅ Mesh operations (center, scale, normalize) successful")
    except Exception as e:
        print(f"   ❌ Mesh operations failed: {e}")
        return False

    return True

def main():
    """Run all tests"""
    print("🚀 AI 3D Generator System Test\n" + "="*40)

    tests = [
        ("Model Manager", test_model_manager),
        ("3D Generation", test_generation),
        ("Mesh Processing", test_mesh_processing)
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        try:
            if test_func():
                print(f"\n✅ {test_name} - PASSED")
                passed += 1
            else:
                print(f"\n❌ {test_name} - FAILED")
        except Exception as e:
            print(f"\n💥 {test_name} - ERROR: {e}")

    print("\n" + "="*40)
    print(f"🎯 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All systems operational! The AI 3D Generator is ready to use.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the implementation.")
        return 1

if __name__ == "__main__":
    sys.exit(main())