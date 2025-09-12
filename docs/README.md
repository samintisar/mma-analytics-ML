# MMA Analytics ML Documentation

**Project**: Mixed Martial Arts Analytics Machine Learning  
**Branch**: `001-setup-tasks-set` (Foundation Setup)  
**Version**: 1.0.0  

## Overview

This project provides a comprehensive foundation for MMA fight analytics using machine learning. The system processes UFC fight footage and statistics to provide actionable insights for coaches, analysts, and fighters.

### Key Features
- **Data Ingestion**: Automated scraping of UFCStats for fighter records and bout results
- **Video Processing**: GPU-accelerated normalization and segmentation of fight footage
- **ML Infrastructure**: PyTorch-based environment optimized for RTX 3090
- **Privacy-First**: Local-only processing with no cloud dependencies

## Quick Start

### Prerequisites
- NVIDIA GPU with CUDA support (RTX 3090 recommended)
- Python 3.11+
- 16GB+ RAM
- 50GB+ free storage

### Setup
```bash
# Clone repository
git clone https://github.com/your-username/mma-analytics-ML.git
cd mma-analytics-ML

# Setup Git LFS
git lfs install
git lfs pull

# Create environment
conda env create -f environment.yml
conda activate mma-analytics

# Initialize directories
python scripts/setup/init_dirs.py

# Validate environment
python src/utils/environment.py --check-components all
```

### First Run
```bash
# Test UFCStats scraping
python scripts/runners/ufcscrape_runner.py \
    --scrape-type fighters \
    --output-dir data/raw/ufcstats/fighters/ \
    --format json

# Test video processing
python scripts/runners/video_preprocess_runner.py \
    --input-dir data/raw/videos/sample/ \
    --output-dir data/processed/videos/ \
    --target-resolution 1280x720
```

## Project Structure

```
mma-analytics-ML/
├── src/                    # Source code libraries
│   ├── ingest/            # UFCStats scraping
│   ├── video/             # Video processing
│   └── utils/             # Utilities and environment
├── data/                  # Data storage (Git LFS managed)
│   ├── raw/              # Original data
│   ├── processed/        # Cleaned data
│   ├── models/           # ML models
│   └── fixtures/         # Test data
├── tests/                 # Test suite
│   ├── contract/         # API tests
│   ├── integration/      # End-to-end tests
│   ├── model/            # ML accuracy tests
│   └── unit/             # Component tests
├── notebooks/            # Jupyter notebooks
├── scripts/              # Automation scripts
│   ├── setup/           # Environment setup
│   └── runners/         # Pipeline runners
└── docs/                # Documentation
```

## Development Guide

### Environment Setup
See: [Setup Guide](setup/README.md)

### Data Processing
See: [Data Processing Guide](processing/README.md)

### ML Development
See: [ML Development Guide](ml/README.md)

### API Reference
See: [API Documentation](api/README.md)

## Configuration

### Environment Variables
- `PYTHONPATH`: Include `src/` directory
- `CUDA_VISIBLE_DEVICES`: GPU selection
- `PYTORCH_CUDA_ALLOC_CONF`: Memory allocation settings

### Configuration Files
- `environment.yml`: Conda environment specification
- `.gitattributes`: Git LFS configuration
- `CLAUDE.md`: Development assistant configuration

## Performance Requirements

### System Requirements
- **GPU**: RTX 3090 or equivalent (24GB VRAM)
- **RAM**: 32GB minimum
- **Storage**: SSD with 100GB+ free space
- **OS**: Windows 10/11, Ubuntu 20.04+, macOS 13+

### Processing Targets
- **Video Processing**: 25-30 FPS on RTX 3090
- **Data Scraping**: <30 minutes for full UFCStats history
- **Memory Usage**: <16GB GPU memory for full pipeline
- **Setup Time**: <15 minutes for complete environment

## Data Sources

### UFCStats
- **URL**: https://ufcstats.com
- **Data Type**: Fighter records, bout results, statistics
- **Update Frequency**: Daily scrape for new events
- **Format**: Structured JSON/CSV

### Fight Videos
- **Source**: UFC broadcasts, highlights, training footage
- **Format**: MP4, MKV (720p-4K)
- **Processing**: Normalization, segmentation, feature extraction
- **Storage**: Local filesystem with Git LFS

## Testing

### Test Categories
- **Contract Tests**: API interface validation
- **Integration Tests**: End-to-end pipeline validation
- **Model Tests**: ML accuracy and performance validation
- **Unit Tests**: Component functionality

### Running Tests
```bash
# All tests
pytest

# With coverage
pytest --cov=src --cov-report=html

# Specific categories
pytest tests/contract/
pytest tests/integration/
```

## Contributing

### Development Workflow
1. Create feature branch from `main`
2. Implement with TDD (RED-GREEN-REFACTOR)
3. Ensure all tests pass
4. Update documentation
5. Submit pull request

### Code Style
- **Python**: Follow PEP 8
- **Type Hints**: Required for all functions
- **Docstrings**: Required for public functions
- **Testing**: pytest with coverage

## Privacy and Security

### Data Privacy
- **Local Processing**: All processing occurs locally
- **No Cloud Uploads**: Fight footage never leaves local system
- **Fair Use**: Data used for research and analysis purposes

### Security
- **Environment Isolation**: Conda environment prevents conflicts
- **Access Control**: Filesystem permissions only
- **No External Dependencies**: Self-contained processing pipeline

## Troubleshooting

### Common Issues
- **GPU Memory**: Reduce batch size or resolution
- **Scraping Blocks**: Add delays and rotate user agents
- **Environment Conflicts**: Clean conda environment rebuild
- **File Permissions**: Verify Git LFS installation

### Support
- **Documentation**: See specific guides in `docs/`
- **Issues**: Report bugs via GitHub issues
- **Discussions**: Use GitHub discussions for questions

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Acknowledgments

- UFCStats for providing comprehensive fight statistics
- PyTorch team for the ML framework
- OpenCV community for computer vision tools
- UFC for providing the sport that makes this analysis possible

---

*Last Updated: 2025-09-12*