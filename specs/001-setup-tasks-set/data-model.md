# Data Model: Project Foundation Setup

**Branch**: `001-setup-tasks-set` | **Date**: 2025-09-12
**Purpose**: Data entities and relationships for infrastructure setup

## Core Data Entities

### 1. UFCStats Data

#### Fighter Record
```json
{
  "fighter_id": "string",
  "name": "string",
  "nickname": "string|null",
  "weight_class": "string",
  "record": {
    "wins": "integer",
    "losses": "integer",
    "draws": "integer",
    "no_contests": "integer"
  },
  "physical_attributes": {
    "height": "string|null",
    "weight": "string|null",
    "reach": "string|null",
    "stance": "string|null"
  },
  "career_stats": {
    "significant_strikes_landed_per_minute": "float|null",
    "significant_striking_accuracy": "float|null",
    "significant_strike_defense": "float|null",
    "takedown_average": "float|null",
    "takedown_accuracy": "float|null",
    "takedown_defense": "float|null",
    "submission_attempt_average": "float|null"
  },
  "last_updated": "datetime"
}
```

#### Bout Record
```json
{
  "bout_id": "string",
  "event_id": "string",
  "event_name": "string",
  "date": "date",
  "location": "string",
  "weight_class": "string",
  "title_fight": "boolean",
  "fighters": {
    "fighter1": {
      "fighter_id": "string",
      "name": "string",
      "result": "string", // "win", "loss", "draw", "no_contest"
      "method": "string|null", // "KO/TKO", "submission", "decision"
      "round": "integer|null",
      "time": "string|null", // "MM:SS"
      "time_format": "string|null" // "5R", "3R", etc.
    },
    "fighter2": {
      "fighter_id": "string",
      "name": "string",
      "result": "string",
      "method": "string|null",
      "round": "integer|null",
      "time": "string|null",
      "time_format": "string|null"
    }
  },
  "fight_stats": {
    "fighter1": {
      "significant_strikes_landed": "integer",
      "significant_strikes_attempted": "integer",
      "total_strikes_landed": "integer",
      "total_strikes_attempted": "integer",
      "takedowns_landed": "integer",
      "takedowns_attempted": "integer",
      "submissions_attempted": "integer",
      "knockdowns": "integer"
    },
    "fighter2": {
      "significant_strikes_landed": "integer",
      "significant_strikes_attempted": "integer",
      "total_strikes_landed": "integer",
      "total_strikes_attempted": "integer",
      "takedowns_landed": "integer",
      "takedowns_attempted": "integer",
      "submissions_attempted": "integer",
      "knockdowns": "integer"
    }
  },
  "last_updated": "datetime"
}
```

### 2. Video Data

#### Video Metadata
```json
{
  "video_id": "string",
  "bout_id": "string",
  "event_id": "string",
  "filename": "string",
  "file_path": "string",
  "file_size_bytes": "integer",
  "duration_seconds": "float",
  "format": "string", // "mp4", "mkv"
  "resolution": {
    "width": "integer",
    "height": "integer"
  },
  "frame_rate": "float",
  "bitrate": "integer",
  "codec": "string",
  "audio_codec": "string|null",
  "created_date": "datetime",
  "processed_date": "datetime|null",
  "processing_status": "string", // "raw", "processing", "processed", "error"
  "checksum": "string|null"
}
```

#### Video Segment
```json
{
  "segment_id": "string",
  "video_id": "string",
  "bout_id": "string",
  "segment_type": "string", // "full_fight", "round", "highlight", "technique"
  "start_time_seconds": "float",
  "end_time_seconds": "float",
  "duration_seconds": "float",
  "file_path": "string",
  "file_size_bytes": "integer",
  "resolution": {
    "width": "integer",
    "height": "integer"
  },
  "frame_rate": "float",
  "processing_date": "datetime",
  "quality_metrics": {
    "resolution_normalized": "boolean",
    "frame_rate_normalized": "boolean",
    "audio_synced": "boolean"
  }
}
```

### 3. Processing Metadata

