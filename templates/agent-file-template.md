# MMA Analytics Development Guidelines

Auto-generated from all feature plans. Last updated: [DATE]

## Active Technologies
- Python 3.11 + PyTorch 2.1 (GPU ML framework)
- OpenCV + MediaPipe (computer vision)
- scikit-learn + XGBoost (stats modeling)
- FFmpeg + moviepy (video processing)
- Jupyter + matplotlib/plotly (analysis/reporting)
[EXTRACTED FROM ALL PLAN.MD FILES]

## Project Structure
```
src/
├── video/              # Video processing libraries
│   ├── preprocessing/  # Video normalization, segmentation
│   ├── pose_estimation/# MediaPipe pose extraction
│   ├── strike_detection/# VideoMAE-based strike classification
│   └── action_recognition/# Combo and sequence analysis
├── stats/              # Statistics libraries  
│   ├── data_ingestion/ # UFCStats scraping and cleaning
│   ├── feature_engineering/# Fight metrics, odds processing
│   └── prediction_models/# XGBoost fight outcome prediction
├── commentary/         # Commentary analysis libraries
│   ├── asr/           # Whisper speech-to-text
│   ├── diarization/   # Speaker separation
│   └── claim_extraction/# NLP claim mining
├── analytics/          # Higher-level analytics
│   ├── combo_analysis/# N-gram strike patterns
│   ├── vulnerability_mining/# Guard state correlations
│   └── style_inference/# Boxing/kickboxing/karate classification
└── reporting/          # Output generation
    ├── jupyter_reports/# Interactive analysis notebooks
    └── clip_generation/# Highlight video export

tests/
├── contract/          # Model interface validation
├── integration/       # End-to-end pipeline tests
├── model/            # Accuracy/performance thresholds
└── unit/             # Component-level tests

data/
├── raw/              # UFC videos, stats CSV files
├── processed/        # Normalized video, cleaned datasets
├── models/           # Trained model checkpoints
└── fixtures/         # Test data samples
[ACTUAL STRUCTURE FROM PLANS]
```

## Commands
```bash
# Core ML Pipeline Commands
cd src/video && python -m strike_detection.cli --video input.mp4 --format json
cd src/stats && python -m prediction_models.cli --features stats.csv --output predictions.json
cd src/analytics && python -m combo_analysis.cli --strikes strikes.json --format csv

# Testing Commands  
pytest tests/contract/ -v                    # Model interface tests
pytest tests/model/ -v                       # Accuracy threshold tests
pytest tests/integration/ -v                 # End-to-end pipeline tests

# Training Commands
python src/video/strike_detection/train_model.py --config config.yaml
python src/stats/prediction_models/train_xgboost.py --data processed_stats.csv

# GPU Environment
nvidia-smi                                   # Check GPU status
python -c "import torch; print(torch.cuda.is_available())"  # Verify PyTorch GPU

# Data Processing
ffmpeg -i input.mp4 -vf scale=720:480 -r 25 normalized.mp4  # Video normalization
python scripts/scrape_ufc_stats.py --output data/raw/      # Stats collection
[ONLY COMMANDS FOR ACTIVE TECHNOLOGIES]
```

## Code Style
**Python**: Follow PEP 8, use black formatter, type hints required
- ML Models: sklearn-like fit/predict interface, save/load methods
- Video Processing: OpenCV + numpy arrays, consistent frame ordering
- Data Pipeline: pandas DataFrames, reproducible transforms with seeds
- CLI Tools: Click framework, JSON output support, progress bars
- Testing: pytest fixtures, parametrized tests for model variations

**Model Development**: 
- Document architecture decisions in model cards
- Include training data requirements and performance metrics
- Use configuration files (YAML) for hyperparameters
- Version model checkpoints with metadata (accuracy, training data)

**Performance Standards**:
- Strike detection: ≥85% precision (jab/cross/hook), ≥75% (advanced techniques)
- Video processing: Real-time capable on RTX 3090 (25-30 FPS)
- Memory constraints: <16GB GPU memory for full pipeline
- Stats prediction: ≥70% accuracy, Brier score ≤0.20
[LANGUAGE-SPECIFIC, ONLY FOR LANGUAGES IN USE]

## Recent Changes
-
[LAST 3 FEATURES AND WHAT THEY ADDED]

## ML Development Workflow
1. **Specification**: Define success criteria (accuracy, speed, usefulness)
2. **Research**: Validate model architecture and performance targets  
3. **Test-First**: Write model validation tests before training
4. **Data Pipeline**: Prepare training/validation splits with no leakage
5. **Model Training**: Use reproducible seeds, track experiments
6. **Validation**: Verify accuracy thresholds, performance constraints
7. **Integration**: End-to-end pipeline testing with real UFC data
8. **Documentation**: Model cards, API docs, usage examples

## Domain Knowledge
**MMA Strike Types**: jab, cross, hook, uppercut, low kick, roundhouse kick, head kick, teep kick
**Grappling Positions**: guard, side control, mount, back control  
**Stance Types**: orthodox, southpaw, fighting stance vs neutral
**Fight Metrics**: significant strikes landed/attempted, takedowns, control time
**Video Constraints**: Single camera UFC broadcast footage, variable lighting
**Privacy Requirements**: Local processing only, no cloud uploads of UFC content

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->