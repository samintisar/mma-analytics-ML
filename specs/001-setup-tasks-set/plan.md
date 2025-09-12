# Implementation Plan: Project Foundation Setup

**Branch**: `001-setup-tasks-set` | **Date**: 2025-09-12 | **Spec**: `/specs/001-setup-tasks-set/spec.md`
**Input**: Feature specification from `/specs/001-setup-tasks-set/spec.md`

## Execution Flow (/plan command scope)
```
1. Load feature spec from Input path
   → Feature spec found and loaded successfully
2. Fill Technical Context (scan for NEEDS CLARIFICATION)
   → Project Type: ml-pipeline (video processing + stats analysis)
   → Structure Decision: Foundation infrastructure setup
3. Evaluate Constitution Check section below
   → Constitution check: PASS (infrastructure setup is constitutional)
   → Update Progress Tracking: Initial Constitution Check complete
4. Execute Phase 0 → research.md
   → No NEEDS CLARIFICATION remain, research phase complete
5. Execute Phase 1 → contracts, data-model.md, quickstart.md, CLAUDE.md
6. Re-evaluate Constitution Check section
   → Constitution remains compliant after design
   → Update Progress Tracking: Post-Design Constitution Check
7. Plan Phase 2 → Describe task generation approach (DO NOT create tasks.md)
8. STOP - Ready for /tasks command
```

**IMPORTANT**: The /plan command STOPS at step 7. Phases 2-4 are executed by other commands.

## Summary
Project foundation setup for MMA Analytics ML development environment, including repository structure, Python 3.11 environment with PyTorch+CUDA support for RTX 3090, data ingestion pipelines for UFCStats, video preprocessing infrastructure, and development documentation.

## Technical Context
**Language/Version**: Python 3.11  
**ML Framework**: PyTorch 2.1+ with CUDA 12.1, scikit-learn, OpenCV  
**Model Architecture**: Foundation infrastructure (models to be developed in future features)  
**Data Pipeline**: UFCStats scraping, video preprocessing (MP4/MKV normalization)  
**Storage**: Local filesystem with hierarchical organization, Git LFS for large files  
**Testing**: pytest with contract tests, integration tests, and model validation  
**Target Platform**: RTX 3090 local GPU, offline processing only  
**Project Type**: ml-pipeline (infrastructure foundation)  
**Performance Goals**: 25-30 FPS video processing, <30 min UFCStats scraping, <15 min env setup  
**Model Constraints**: <16GB GPU memory, local-only UFC footage processing  
**Data Scale**: Foundation for 1000+ fights, 10GB+ video data, structured statistics

## Constitution Check
*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Simplicity**:
- Projects: [3] (core libraries, notebooks, tools)
- Using frameworks directly? (PyTorch/OpenCV, no ML wrappers)
- Single data model? (structured JSON/CSV for stats, MP4 for video)
- Avoiding patterns? (no complex abstractions, direct library usage)

**Library-First Architecture**:
- EVERY feature as library? (independent, testable modules)
- Libraries listed: 
  * `src/ingest/` - UFCStats scraping library
  * `src/video/` - Video preprocessing library  
  * `src/utils/` - Environment and utilities library
- CLI per library: 
  * `ufcscrape --help/--version/--format json`
  * `video_preprocess --help/--version/--format json`
  * `utils detect-env`
- Library docs: llms.txt format planned?

**Testing (NON-NEGOTIABLE)**:
- RED-GREEN-Refactor cycle enforced? (test MUST fail first)
- Model validation included? (accuracy/precision thresholds for future models)
- Order: Contract→Integration→Model→Unit strictly followed?
- Real data used? (actual UFCStats data, fight videos)
- Integration tests for: data pipelines, video processing, environment setup
- FORBIDDEN: Training before tests, skipping validation

**ML Observability**:
- Structured logging included? (JSON format with timestamps, component context)
- Model versioning tracked? (Git LFS for model files, versioned data)
- Error context sufficient? (frame numbers, processing times, error codes)
- Performance monitoring? (GPU memory usage, processing speed metrics)

**Data Management**:
- Reproducibility ensured? (seeds, data versions, environment snapshots)
- Privacy compliant? (local-only UFC footage processing)
- Version control? (Git LFS for large files, structured data organization)

## Project Structure

### Documentation (this feature)
```
specs/001-setup-tasks-set/
├── plan.md              # This file (/plan command output)
├── research.md          # Phase 0 output (/plan command)
├── data-model.md        # Phase 1 output (/plan command)
├── quickstart.md        # Phase 1 output (/plan command)
├── contracts/           # Phase 1 output (/plan command)
└── tasks.md             # Phase 2 output (/tasks command - NOT created by /plan)
```

