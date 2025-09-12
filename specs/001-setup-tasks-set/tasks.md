# Tasks: Project Foundation Setup

**Input**: Design documents from `/specs/001-setup-tasks-set/`  
**Prerequisites**: plan.md, research.md, data-model.md, contracts/  
**Branch**: `001-setup-tasks-set` | **Date**: 2025-09-12

## Execution Flow (main)
```
1. Load plan.md from feature directory
   → Infrastructure foundation setup with ML pipeline structure
2. Load design documents:
   → data-model.md: Fighter/bout/video entities → data processing tasks
   → contracts/: UFCStats/video/environment schemas → validation test tasks
   → research.md: PyTorch/CUDA decisions → environment setup tasks
3. Generate tasks by infrastructure category:
   → Setup: Environment validation, Git LFS, directory structure
   → Tests: Contract tests, integration tests, performance tests
   → Core: UFCStats scraping, video preprocessing, CLI interfaces
   → Integration: End-to-end pipelines, GPU optimization
   → Polish: Documentation, validation guides
4. Apply infrastructure task rules:
   → Different libraries = mark [P] for parallel (ingest, video, utils)
   → Same file/module = sequential (no [P])
   → Tests before implementation (TDD for infrastructure)
5. Number tasks sequentially (T001, T002...)
6. Generate infrastructure dependency graph
7. Create parallel execution examples
8. Validate infrastructure completeness:
   → All contracts have validation tests?
   → All libraries have CLI interfaces?
   → All performance targets specified?
9. Return: SUCCESS (tasks ready for execution)
```

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different libraries, no shared dependencies)
- Include exact file paths and acceptance criteria in descriptions

## Path Conventions for Infrastructure Setup
- **Core Libraries**: `src/ingest/`, `src/video/`, `src/utils/` at repository root
- **Data**: `data/raw/`, `data/processed/`, `data/models/` (Git LFS managed)
- **Tests**: `tests/contract/`, `tests/integration/`, `tests/unit/`
- **Scripts**: `scripts/setup/`, `scripts/runners/`
- **Documentation**: `docs/`, `specs/001-setup-tasks-set/`

## Phase 3.1: Setup & Infrastructure Foundation
- [ ] **T001** Complete Git LFS configuration for video/model files in `.gitattributes`
  - *AC: Git LFS tracking configured for *.mp4, *.mkv, *.pt, *.pth files*
  - *Est: 15 min | File: `.gitattributes`*
- [ ] **T002** [P] Validate conda environment setup with all dependencies in `environment.yml`
  - *AC: All 40+ packages install successfully, PyTorch CUDA functional*
  - *Est: 20 min | File: `environment.yml`*
- [ ] **T003** [P] Complete environment validation with GPU detection in `src/utils/environment.py`
  - *AC: RTX 3090 detected, CUDA 12.1 functional, memory monitoring working*
  - *Est: 30 min | File: `src/utils/environment.py`*
- [ ] **T004** Complete directory structure initialization in `scripts/setup/init_dirs.py`
  - *AC: All data/, src/, tests/, notebooks/, docs/ directories created*
  - *Est: 20 min | File: `scripts/setup/init_dirs.py`*
- [ ] **T005** Create bootstrap script for environment setup in `scripts/setup/bootstrap.sh`
  - *AC: One-command environment setup with validation*
  - *Est: 25 min | File: `scripts/setup/bootstrap.sh`*

## Phase 3.2: Contract & Integration Tests (TDD) ⚠️ MUST COMPLETE BEFORE 3.3
**CRITICAL: These tests MUST be written and MUST FAIL before ANY implementation**
- [ ] **T006** [P] UFCStats scraping contract test in `tests/contract/test_ufcscrape.py`
  - *AC: Test validates input schema, output format, error handling*
  - *Est: 20 min | File: `tests/contract/test_ufcscrape.py`*
- [ ] **T007** [P] Video preprocessing contract test in `tests/contract/test_video_preprocess.py`
  - *AC: Test validates video input/output, processing options, performance*
  - *Est: 25 min | File: `tests/contract/test_video_preprocess.py`*
- [ ] **T008** [P] Environment detection contract test in `tests/contract/test_environment.py`
  - *AC: Test validates GPU detection, CUDA functionality, memory validation*
  - *Est: 15 min | File: `tests/contract/test_environment.py`*
- [ ] **T009** [P] Integration test for UFCStats data pipeline in `tests/integration/test_ufc_pipeline.py`
  - *AC: End-to-end UFCStats scraping with real data validation*
  - *Est: 30 min | File: `tests/integration/test_ufc_pipeline.py`*
