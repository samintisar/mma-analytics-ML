#!/bin/bash

# MMA Analytics Environment Bootstrap Script
# Sets up conda environment, Git LFS, and validates GPU support for RTX 3090

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
ENV_NAME="mma-analytics"
ENV_FILE="$PROJECT_ROOT/environment.yml"
GITATTRIBUTES_FILE="$PROJECT_ROOT/.gitattributes"
VERBOSE=false
DRY_RUN=false
FORCE=false

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_verbose() {
    if [ "$VERBOSE" = true ]; then
        echo -e "${BLUE}[VERBOSE]${NC} $1"
    fi
}

# Help function
show_help() {
    cat << EOF
MMA Analytics Environment Bootstrap Script

USAGE: $0 [OPTIONS]

OPTIONS:
    -h, --help          Show this help message
    -v, --verbose       Enable verbose output
    -f, --force         Force environment recreation
    -d, --dry-run       Show what would be done without executing
    --skip-env          Skip conda environment creation
    --skip-lfs          Skip Git LFS setup
    --skip-validation   Skip GPU validation

DESCRIPTION:
    This script sets up the complete MMA Analytics development environment:
    - Validates Python 3.11 availability
    - Creates conda environment from environment.yml
    - Initializes Git LFS for large file tracking
    - Validates GPU support and CUDA configuration
    - Tests PyTorch GPU functionality

EXAMPLES:
    $0                           # Standard setup
    $0 --verbose --force         # Verbose output with force recreation
    $0 --dry-run                 # Show what would be done
    $0 --skip-env --skip-lfs     # Skip environment and LFS setup

REQUIREMENTS:
    - Python 3.11 or higher
    - Conda (miniconda or anaconda)
    - Git with LFS support
    - NVIDIA GPU with CUDA drivers (optional but recommended)

EXIT CODES:
    0: Success
    1: General error
    2: Missing requirements
    3: Environment creation failed
    4: GPU validation failed
EOF
}

# Parse command line arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -v|--verbose)
                VERBOSE=true
                shift
                ;;
            -f|--force)
                FORCE=true
                shift
                ;;
            -d|--dry-run)
                DRY_RUN=true
                shift
                ;;
            --skip-env)
                SKIP_ENV=true
                shift
                ;;
            --skip-lfs)
                SKIP_LFS=true
                shift
                ;;
            --skip-validation)
                SKIP_VALIDATION=true
                shift
                ;;
            *)
                log_error "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
    done
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Validate system requirements
validate_requirements() {
    log_info "Validating system requirements..."
    
    # Check Python 3.11
    if ! command_exists python3; then
        log_error "Python 3 is not installed"
        exit 2
    fi
    
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
    
    log_verbose "Found Python version: $PYTHON_VERSION"
    
    if [ "$PYTHON_MAJOR" -ne 3 ] || [ "$PYTHON_MINOR" -lt 11 ]; then
        log_error "Python 3.11 or higher is required (found: $PYTHON_VERSION)"
        exit 2
    fi
    
    log_success "Python version validated: $PYTHON_VERSION"
    
    # Check conda
    if ! command_exists conda; then
        log_error "Conda is not installed. Please install miniconda or anaconda."
        exit 2
    fi
    
    CONDA_VERSION=$(conda --version | awk '{print $2}')
    log_verbose "Found conda version: $CONDA_VERSION"
    log_success "Conda installation validated: $CONDA_VERSION"
    
    # Check git
    if ! command_exists git; then
        log_error "Git is not installed"
        exit 2
    fi
    
    GIT_VERSION=$(git --version | awk '{print $3}')
    log_verbose "Found git version: $GIT_VERSION"
    log_success "Git installation validated: $GIT_VERSION"
}

