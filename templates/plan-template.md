# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

## Execution Flow (/plan command scope)
```
1. Load feature spec from Input path
   → If not found: ERROR "No feature spec at {path}"
2. Fill Technical Context (scan for NEEDS CLARIFICATION)
   → Detect Project Type: ml-pipeline/video-processing/stats-analysis/reporting
   → Set Structure Decision based on ML workflow type
3. Evaluate Constitution Check section below
   → If violations exist: Document in Complexity Tracking
   → If no justification possible: ERROR "Simplify approach first"
   → Update Progress Tracking: Initial Constitution Check
4. Execute Phase 0 → research.md
   → If NEEDS CLARIFICATION remain: ERROR "Resolve unknowns"
5. Execute Phase 1 → contracts, data-model.md, quickstart.md, CLAUDE.md
6. Re-evaluate Constitution Check section
   → If new violations: Refactor design, return to Phase 1
   → Update Progress Tracking: Post-Design Constitution Check
7. Plan Phase 2 → Describe task generation approach (DO NOT create tasks.md)
8. STOP - Ready for /tasks command
```

**IMPORTANT**: The /plan command STOPS at step 7. Phases 2-4 are executed by other commands.

## Summary
[Extract from feature spec: primary requirement + ML approach from research]

## Technical Context
**Language/Version**: [e.g., Python 3.11, PyTorch 2.1 or NEEDS CLARIFICATION]  
**ML Framework**: [e.g., PyTorch, scikit-learn, OpenCV or NEEDS CLARIFICATION]  
**Model Architecture**: [e.g., VideoMAE-S, XGBoost, ResNet or NEEDS CLARIFICATION]  
**Data Pipeline**: [e.g., video preprocessing, feature engineering or NEEDS CLARIFICATION]  
**Storage**: [e.g., local files, HDF5, parquet or NEEDS CLARIFICATION]  
**Testing**: [e.g., pytest + model validation, accuracy thresholds or NEEDS CLARIFICATION]  
**Target Platform**: [e.g., RTX 3090 local, offline processing or NEEDS CLARIFICATION]
**Project Type**: [ml-pipeline/video-processing/stats-analysis/reporting]  
**Performance Goals**: [e.g., 85% precision, 25 FPS processing, <200ms inference or NEEDS CLARIFICATION]  
**Model Constraints**: [e.g., <16GB GPU memory, offline-only, reproducible or NEEDS CLARIFICATION]  
**Data Scale**: [e.g., 1000 fights, 10GB videos, 50k samples or NEEDS CLARIFICATION]