- [ ] **T010** [P] Integration test for video processing pipeline in `tests/integration/test_video_pipeline.py`
  - *AC: End-to-end video processing with 25+ FPS performance target*
  - *Est: 35 min | File: `tests/integration/test_video_pipeline.py`*
- [ ] **T011** Performance test for GPU processing in `tests/model/test_gpu_performance.py`
  - *AC: Validates 25-30 FPS processing, <16GB memory usage*
  - *Est: 25 min | File: `tests/model/test_gpu_performance.py`*

## Phase 3.3: Core Library Implementation (ONLY after tests are failing)
- [ ] **T012** UFCStats scraping library in `src/ingest/ufcscrape.py`
  - *AC: Fighter/bout/event scraping, JSON/CSV output, error handling*
  - *Est: 45 min | File: `src/ingest/ufcscrape.py`*
- [ ] **T013** [P] UFCStats data models in `src/ingest/models/`
  - *AC: Fighter, Bout, Event models with validation and serialization*
  - *Est: 30 min | Files: `src/ingest/models/fighter.py`, `src/ingest/models/bout.py`*
- [ ] **T014** Video preprocessing library in `src/video/preprocessing.py`
  - *AC: Video normalization, format validation, segmentation support*
  - *Est: 50 min | File: `src/video/preprocessing.py`*
- [ ] **T015** [P] Video format utilities in `src/video/formats/`
  - *AC: Format detection, validation, conversion utilities*
  - *Est: 25 min | Files: `src/video/formats/validator.py`, `src/video/formats/converter.py`*
- [ ] **T016** Enhanced logging utilities in `src/utils/logging.py`
  - *AC: Structured JSON logging with component context*
  - *Est: 20 min | File: `src/utils/logging.py`*
- [ ] **T017** [P] CLI interface for UFCStats scraping in `src/ingest/cli.py`
  - *AC: --help/--version/--format json support, all scraping options*
  - *Est: 30 min | File: `src/ingest/cli.py`*
- [ ] **T018** [P] CLI interface for video preprocessing in `src/video/cli.py`
  - *AC: --help/--version/--format json support, all processing options*
  - *Est: 30 min | File: `src/video/cli.py`*
- [ ] **T019** Configuration management in `src/utils/config.py`
  - *AC: Environment-based config, validation, default values*
  - *Est: 25 min | File: `src/utils/config.py`*

## Phase 3.4: Runner Scripts & Integration
- [ ] **T020** UFCStats scraping runner in `scripts/runners/ufcscrape_runner.py`
  - *AC: Complete scraping pipeline with progress tracking and error recovery*
  - *Est: 40 min | File: `scripts/runners/ufcscrape_runner.py`*
- [ ] **T021** Video preprocessing runner in `scripts/runners/video_preprocess_runner.py`
  - *AC: Complete video processing pipeline with GPU optimization*
  - *Est: 45 min | File: `scripts/runners/video_preprocess_runner.py`*
- [ ] **T022** [P] Data validation utilities in `src/utils/validation.py`
  - *AC: Schema validation, data integrity checks, error reporting*
  - *Est: 30 min | File: `src/utils/validation.py`*
- [ ] **T023** GPU optimization and memory management in `src/video/gpu_utils.py`
  - *AC: Memory monitoring, batch sizing, optimization strategies*
  - *Est: 35 min | File: `src/video/gpu_utils.py`*
- [ ] **T024** End-to-end pipeline integration in `src/utils/pipeline.py`
  - *AC: Unified pipeline interface with error handling and monitoring*
  - *Est: 40 min | File: `src/utils/pipeline.py`*

## Phase 3.5: Documentation & Polish
- [ ] **T025** [P] Complete setup guide in `docs/setup/README.md`
  - *AC: Step-by-step setup instructions, troubleshooting, validation*
  - *Est: 30 min | File: `docs/setup/README.md`*
- [ ] **T026** [P] API documentation in `docs/api/README.md`
  - *AC: Complete API reference for all libraries and CLI interfaces*
  - *Est: 35 min | File: `docs/api/README.md`*
- [ ] **T027** Data processing guide in `docs/processing/README.md`
  - *AC: UFCStats scraping, video processing, data organization guide*
  - *Est: 25 min | File: `docs/processing/README.md`*
- [ ] **T028** Jupyter notebook templates in `notebooks/templates/`
  - *AC: Data exploration, ML experiments, analysis templates*
  - *Est: 30 min | Files: `notebooks/templates/exploration.ipynb`, `notebooks/templates/analysis.ipynb`*
