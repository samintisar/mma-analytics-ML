# MMA Analytics Constitution

## Core Principles

### I. Library-First Architecture
Every feature must be implemented as a standalone library with clear interfaces:
- **Video processing**: Independent modules for pose estimation, strike detection, action recognition
- **Stats analysis**: Separate libraries for data ingestion, feature engineering, model training
- **Commentary mining**: Standalone ASR, NLP, and claim extraction modules
- **Reporting**: Modular visualization and export libraries
- Each library must be independently testable and documented

### II. CLI Interface Standard
Every library exposes functionality via command-line interface:
- **Input/Output**: stdin/args → stdout, errors → stderr
- **Format support**: JSON + human-readable formats required
- **Standard flags**: `--help`, `--version`, `--format json|csv|yaml`
- **Example**: `mma-strikes --video input.mp4 --format json > strikes.json`

### III. Test-First Development (NON-NEGOTIABLE)
Strict TDD enforcement for ML/video processing reliability:
- **Order**: Write tests → Get approval → Watch tests fail → Implement
- **Coverage**: Contract tests, integration tests, model validation tests
- **Real data**: Use actual video files and datasets, not mocks
- **Performance**: Include accuracy/precision thresholds in tests

### IV. Integration Testing Focus
Critical areas requiring integration tests:
- **Video pipeline**: End-to-end processing (raw video → insights)
- **Model chains**: Strike detection → combo analysis → vulnerability mining
- **Data flows**: UFCStats → feature engineering → prediction model
- **Commentary alignment**: ASR → claim extraction → video event correlation

### V. Observability & Debugging
Text-based protocols ensure debuggability in ML workflows:
- **Structured logging**: JSON logs with timestamps, confidence scores, processing stages
- **Pipeline tracking**: Log video processing steps, model predictions, data transformations
- **Error context**: Include frame numbers, timestamps, model versions in error messages
- **Performance metrics**: Log processing times, memory usage, GPU utilization

### VI. Versioning & Model Management
Handle ML model evolution and breaking changes:
- **Format**: MAJOR.MINOR.BUILD (e.g., v1.2.15)
- **Model versions**: Track training data, hyperparameters, performance metrics
- **Breaking changes**: New model architectures, changed input formats
- **Migration**: Parallel model testing, gradual rollout procedures

### VII. Simplicity & YAGNI
Start simple, avoid over-engineering ML pipelines:
- **Max 3 projects**: Core (video+stats), notebooks (analysis), tools (utilities)
- **Direct frameworks**: Use PyTorch/OpenCV directly, avoid wrapper abstractions
- **Single data model**: Avoid DTOs unless serialization formats truly differ
- **Proven patterns only**: No Repository/UoW patterns without demonstrated need

## ML-Specific Constraints

### Data Management
- **Reproducibility**: Version datasets, seed random generators, track data splits
- **Storage**: Local-first approach, offline-capable for RTX 3090 setup
- **Privacy**: No cloud uploads of UFC footage, local processing only

### Model Development
- **Evaluation**: Precision ≥85% for basic strikes, ≥75% for complex techniques
- **Validation**: Time-aware splits, no data leakage across fights
- **Documentation**: Model cards with architecture, training data, performance metrics

### Performance Standards
- **Real-time capable**: Video processing at 25-30 FPS on RTX 3090
- **Memory efficient**: <16GB GPU memory usage for full pipeline
- **Accuracy targets**: Stats model ≥70% accuracy, Brier ≤0.20

## Governance
Constitution supersedes all development practices. All features must pass constitutional compliance checks before implementation. Complexity deviations require written justification and simpler alternative analysis.

**Version**: 1.0.0 | **Ratified**: 2025-09-09 | **Last Amended**: 2025-09-09
