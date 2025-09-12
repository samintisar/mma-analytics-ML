# Quickstart Guide: MMA Analytics ML Foundation

**Branch**: `001-setup-tasks-set` | **Date**: 2025-09-12
**Purpose**: Quick setup guide for new developers

## Prerequisites

### System Requirements
- **Operating System**: Windows, macOS, or Linux
- **Python**: 3.11 or higher
- **GPU**: NVIDIA GPU with CUDA support (RTX 3090 recommended)
- **Memory**: 16GB RAM minimum, 32GB recommended
- **Storage**: 50GB free space minimum
- **Network**: Internet connection for package installation

### Software Requirements
- **Git**: Version control system
- **Conda**: Package and environment management
- **Git LFS**: Large file support for Git

## Setup Steps

### 1. Clone Repository
```bash
git clone https://github.com/your-username/mma-analytics-ML.git
cd mma-analytics-ML
```

### 2. Install Git LFS
```bash
# Install Git LFS (if not already installed)
git lfs install

# Track large files
git lfs track "*.mp4"
git lfs track "*.mkv" 
git lfs track "*.pt"
git lfs track "*.pth"
git lfs track "*.onnx"

# Apply tracking
git add .gitattributes
git commit -m "Configure Git LFS for large files"
```

### 3. Create Conda Environment
```bash
# Create environment from environment.yml
conda env create -f environment.yml

# Activate environment
conda activate mma-analytics

# Validate environment
python scripts/setup/validate_environment.py
```

### 4. Initialize Directory Structure
```bash
# Create data directories
python scripts/setup/init_dirs.py

# Verify structure
ls -la data/
ls -la src/
ls -la tests/
```

### 5. Validate GPU Setup
```bash
# Check PyTorch CUDA availability
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"
python -c "import torch; print(f'GPU count: {torch.cuda.device_count()}')"
python -c "import torch; print(f'Current GPU: {torch.cuda.get_device_name()}')"

# Check GPU memory
python -c "import torch; print(f'GPU memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB')"
```

## First Data Pipeline Run

### 1. UFCStats Data Scraping
```bash
# Scrape all fighter data
python scripts/runners/ufcscrape_runner.py \
    --scrape-type fighters \
    --output-dir data/raw/ufcstats/fighters/ \
    --format json

# Scrape recent bouts
python scripts/runners/ufcscrape_runner.py \
    --scrape-type bouts \
    --output-dir data/raw/ufcstats/bouts/ \
    --format json \
    --date-range-start 2024-01-01 \
    --date-range-end 2024-12-31
```

### 2. Video Processing Test
```bash
# Process sample video (if available)
python scripts/runners/video_preprocess_runner.py \
    --input-dir data/raw/videos/sample/ \
    --output-dir data/processed/videos/ \
    --target-resolution 1280x720 \
    --target-frame-rate 30 \
    --create-segments true \
    --segment-type rounds

# Monitor performance
python scripts/runners/video_preprocess_runner.py \
    --input-dir data/raw/videos/sample/ \
    --output-dir data/processed/videos/ \
    --gpu-acceleration true \
    --batch-size 1
```

## Development Workflow

### 1. Environment Validation
```bash
# Full environment check
python src/utils/environment.py --check-components all --validation-mode comprehensive

# Quick GPU check
python src/utils/environment.py --check-components gpu --validation-mode basic
```

### 2. Running Tests
```bash
# Run all tests
pytest

# Run specific test categories
pytest tests/contract/
pytest tests/integration/
pytest tests/unit/

# Run with coverage
pytest --cov=src --cov-report=html
```

### 3. Code Quality
```bash
# Format code (if using black)
black src/ tests/

# Lint code (if using flake8)
flake8 src/ tests/

# Type checking (if using mypy)
mypy src/
```

## Common Issues

### Environment Issues
**Problem**: Conda environment creation fails
```bash
# Solution: Clean up and retry
conda env remove -n mma-analytics
conda clean -a
conda env create -f environment.yml
```

**Problem**: PyTorch CUDA not available
```bash
# Solution: Verify CUDA installation
nvidia-smi

# Reinstall PyTorch with CUDA
conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia
```

### GPU Memory Issues
**Problem**: Out of memory during video processing
```bash
# Solution: Reduce batch size or resolution
python scripts/runners/video_preprocess_runner.py \
    --input-dir data/raw/videos/ \
    --output-dir data/processed/videos/ \
    --batch-size 1 \
    --target-resolution 640x360
```

### Data Scraping Issues
**Problem**: UFCStats scraping blocked
```bash
# Solution: Add delays and use headers
python scripts/runners/ufcscrape_runner.py \
    --scrape-type fighters \
    --output-dir data/raw/ufcstats/ \
    --delay-seconds 2.0 \
    --batch-size 50
```

## Next Steps

### 1. Explore Data
```bash
# Start Jupyter notebook
jupyter notebook

# Open exploration notebook
jupyter notebook notebooks/exploration/ufc_data_exploration.ipynb
```

### 2. Custom Processing
```bash
# Create custom video processing
cp scripts/runners/video_preprocess_runner.py scripts/runners/custom_processor.py

# Modify custom processor for your needs
# Edit scripts/runners/custom_processor.py
```

### 3. Model Development
```bash
# Start ML development
python src/ingest/ufcscrape.py --help
python src/video/preprocessing.py --help
```

## Validation Checklist

### Environment Setup
- [ ] Conda environment created successfully
- [ ] All packages installed without errors
- [ ] GPU detected and CUDA functional
- [ ] Git LFS configured for large files
- [ ] Directory structure created

### Data Processing
- [ ] UFCStats scraping works without errors
- [ ] Video processing completes successfully
- [ ] Output files are created in correct locations
- [ ] Performance meets requirements (>25 FPS)

### Development
- [ ] Tests run successfully
- [ ] Code quality tools pass
- [ ] Documentation is accessible
- [ ] CLI interfaces work correctly

## Getting Help

### Documentation
- **Feature Specification**: `specs/001-setup-tasks-set/spec.md`
- **Implementation Plan**: `specs/001-setup-tasks-set/plan.md`
- **Data Model**: `specs/001-setup-tasks-set/data-model.md`
- **Contracts**: `specs/001-setup-tasks-set/contracts/`

### Commands
```bash
# Show help for any script
python scripts/runners/ufcscrape_runner.py --help
python scripts/runners/video_preprocess_runner.py --help
python src/utils/environment.py --help

# Check project status
git status
git branch --show-current

# Validate entire setup
pytest tests/integration/test_full_pipeline.py
```

### Troubleshooting
1. Check error messages in console output
2. Verify all prerequisites are installed
3. Ensure GPU drivers are up to date
4. Check disk space and permissions
5. Review logs in output files

---
*Quickstart complete - Ready for development*