- [ ] **T029** [P] Unit tests for core utilities in `tests/unit/`
  - *AC: Complete unit test coverage for utils, models, and helpers*
  - *Est: 40 min | Files: `tests/unit/test_utils.py`, `tests/unit/test_models.py`*
- [ ] **T030** Final validation and integration test suite
  - *AC: All tests passing, performance targets met, documentation complete*
  - *Est: 45 min | Command: `pytest --cov=src --cov-report=html`*

## Dependencies
- Tests (T006-T011) before implementation (T012-T019)
- Environment setup (T001-T005) before all other tasks
- Core libraries (T012-T019) before runners (T020-T024)
- Integration (T020-T024) before polish (T025-T030)
- All tasks before final validation (T030)

## Parallel Example for Infrastructure Workflows
```
# Launch independent contract tests together:
Task: "UFCStats scraping contract test in tests/contract/test_ufcscrape.py"
Task: "Video preprocessing contract test in tests/contract/test_video_preprocess.py"  
Task: "Environment detection contract test in tests/contract/test_environment.py"

# Launch independent library implementations together:
Task: "UFCStats scraping library in src/ingest/ufcscrape.py"
Task: "Video preprocessing library in src/video/preprocessing.py"
Task: "Enhanced logging utilities in src/utils/logging.py"

# Launch independent CLI interfaces together:
Task: "CLI interface for UFCStats scraping in src/ingest/cli.py"
Task: "CLI interface for video preprocessing in src/video/cli.py"
Task: "Configuration management in src/utils/config.py"
```

## Milestone Mapping

### M1: Repository + Environment (T001-T005)
- Git LFS configuration
- Environment validation  
- Directory structure
- Bootstrap script

### M2: Data Ingestion - UFCStats (T006, T009, T012, T013, T017, T020)
- Contract tests
- Scraping library and models
- CLI interface
- Runner script
- Integration tests

### M3: Video Preprocessing (T007, T008, T010, T011, T014-T016, T018, T021, T023)
- Contract and performance tests
- Video processing library
- Format utilities
- GPU optimization
- CLI interface and runner

### M4: Documentation + Validation (T019, T022, T024-T030)
- Configuration and utilities
- Complete documentation
- Notebook templates
- Final validation

## Notes for Infrastructure Development
- [P] tasks = different libraries/files, no shared dependencies
- Verify contract tests fail before implementing libraries
- Use structured JSON logging throughout
- Follow library-first architecture with CLI interfaces
- Include GPU memory monitoring in performance tests
- Ensure all components work offline (no cloud dependencies)

## Task Generation Rules for Infrastructure Setup
*Applied during main() execution*

1. **From Model Contracts**:
   - Each schema → contract validation test [P]
   - Each performance target → performance test task [P]
   
2. **From Data Model**:
   - Each entity → model creation task [P]
   - Each data source → processing pipeline task
   
3. **From User Stories**:
   - Each workflow → integration test [P]
   - Each CLI requirement → interface task [P]

4. **Infrastructure-Specific Ordering**:
   - Setup → Tests → Libraries → Runners → Integration → Documentation
   - Independent libraries can be developed in parallel
   - Shared utilities block dependent components

## Validation Checklist for Infrastructure Tasks
*GATE: Checked by main() before returning*

- [ ] All contracts have corresponding validation tests
- [ ] All libraries have CLI interfaces
- [ ] All tests come before implementation (TDD)
- [ ] Performance targets specified in test tasks
- [ ] Parallel tasks use independent libraries
- [ ] Each task specifies exact file path and acceptance criteria
- [ ] GPU memory constraints considered in task planning
- [ ] Git LFS and environment setup validated
- [ ] Documentation included for all components

## PR Checklist Template

```markdown
## PR Checklist

### Milestone Completion
- [ ] M1: Repository + Environment setup complete
- [ ] M2: UFCStats data ingestion pipeline working
- [ ] M3: Video preprocessing pipeline functional  
- [ ] M4: Documentation and validation complete

### Core Requirements
- [ ] All contract tests implemented and passing
- [ ] All library CLI interfaces functional
- [ ] Performance targets met (25+ FPS, <30 min scraping)
- [ ] Git LFS properly configured for large files
- [ ] Environment validation working for RTX 3090

### Testing & Validation
- [ ] Contract tests: `pytest tests/contract/`
- [ ] Integration tests: `pytest tests/integration/`
- [ ] Performance tests: `pytest tests/model/`
- [ ] Unit tests: `pytest tests/unit/`
- [ ] Coverage report: `pytest --cov=src`

### Documentation
- [ ] Quickstart guide updated and tested
- [ ] API documentation complete
- [ ] Setup guide validated
- [ ] Jupyter templates provided
```

---
*Task generation complete - Ready for execution*