### Source Code (repository root)
```
# Foundation Structure for MMA Analytics
src/
├── ingest/              # UFCStats scraping library
│   ├── __init__.py
│   ├── ufcscrape.py     # Main scraping functionality
│   └── models/          # Data models for UFCStats
├── video/               # Video processing library
│   ├── __init__.py
│   ├── preprocessing.py # Video normalization/segmentation
│   └── formats/         # Format validation utilities
└── utils/               # Environment and utilities
    ├── __init__.py
    ├── environment.py   # GPU detection, setup validation
    └── logging.py       # Structured logging

tests/
├── contract/           # API/interface tests
├── integration/        # End-to-end pipeline tests
├── model/              # Model accuracy/precision tests
└── unit/               # Component tests

data/
├── raw/                # Original UFCStats data, videos
├── processed/          # Normalized videos, segments
├── models/             # Git LFS tracked model files
└── fixtures/           # Test data samples

notebooks/
├── exploration/        # Data exploration notebooks
├── experiments/        # ML experiments
└── templates/          # Notebook templates

docs/
├── README.md           # Project documentation
├── setup/              # Setup guides
└── api/                # API documentation

scripts/
├── setup/              # Environment setup scripts
│   ├── bootstrap.sh    # Conda environment creation
│   └── init_dirs.py    # Directory structure initialization
└── runners/            # Pipeline execution scripts
    ├── ufcscrape_runner.py
    └── video_preprocess_runner.py
```

**Structure Decision**: Foundation Infrastructure (data processing + environment setup)

## Phase 0: Research & Model Architecture
1. **Extract unknowns from Technical Context**:
   - All technical requirements clearly specified in feature spec
   - No NEEDS CLARIFICATION items remain

2. **Research findings**:
   - RTX 3090 supports PyTorch 2.1+ with CUDA 12.1
   - UFCStats scraping requires requests/BeautifulSoup4
   - Video processing pipeline needs OpenCV and FFmpeg
   - Git LFS recommended for large video/model files
   - Conda environment isolation best practice for ML projects

**Output**: research.md with all requirements validated

## Phase 1: Design & Model Contracts
*Prerequisites: research.md complete*

1. **Extract entities from feature spec** → `data-model.md`:
   - Input data: UFCStats pages, fight videos (MP4/MKV)
   - Processing outputs: structured stats, normalized video segments
   - Configuration: environment settings, directory paths

2. **Generate contracts** from functional requirements:
   - UFCStats scraper interface (input: URL patterns, output: structured data)
   - Video preprocessing interface (input: video files, output: normalized segments)
   - Environment validation interface (input: system info, output: capability report)

3. **Generate contract tests**:
   - UFCStats scraping contract tests
   - Video processing contract tests
   - Environment detection contract tests

4. **Extract validation scenarios**:
   - Environment setup validation
   - Data ingestion pipeline validation
   - Video processing pipeline validation

5. **Update documentation**:
   - Quickstart guide for new developers
   - API documentation for CLI interfaces
   - Environment setup instructions

**Output**: data-model.md, /contracts/*, failing tests, quickstart.md, updated CLAUDE.md

## Phase 2: Task Planning Approach
*This section describes what the /tasks command will do - DO NOT execute during /plan*

**Task Generation Strategy**:
- Load `/templates/tasks-template.md` as infrastructure setup base
- Generate tasks from Phase 1 design docs
- Each contract → validation test task [P]
- Each directory → structure creation task
- Each dependency → environment setup task
- Each pipeline → runner script task

**Infrastructure-Specific Ordering**:
- Environment setup before anything else
- Directory structure creation before data processing
- Contract tests before implementation
- Data ingestion before video processing
- Documentation throughout

**Estimated Output**: 25-35 numbered, ordered tasks in tasks.md

**IMPORTANT**: This phase is executed by the /tasks command, NOT by /plan

## Phase 3+: Future Implementation
*These phases are beyond the scope of the /plan command*

**Phase 3**: Task execution (/tasks command creates tasks.md)  
**Phase 4**: Implementation (environment setup, data pipelines following constitutional principles)  
**Phase 5**: Validation (functionality tests, performance benchmarks, quickstart validation)

## Complexity Tracking
*No constitution violations - all design decisions align with simplicity and library-first principles*

## Progress Tracking
*This checklist is updated during execution flow*

**Phase Status**:
- [x] Phase 0: Research complete (/plan command)
- [x] Phase 1: Design complete (/plan command)
- [x] Phase 2: Task planning complete (/plan command - describe approach only)
- [ ] Phase 3: Tasks generated (/tasks command)
- [ ] Phase 4: Implementation complete
- [ ] Phase 5: Validation passed

**Gate Status**:
- [x] Initial Constitution Check: PASS
- [x] Post-Design Constitution Check: PASS
- [x] All NEEDS CLARIFICATION resolved
- [x] ML complexity deviations documented

**Model Validation Gates**:
- [x] Training data requirements identified
- [x] Performance targets validated as achievable
- [x] Model architecture selected and justified
- [x] Privacy/compliance requirements addressed

---
*Based on MMA Analytics Constitution v1.0.0 - Infrastructure Setup Foundation*