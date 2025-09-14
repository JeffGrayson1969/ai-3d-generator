#!/bin/bash

# Create main project directory
mkdir -p ai-3d-generator
cd ai-3d-generator

# Create project structure
mkdir -p core/{text_to_3d,mesh_processing,optimization}
mkdir -p api/{routes,models,utils}
mkdir -p frontend/{public,src/{components,viewer,utils}}
mkdir -p models/pretrained
mkdir -p examples/gallery
mkdir -p tests/{unit,integration}
mkdir -p docs
mkdir -p scripts
mkdir -p .github/workflows

# Create Python virtual environment
python3 -m venv venv

# Create .gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/
*.egg-info/
dist/
build/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Project specific
models/pretrained/*.pth
models/pretrained/*.ckpt
*.stl
*.obj
*.ply
temp/
cache/

# Environment
.env
.env.local

# Node
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
frontend/.pnpm-debug.log*

# Production
frontend/build/
frontend/dist/

# OS
.DS_Store
Thumbs.db

# Logs
logs/
*.log
EOF

# Create README.md
cat > README.md << 'EOF'
# 🎨 AI 3D Model Generator

An open-source AI-powered 3D model generator for makers and 3D printing enthusiasts. Generate STL files from text descriptions using state-of-the-art AI models.

## 🚀 Features

- **Text-to-3D Generation**: Create 3D models from natural language descriptions
- **Real-time Preview**: Interactive 3D viewer with WebGL
- **Print Optimization**: Automatic manifold checking and repair
- **Interactive Editing**: Modify models with text commands
- **STL Export**: Ready-to-print files for your 3D printer

## 📋 Requirements

- Python 3.8+
- Node.js 16+
- CUDA-capable GPU (optional but recommended)
- 8GB+ RAM

## 🛠️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/ai-3d-generator.git
cd ai-3d-generator
```

### 2. Set up Python backend
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Set up frontend
```bash
cd frontend
npm install
```

### 4. Download AI models
```bash
python scripts/download_models.py
```

## 🎮 Usage

### Start the backend server
```bash
source venv/bin/activate
python api/main.py
```

### Start the frontend (in another terminal)
```bash
cd frontend
npm start
```

Navigate to `http://localhost:3000` in your browser.

## 🏗️ Architecture

```
├── core/               # Core AI and 3D processing
├── api/                # FastAPI backend
├── frontend/           # React + Three.js frontend
├── models/             # Pre-trained model storage
└── examples/           # Example generations
```

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI Point-E team
- Three.js community
- Trimesh developers

## 🔗 Links

- [Documentation](https://github.com/yourusername/ai-3d-generator/wiki)
- [Issues](https://github.com/yourusername/ai-3d-generator/issues)
- [Discussions](https://github.com/yourusername/ai-3d-generator/discussions)
EOF

# Create LICENSE (MIT)
cat > LICENSE << 'EOF'
MIT License

Copyright (c) 2024 AI 3D Generator Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF

# Create requirements.txt
cat > requirements.txt << 'EOF'
# Core dependencies
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6
websockets==12.0
python-dotenv==1.0.0

# AI/ML dependencies
torch>=2.0.0
transformers==4.35.0
diffusers==0.23.0
accelerate==0.24.0

# 3D processing
trimesh==4.0.5
numpy-stl==3.0.1
open3d==0.17.0
pymeshlab==2022.2.post3
scikit-image==0.22.0

# Utilities
numpy==1.24.3
pillow==10.1.0
requests==2.31.0
pydantic==2.5.0
aiofiles==23.2.1

# Development
pytest==7.4.3
black==23.11.0
flake8==6.1.0
EOF

# Create package.json for frontend
cat > frontend/package.json << 'EOF'
{
  "name": "ai-3d-generator-frontend",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "three": "^0.158.0",
    "@react-three/fiber": "^8.15.0",
    "@react-three/drei": "^9.88.0",
    "axios": "^1.6.0",
    "socket.io-client": "^4.5.4",
    "react-dropzone": "^14.2.3",
    "tailwindcss": "^3.3.5",
    "lucide-react": "^0.292.0"
  },
  "scripts": {
    "start": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.1.1",
    "vite": "^5.0.0",
    "autoprefixer": "^10.4.16",
    "postcss": "^8.4.31"
  }
}
EOF

# Create .env.example
cat > .env.example << 'EOF'
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_ENV=development

# AI Model Configuration
MODEL_PATH=./models/pretrained
USE_GPU=true
MODEL_TYPE=point-e  # Options: point-e, shap-e, custom

# Frontend Configuration
FRONTEND_URL=http://localhost:3000

# Cache Configuration
CACHE_DIR=./cache
MAX_CACHE_SIZE=10GB

# Security
SECRET_KEY=your-secret-key-here
CORS_ORIGINS=["http://localhost:3000"]
EOF

# Create docker-compose.yml
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    ports:
      - "8000:8000"
    volumes:
      - ./models:/app/models
      - ./cache:/app/cache
    environment:
      - API_ENV=production
      - USE_GPU=true
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:80"
    depends_on:
      - backend
    environment:
      - REACT_APP_API_URL=http://localhost:8000

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  redis_data:
EOF

# Create Dockerfile for backend
cat > Dockerfile.backend << 'EOF'
FROM nvidia/cuda:11.8.0-runtime-ubuntu22.04

WORKDIR /app

# Install Python
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF

# Create initial test file
cat > tests/test_basic.py << 'EOF'
import pytest
from fastapi.testclient import TestClient
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_placeholder():
    """Placeholder test to ensure pytest works"""
    assert True == True
EOF

# Create CONTRIBUTING.md
cat > CONTRIBUTING.md << 'EOF'
# Contributing to AI 3D Generator

Thank you for your interest in contributing to AI 3D Generator!

## Getting Started

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Development Setup

See README.md for installation instructions.

## Code Style

- Python: We use Black for formatting and flake8 for linting
- JavaScript: Prettier and ESLint

## Testing

Run tests before submitting PR:
```bash
pytest tests/
```

## Pull Request Process

1. Update README.md with details of changes if needed
2. Update requirements.txt if you add dependencies
3. Ensure all tests pass
4. Request review from maintainers
EOF

echo "✅ Project structure created successfully!"
echo ""
echo "Next steps:"
echo "1. cd ai-3d-generator"
echo "2. git init"
echo "3. source venv/bin/activate"
echo "4. pip install -r requirements.txt"
echo "5. Open in VSCode: code ."