# Setup conda environment
setup_conda_environment() {
    if [ "${SKIP_ENV:-false}" = true ]; then
        log_info "Skipping conda environment setup"
        return 0
    fi
    
    log_info "Setting up conda environment..."
    
    # Check if environment.yml exists
    if [ ! -f "$ENV_FILE" ]; then
        log_error "Environment file not found: $ENV_FILE"
        exit 3
    fi
    
    # Check if environment already exists
    if conda env list | grep -q "^$ENV_NAME\s"; then
        if [ "$FORCE" = true ]; then
            log_info "Environment '$ENV_NAME' already exists, removing due to --force flag"
            if [ "$DRY_RUN" = false ]; then
                conda env remove -n "$ENV_NAME"
            else
                log_info "[DRY RUN] Would remove environment: $ENV_NAME"
            fi
        else
            log_warning "Environment '$ENV_NAME' already exists. Use --force to recreate."
            return 0
        fi
    fi
    
    # Create environment
    log_info "Creating conda environment from $ENV_FILE"
    if [ "$DRY_RUN" = false ]; then
        conda env create -f "$ENV_FILE" -y
        log_success "Conda environment '$ENV_NAME' created successfully"
    else
        log_info "[DRY RUN] Would create environment from: $ENV_FILE"
    fi
}

