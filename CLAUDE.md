# CLAUDE.md - AI 3D Generator

## Claude Code Configuration

This file contains Claude Code specific instructions and configurations for the AI 3D Generator project.

### Project Commands

```bash
# Backend development
source venv/bin/activate
python api/main.py

# Frontend development
cd frontend
npm start

# Testing
pytest tests/
npm test  # (when frontend tests are added)

# Docker development
docker-compose up -d

# Linting and formatting
black .
flake8 .
npm run lint  # (when configured)

# Model downloads
python scripts/download_models.py
```

### Development Workflow

1. **Setup Process**
   - Run `python -m venv venv` to create virtual environment
   - Activate with `source venv/bin/activate` (Unix) or `venv\Scripts\activate` (Windows)
   - Install dependencies with `pip install -r requirements.txt`
   - Set up frontend with `cd frontend && npm install`

2. **Local Development**
   - Backend runs on `http://localhost:8000`
   - Frontend runs on `http://localhost:3000`
   - Use `.env` file for environment configuration (copy from `.env.example`)

3. **Testing Strategy**
   - Backend tests in `tests/` directory using pytest
   - Run with `pytest tests/` for unit and integration tests
   - Frontend tests to be added in `frontend/src/__tests__/`

4. **Docker Deployment**
   - Use `docker-compose up -d` for full stack
   - Includes backend, frontend, and Redis services
   - GPU support configured for ML workloads

### Architecture Overview

This project implements an AI-powered 3D model generator with the following components:

#### Core Components
- **Text-to-3D Pipeline**: AI models for converting text descriptions to 3D models
- **Mesh Processing**: 3D geometry optimization and repair
- **FastAPI Backend**: RESTful API with WebSocket support
- **React Frontend**: Interactive web interface with Three.js 3D viewer
- **Model Storage**: Pre-trained AI models and generated assets

#### Technology Stack
- **Backend**: FastAPI, PyTorch, Transformers, Diffusers
- **3D Processing**: Trimesh, Open3D, PyMeshLab
- **Frontend**: React, Three.js, React Three Fiber
- **Infrastructure**: Docker, Redis, CUDA support

### File Structure

```
ai-3d-generator/
├── core/                           # Core AI and 3D processing
│   ├── text_to_3d/                # Text-to-3D generation models
│   ├── mesh_processing/            # 3D geometry processing
│   └── optimization/               # Model optimization utilities
├── api/                           # FastAPI backend
│   ├── routes/                    # API route definitions
│   ├── models/                    # Pydantic models
│   └── utils/                     # Backend utilities
├── frontend/                      # React + Three.js frontend
│   ├── public/                    # Static assets
│   └── src/                       # React source code
│       ├── components/            # React components
│       ├── viewer/                # 3D viewer components
│       └── utils/                 # Frontend utilities
├── models/pretrained/             # AI model storage
├── examples/gallery/              # Example generations
├── tests/                         # Test suites
│   ├── unit/                      # Unit tests
│   └── integration/               # Integration tests
├── docs/                          # Documentation
├── scripts/                       # Utility scripts
└── .github/                       # GitHub workflows and templates
```

### AI Model Configuration

The project supports multiple AI models for 3D generation:

1. **Point-E**: OpenAI's point cloud generation model
2. **Shap-E**: OpenAI's 3D shape generation model
3. **Custom Models**: Extensible framework for additional models

Configure in `.env`:
```bash
MODEL_TYPE=point-e  # Options: point-e, shap-e, custom
MODEL_PATH=./models/pretrained
USE_GPU=true
```

### API Endpoints

Key API endpoints (when implemented):
- `POST /generate` - Generate 3D model from text
- `GET /models` - List available AI models
- `POST /optimize` - Optimize 3D mesh for printing
- `GET /gallery` - Browse example generations
- `WebSocket /ws` - Real-time generation updates

### Frontend Features

- **Text Input**: Natural language 3D model descriptions
- **3D Viewer**: Interactive WebGL-based model preview
- **Export Options**: STL, OBJ, PLY file formats
- **Gallery**: Browse and favorite generated models
- **Real-time Updates**: WebSocket connection for generation progress

### Performance Targets

- **Generation Time**: <30 seconds for simple models
- **Model Quality**: Manifold meshes suitable for 3D printing
- **File Size**: Optimized STL files <10MB
- **Concurrent Users**: Support 10+ simultaneous generations
- **GPU Memory**: <8GB VRAM for most models

### Development Guidelines

1. **Code Style**
   - Python: Black formatting, flake8 linting
   - JavaScript: Prettier formatting, ESLint
   - Follow existing patterns in the codebase

2. **Testing Requirements**
   - Write unit tests for all new functions
   - Integration tests for API endpoints
   - Visual regression tests for 3D viewer

3. **Security Considerations**
   - Input validation for text prompts
   - File size limits for uploads/downloads
   - Rate limiting for API endpoints
   - Secure model file handling

### Troubleshooting

Common issues and solutions:

1. **GPU/CUDA Issues**
   - Verify CUDA installation: `nvidia-smi`
   - Check PyTorch CUDA support: `python -c "import torch; print(torch.cuda.is_available())"`
   - Use CPU fallback if GPU unavailable

2. **Memory Issues**
   - Monitor GPU memory usage during generation
   - Implement model caching and cleanup
   - Use model quantization for resource constraints

3. **3D Processing Issues**
   - Validate mesh topology before export
   - Use mesh repair tools for broken geometries
   - Check manifold properties for 3D printing

### Environment Variables

Required environment variables:
```bash
# API Configuration
export API_HOST=0.0.0.0
export API_PORT=8000
export API_ENV=development

# AI Configuration
export MODEL_PATH=./models/pretrained
export USE_GPU=true
export MODEL_TYPE=point-e

# Frontend Configuration
export FRONTEND_URL=http://localhost:3000

# Cache and Storage
export CACHE_DIR=./cache
export MAX_CACHE_SIZE=10GB

# Security
export SECRET_KEY=your-secret-key-here
export CORS_ORIGINS=["http://localhost:3000"]
```

### Claude Code Integration

This project is optimized for Claude Code development:
- Use `Read` to examine component implementations
- Use `Grep` to search for specific functionality
- Use `Edit` to modify configurations and code
- Use `Bash` to run development and test commands
- Use `TodoWrite` to track feature development

### Contributing Guidelines

When working on this project:
1. Follow the established directory structure
2. Write comprehensive tests for new features
3. Update documentation for API changes
4. Ensure 3D models are manifold and printable
5. Test with multiple AI model backends
6. Validate frontend 3D viewer compatibility

### Monitoring and Debugging

- Use FastAPI automatic docs at `http://localhost:8000/docs`
- Monitor GPU usage with `nvidia-smi`
- Check Redis connection for caching
- Use browser dev tools for frontend debugging
- Enable verbose logging in development mode

For questions or issues, refer to the comprehensive documentation in README.md or examine the source code directly.