## Constitution Check
*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Simplicity**:
- Projects: [#] (max 3 - core, notebooks, tools)
- Using frameworks directly? (PyTorch/OpenCV, no ML wrappers)
- Single data model? (no DTOs unless formats differ)
- Avoiding patterns? (no Repository/UoW without proven ML need)

**Library-First Architecture**:
- EVERY feature as library? (independent, testable modules)
- Libraries listed: [name + ML purpose for each]
- CLI per library: [commands with --help/--version/--format json]
- Library docs: llms.txt format planned?

**Testing (NON-NEGOTIABLE)**:
- RED-GREEN-Refactor cycle enforced? (test MUST fail first)
- Model validation included? (accuracy/precision thresholds)
- Order: Contract→Integration→Model→Unit strictly followed?
- Real data used? (actual video files, not synthetic)
- Integration tests for: new models, data pipelines, accuracy regressions?
- FORBIDDEN: Training before tests, skipping validation

**ML Observability**:
- Structured logging included? (training metrics, inference times)
- Model versioning tracked? (architecture, data, performance)
- Error context sufficient? (frame numbers, confidence scores)
- Performance monitoring? (GPU memory, processing speed)

**Data Management**:
- Reproducibility ensured? (seeds, data splits, versions)
- Privacy compliant? (local-only UFC footage)
- Version control? (datasets, model checkpoints)

## Project Structure

### Documentation (this feature)
```
specs/[###-feature]/
├── plan.md              # This file (/plan command output)
├── research.md          # Phase 0 output (/plan command)
├── data-model.md        # Phase 1 output (/plan command)
├── quickstart.md        # Phase 1 output (/plan command)
├── contracts/           # Phase 1 output (/plan command)
└── tasks.md             # Phase 2 output (/tasks command - NOT created by /plan)
```

### Source Code (repository root)
```
# ML Pipeline Structure (DEFAULT for MMA Analytics)
src/
├── video/              # Video processing libraries
│   ├── preprocessing/
│   ├── pose_estimation/
│   ├── strike_detection/
│   └── action_recognition/
├── stats/              # Statistics libraries
│   ├── data_ingestion/
│   ├── feature_engineering/
│   └── prediction_models/
├── commentary/         # Commentary analysis libraries
│   ├── asr/
│   ├── diarization/
│   └── claim_extraction/
├── analytics/          # Higher-level analytics
│   ├── combo_analysis/
│   ├── vulnerability_mining/
│   └── style_inference/
└── reporting/          # Output generation
    ├── jupyter_reports/
    └── clip_generation/

tests/
├── contract/           # API/interface tests
├── integration/        # End-to-end pipeline tests
├── model/              # Model accuracy/precision tests
└── unit/               # Component tests

data/
├── raw/                # Original data (videos, stats)
├── processed/          # Cleaned/normalized data
├── models/             # Trained model checkpoints
├── clips/              # Generated highlight clips
└── fixtures/           # Test data samples
```

**Structure Decision**: ML Pipeline (video + stats + analytics libraries)

## Phase 0: Research & Model Architecture
1. **Extract unknowns from Technical Context** above:
   - For each NEEDS CLARIFICATION → research task
   - For each ML component → architecture/benchmark task
   - For each performance target → feasibility task

2. **Generate and dispatch research agents**:
   ```
   For each unknown in Technical Context:
     Task: "Research {ML component} for {MMA context}"
   For each model choice:
     Task: "Find best practices for {model} in {video/stats domain}"
   For each performance target:
     Task: "Validate {metric} achievability with {constraints}"
   ```

3. **Consolidate findings** in `research.md` using format:
   - Model Decision: [architecture chosen]
   - Performance Rationale: [why achievable with constraints]
   - Data Requirements: [what data needed]
   - Alternatives considered: [what else evaluated]

**Output**: research.md with all NEEDS CLARIFICATION resolved

## Phase 1: Design & Model Contracts
*Prerequisites: research.md complete*

1. **Extract entities from feature spec** → `data-model.md`:
   - Input data: video frames, stats records, audio segments
   - Model outputs: predictions, confidence scores, timestamps
   - Training data: labeled examples, validation splits
   - Inference data: preprocessing steps, normalization

2. **Generate model contracts** from functional requirements:
   - For each prediction → input/output schema
   - For each model → training/inference interface
   - Use standard ML patterns (sklearn-like fit/predict)
   - Output schemas to `/contracts/` (JSON Schema format)

3. **Generate contract tests** from model contracts:
   - One test file per model interface
   - Assert input validation, output formats
   - Include accuracy/precision thresholds
   - Tests must fail (no implementation yet)

4. **Extract validation scenarios** from user stories:
   - Each story → integration test with real data
   - Quickstart = end-to-end pipeline validation

5. **Update agent file incrementally**:
   - Add new ML technologies and libraries
   - Include model architecture details
   - Update performance targets and constraints

**Output**: data-model.md, /contracts/*, failing tests, quickstart.md, CLAUDE.md

## Phase 2: Task Planning Approach
*This section describes what the /tasks command will do - DO NOT execute during /plan*

**Task Generation Strategy**:
- Load `/templates/tasks-template.md` as ML-specific base
- Generate tasks from Phase 1 design docs
- Each model contract → validation test task [P]
- Each data pipeline → preprocessing task [P]
- Each training script → model training task
- Each inference pipeline → performance test task

**ML-Specific Ordering**:
- TDD order: Tests before training/implementation
- Data flow: Preprocessing before training before inference
- Dependencies: Models before analytics before reporting
- Mark [P] for parallel execution (independent models/data)

**Estimated Output**: 30-40 numbered, ordered tasks in tasks.md

**IMPORTANT**: This phase is executed by the /tasks command, NOT by /plan

## Phase 3+: Future Implementation
*These phases are beyond the scope of the /plan command*

**Phase 3**: Task execution (/tasks command creates tasks.md)  
**Phase 4**: Implementation (train models, build pipelines following constitutional principles)  
**Phase 5**: Validation (accuracy tests, performance benchmarks, quickstart validation)

## Complexity Tracking
*Fill ONLY if Constitution Check has violations that must be justified*

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [specific ML need] | [why 3 projects insufficient for ML pipeline] |
| [e.g., Wrapper classes] | [model ensemble need] | [why direct framework access insufficient] |

## Progress Tracking
*This checklist is updated during execution flow*

**Phase Status**:
- [ ] Phase 0: Research complete (/plan command)
- [ ] Phase 1: Design complete (/plan command)
- [ ] Phase 2: Task planning complete (/plan command - describe approach only)
- [ ] Phase 3: Tasks generated (/tasks command)
- [ ] Phase 4: Implementation complete
- [ ] Phase 5: Validation passed

**Gate Status**:
- [ ] Initial Constitution Check: PASS
- [ ] Post-Design Constitution Check: PASS
- [ ] All NEEDS CLARIFICATION resolved
- [ ] ML complexity deviations documented

**Model Validation Gates**:
- [ ] Training data requirements identified
- [ ] Performance targets validated as achievable
- [ ] Model architecture selected and justified
- [ ] Privacy/compliance requirements addressed

---
*Based on MMA Analytics Constitution v1.0.0 - See `/memory/constitution.md`*