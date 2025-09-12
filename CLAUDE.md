# Claude Development Assistant Configuration

**Project**: MMA Analytics ML  
**Feature**: Project Foundation Setup  
**Branch**: 001-setup-tasks-set  
**Updated**: 2025-09-12

## Project Overview

This is a foundation setup for MMA Analytics machine learning project focused on UFC fight analysis. The project uses Python 3.11, PyTorch with CUDA support for RTX 3090, and follows constitutional principles for library-first architecture.

## Current Development Context

### Active Feature
- **Branch**: `001-setup-tasks-set`
- **Status**: Foundation setup in progress
- **Phase**: Planning and design complete
- **Next Step**: Task generation and implementation

### Technical Stack
- **Language**: Python 3.11
- **ML Framework**: PyTorch 2.1+ with CUDA 12.1
- **Data Processing**: Pandas, NumPy, scikit-learn
- **Computer Vision**: OpenCV, FFmpeg
- **Web Scraping**: Requests, BeautifulSoup4
- **Development**: Jupyter, pytest
- **Environment**: Conda with isolated environment
- **Version Control**: Git with LFS for large files

### Repository Structure
```
src/
├── ingest/          # UFCStats scraping, data validation
├── video/           # Video preprocessing, format validation
└── utils/           # Environment detection, logging

data/
├── raw/            # Original UFCStats data, videos
├── processed/      # Normalized videos, segments
├── models/         # Git LFS tracked model files
└── fixtures/       # Test data samples

tests/
├── contract/       # API/interface validation
├── integration/    # End-to-end pipeline tests
├── model/          # Model accuracy tests
└── unit/           # Component tests

scripts/
├── setup/          # Environment bootstrap, directory init
└── runners/        # UFCStats and video processing runners
```

## Development Guidelines

### Constitutional Compliance
- **Library-First**: Every component as independent, testable library
- **CLI Interface**: All functionality exposed via command line
- **Test-First**: RED-GREEN-REFACTOR cycle strictly enforced
- **Simplicity**: Max 3 projects, direct framework usage, minimal abstractions
- **Observability**: Structured logging, pipeline tracking, error context
- **Privacy**: Local-only UFC footage processing, no cloud uploads

### Code Style
- **Python**: Follow PEP 8, type hints for all functions
- **Documentation**: Docstrings for all public functions
- **Testing**: pytest with coverage, contract tests first
- **Error Handling**: Specific exception types with context
- **Logging**: JSON format with timestamps and component context

### Data Handling
- **Formats**: JSON for structured data, MP4/MKV for videos
- **Validation**: Schema validation for all data inputs/outputs
- **Storage**: Hierarchical organization by data type and processing stage
- **Privacy**: No external data uploads, local processing only

## Current Tasks Status

### Completed (Planning Phase)
- [x] Feature specification analysis
- [x] Technical research and architecture design
- [x] Data model and entity definition
- [x] Contract schema generation
- [x] Quickstart guide creation

### Next Phase (Implementation)
- [ ] Task generation from design documents
- [ ] Environment setup implementation
- [ ] Repository structure creation
- [ ] Data ingestion scripts
- [ ] Video preprocessing pipeline
- [ ] CLI interface implementation
- [ ] Test suite development
- [ ] Validation and integration testing

## Important Files and Locations

### Configuration Files
- `environment.yml` - Conda environment specification
- `.gitattributes` - Git LFS configuration
- `specs/001-setup-tasks-set/` - Feature documentation

### Key Scripts
- `scripts/setup/bootstrap.sh` - Environment setup
- `scripts/setup/init_dirs.py` - Directory structure initialization
- `scripts/runners/ufcscrape_runner.py` - UFCStats data scraping
- `scripts/runners/video_preprocess_runner.py` - Video processing

### Library Entry Points
- `src/ingest/ufcscrape.py` - UFCStats scraping library
- `src/video/preprocessing.py` - Video processing library
- `src/utils/environment.py` - Environment utilities

### Test Structure
- `tests/contract/` - API contract validation tests
- `tests/integration/` - End-to-end pipeline tests
- `tests/unit/` - Component unit tests

## Development Commands

### Environment Setup
```bash
# Create and activate environment
conda env create -f environment.yml
conda activate mma-analytics

# Validate environment
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"
```

### Data Operations
```bash
# Scrape UFCStats data
python scripts/runners/ufcscrape_runner.py --output-dir data/raw/

# Process videos
python scripts/runners/video_preprocess_runner.py --input-dir data/raw/videos/ --output-dir data/processed/
```

### Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Test specific components
pytest tests/contract/ tests/integration/
```

## Performance Requirements

### Environment Setup
- **Time**: < 15 minutes for complete environment creation
- **Success**: All dependencies install without conflicts
- **GPU**: RTX 3090 detected and functional (≥12GB utilization)

### Data Processing
- **UFCStats Scraping**: < 30 minutes for complete historical data
- **Video Processing**: 25-30 FPS on RTX 3090
- **Memory Usage**: < 16GB GPU memory for full pipeline
- **Data Quality**: > 95% completeness and accuracy

## Risk Areas and Mitigation

### Technical Risks
- **UFCStats Website Changes**: Modular scraping design, easy selector updates
- **Corrupted Video Files**: Format validation, checksum verification
- **GPU Memory Constraints**: Chunked processing, memory monitoring
- **Dependency Conflicts**: Pinned versions, clean environment rebuild

### Development Risks
- **Scope Creep**: Strict adherence to foundation setup requirements
- **Over-engineering**: Constitution compliance and simplicity principles
- **Integration Issues**: Contract tests before implementation

## Getting Help

### Resources
- **Feature Specification**: `specs/001-setup-tasks-set/spec.md`
- **Implementation Plan**: `specs/001-setup-tasks-set/plan.md`
- **Constitution**: `memory/constitution.md`
- **Quickstart Guide**: `specs/001-setup-tasks-set/quickstart.md`

### Commands for Development
```bash
# Show current branch and status
git status
git branch --show-current

# View feature specifications
cat specs/001-setup-tasks-set/spec.md

# Check development guidelines
cat memory/constitution.md

# Run validation tests
pytest tests/contract/ -v
```

## Notes for Future Development

### ML Model Development
- Foundation setup provides environment and data pipelines
- Next phase will implement actual ML models for fight analysis
- Constitutional principles apply to all ML components
- Library-first architecture required for model components

### Scaling Considerations
- Current setup optimized for single RTX 3090
- Local-first approach can be extended to distributed processing
- Data organization supports incremental growth
- CLI interfaces enable automation and pipeline integration

---
*Configuration complete - Ready for foundation implementation*