#### Environment Configuration
```json
{
  "config_id": "string",
  "timestamp": "datetime",
  "system_info": {
    "platform": "string",
    "python_version": "string",
    "cuda_version": "string|null",
    "gpu_info": {
      "name": "string",
      "memory_total_gb": "float",
      "memory_available_gb": "float",
      "cuda_cores": "integer"
    }|null
  },
  "package_versions": {
    "torch": "string",
    "torchvision": "string",
    "opencv": "string",
    "pandas": "string",
    "numpy": "string",
    "scikit_learn": "string"
  },
  "validation_results": {
    "gpu_available": "boolean",
    "cuda_functional": "boolean",
    "memory_sufficient": "boolean",
    "dependencies_installed": "boolean"
  }
}
```

#### Processing Job
```json
{
  "job_id": "string",
  "job_type": "string", // "ufcstats_scrape", "video_preprocess"
  "status": "string", // "pending", "running", "completed", "error"
  "input_path": "string",
  "output_path": "string",
  "parameters": {
    "batch_size": "integer|null",
    "resolution_target": "string|null",
    "frame_rate_target": "float|null"
  },
  "start_time": "datetime|null",
  "end_time": "datetime|null",
  "duration_seconds": "float|null",
  "items_processed": "integer",
  "items_total": "integer",
  "error_message": "string|null",
  "performance_metrics": {
    "processing_fps": "float|null",
    "memory_usage_mb": "float|null",
    "gpu_usage_percent": "float|null"
  }
}
```

## Data Relationships

### UFCStats Data Flow
```
Fighter Records ←→ Bout Records ←→ Video Files
      ↓                  ↓              ↓
  Fighter Stats ←→ Fight Stats ←→ Video Segments
```

### Processing Pipeline Flow
```
Raw UFCStats → Scraped JSON → Structured CSV → ML Ready
Raw Videos → Preprocessed → Segmented → Analysis Ready
```

## Directory Structure Mapping

### Data Organization
```
data/
├── raw/
│   ├── ufcstats/           # Scraped JSON files
│   │   ├── fighters/
│   │   ├── bouts/
│   │   └── events/
│   └── videos/             # Original video files
│       ├── events/
│       │   └── {event_id}/
│       │       ├── {bout_id}.mp4
│       │       └── metadata.json
│       └── fighters/
│           └── {fighter_id}/
├── processed/
│   ├── ufcstats/          # Cleaned/normalized data
│   │   ├── fighters.csv
│   │   ├── bouts.csv
│   │   └── fight_stats.csv
│   └── videos/            # Processed video segments
│       ├── segments/
│       │   ├── full_fights/
│       │   ├── rounds/
│       │   └── highlights/
│       └── thumbnails/
├── models/                 # Trained ML models (Git LFS)
│   ├── checkpoints/
│   ├── embeddings/
│   └── classifiers/
└── fixtures/              # Test data samples
    ├── sample_videos/
    └── sample_stats/
```

## Data Validation Rules

### UFCStats Validation
- **Fighter ID**: Must be unique across all records
- **Bout ID**: Must be unique and reference existing fighters
- **Dates**: Must be valid dates in historical range
- **Statistics**: Must be non-negative integers where applicable
- **Percentages**: Must be between 0-100 for accuracy stats

### Video Validation
- **File Format**: Must be MP4 or MKV
- **Resolution**: Must be between 480p and 4K
- **Frame Rate**: Must be between 24-60 FPS
- **Duration**: Must be >0 seconds for fights
- **Checksum**: Must match file integrity

### Processing Validation
- **Environment**: GPU must be detected and functional
- **Memory**: Sufficient memory available for processing
- **Output**: All generated files must be valid and accessible
- **Performance**: Must meet minimum FPS requirements

## Data Access Patterns

### Read Operations
- **Fighter Lookup**: By fighter ID or name
- **Bout History**: By fighter ID or date range
- **Video Retrieval**: By bout ID or event ID
- **Segment Access**: By video ID and time range

### Write Operations
- **Stats Updates**: Incremental updates from UFCStats
- **Video Processing**: Batch processing of raw videos
- **Model Training**: Output trained model checkpoints
- **Job Logging**: Processing job status and metrics

## Data Security and Privacy

### Access Control
- **Local Only**: All data processing occurs locally
- **File Permissions**: Standard filesystem permissions
- **No Cloud**: No external data transmission

### Data Integrity
- **Checksums**: MD5/SHA256 for large files
- **Validation**: Format and content validation
- **Backups**: Git version control for configuration

---
*Data model complete - Ready for contract generation*