# Setup Git LFS
setup_git_lfs() {
    if [ "${SKIP_LFS:-false}" = true ]; then
        log_info "Skipping Git LFS setup"
        return 0
    fi
    
    log_info "Setting up Git LFS..."
    
    # Check if .gitattributes exists
    if [ ! -f "$GITATTRIBUTES_FILE" ]; then
        log_warning "Git attributes file not found: $GITATTRIBUTES_FILE"
        return 0
    fi
    
    # Initialize Git LFS
    if [ "$DRY_RUN" = false ]; then
        git lfs install
        log_success "Git LFS initialized"
        
        # Install tracking patterns from .gitattributes
        log_info "Installing LFS tracking patterns..."
        while IFS= read -r line; do
            if [[ $line =~ ^([^#]+)filter=lfs ]]; then
                pattern=$(echo "$line" | awk '{print $1}')
                git lfs track "$pattern"
                log_verbose "Added LFS tracking for: $pattern"
            fi
        done < "$GITATTRIBUTES_FILE"
        
        log_success "Git LFS tracking patterns installed"
    else
        log_info "[DRY RUN] Would initialize Git LFS and install tracking patterns"
    fi
}

# Validate GPU support
validate_gpu() {
    if [ "${SKIP_VALIDATION:-false}" = true ]; then
        log_info "Skipping GPU validation"
        return 0
    fi
    
    log_info "Validating GPU support..."
    
    if [ "$DRY_RUN" = true ]; then
        log_info "[DRY RUN] Would validate GPU support"
        return 0
    fi
    
    # Check if CUDA is available
    if ! command_exists nvidia-smi; then
        log_warning "nvidia-smi not found. GPU validation skipped."
        return 0
    fi
    
    # Get GPU info
    GPU_INFO=$(nvidia-smi --query-gpu=name,memory.total --format=csv,noheader,nounits)
    log_verbose "GPU Info: $GPU_INFO"
    
    # Test PyTorch CUDA support
    log_info "Testing PyTorch CUDA support..."
    
    # Create temporary Python script to test CUDA
    cat > /tmp/test_cuda.py << 'EOF'
import torch
import json
import sys

def test_cuda():
    result = {
        "cuda_available": torch.cuda.is_available(),
        "cuda_version": torch.version.cuda if torch.cuda.is_available() else None,
        "gpu_count": torch.cuda.device_count() if torch.cuda.is_available() else 0,
        "gpu_name": None,
        "memory_total_gb": None
    }
    
    if torch.cuda.is_available():
        try:
            result["gpu_name"] = torch.cuda.get_device_name(0)
            props = torch.cuda.get_device_properties(0)
            result["memory_total_gb"] = round(props.total_memory / (1024**3), 1)
        except Exception as e:
            result["error"] = str(e)
    
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    test_cuda()
EOF
    
    # Run the test script
    if conda run -n "$ENV_NAME" python /tmp/test_cuda.py > /tmp/cuda_test.json 2>/dev/null; then
        CUDA_RESULT=$(cat /tmp/cuda_test.json)
        log_verbose "CUDA Test Result: $CUDA_RESULT"
        
        # Parse result
        CUDA_AVAILABLE=$(echo "$CUDA_RESULT" | jq -r '.cuda_available' 2>/dev/null || echo "false")
        
        if [ "$CUDA_AVAILABLE" = "true" ]; then
            GPU_NAME=$(echo "$CUDA_RESULT" | jq -r '.gpu_name' 2>/dev/null)
            MEMORY_GB=$(echo "$CUDA_RESULT" | jq -r '.memory_total_gb' 2>/dev/null)
            CUDA_VERSION=$(echo "$CUDA_RESULT" | jq -r '.cuda_version' 2>/dev/null)
            
            log_success "GPU validation successful"
            log_info "  GPU: $GPU_NAME"
            log_info "  Memory: ${MEMORY_GB}GB"
            log_info "  CUDA: $CUDA_VERSION"
        else
            log_warning "CUDA not available in PyTorch. CPU-only mode."
        fi
    else
        log_warning "Failed to test CUDA support. Manual validation required."
    fi
    
    # Clean up
    rm -f /tmp/test_cuda.py /tmp/cuda_test.json
}

# Activate environment and run post-setup validation
post_setup_validation() {
    log_info "Running post-setup validation..."
    
    if [ "$DRY_RUN" = true ]; then
        log_info "[DRY RUN] Would run post-setup validation"
        return 0
    fi
    
    # Test environment activation
    log_info "Testing environment activation..."
    
    # Test basic imports
    cat > /tmp/test_imports.py << 'EOF'
import sys
import json

def test_imports():
    packages = [
        "torch", "torchvision", "torchaudio",
        "pandas", "numpy", "sklearn",
        "cv2", "matplotlib", "seaborn",
        "requests", "beautifulsoup4"
    ]
    
    results = {}
    for package in packages:
        try:
            __import__(package)
            results[package] = "success"
        except ImportError as e:
            results[package] = f"failed: {str(e)}"
    
    return results

if __name__ == "__main__":
    results = test_imports()
    failed = [pkg for pkg, status in results.items() if status != "success"]
    
    print(json.dumps({
        "total_packages": len(results),
        "successful": len(results) - len(failed),
        "failed": len(failed),
        "failed_packages": failed,
        "success": len(failed) == 0
    }, indent=2))
EOF
    
    if conda run -n "$ENV_NAME" python /tmp/test_imports.py > /tmp/import_test.json; then
        IMPORT_RESULT=$(cat /tmp/import_test.json)
        SUCCESS_COUNT=$(echo "$IMPORT_RESULT" | jq -r '.successful')
        TOTAL_COUNT=$(echo "$IMPORT_RESULT" | jq -r '.total_packages')
        
        log_info "Package imports: $SUCCESS_COUNT/$TOTAL_COUNT successful"
        
        if [ "$(echo "$IMPORT_RESULT" | jq -r '.success')" = "true" ]; then
            log_success "All required packages imported successfully"
        else
            FAILED_PACKAGES=$(echo "$IMPORT_RESULT" | jq -r '.failed_packages[]')
            log_warning "Failed to import some packages: $FAILED_PACKAGES"
        fi
    else
        log_error "Failed to test package imports"
        exit 4
    fi
    
    # Clean up
    rm -f /tmp/test_imports.py /tmp/import_test.json
}

# Main execution
main() {
    local start_time=$(date +%s)
    
    echo "=============================================="
    echo "MMA Analytics Environment Bootstrap"
    echo "=============================================="
    echo
    
    # Parse arguments
    parse_args "$@"
    
    # Validate requirements
    validate_requirements
    
    # Setup environment
    setup_conda_environment
    
    # Setup Git LFS
    setup_git_lfs
    
    # Validate GPU
    validate_gpu
    
    # Post-setup validation
    post_setup_validation
    
    # Calculate and display execution time
    local end_time=$(date +%s)
    local duration=$((end_time - start_time))
    
    echo
    echo "=============================================="
    if [ "$DRY_RUN" = true ]; then
        log_success "Bootstrap script completed (DRY RUN)"
    else
        log_success "Environment setup completed successfully"
    fi
    echo "Execution time: ${duration}s"
    echo "=============================================="
    echo
    echo "Next steps:"
    echo "1. Activate environment: conda activate $ENV_NAME"
    echo "2. Test GPU: python -c 'import torch; print(torch.cuda.is_available())'"
    echo "3. Initialize directories: python scripts/setup/init_dirs.py"
    echo "4. Check quickstart guide: specs/001-setup-tasks-set/quickstart.md"
}

# Run main function
main "$@"