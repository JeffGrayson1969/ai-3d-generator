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