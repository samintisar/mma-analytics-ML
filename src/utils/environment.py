#!/usr/bin/env python3
"""
MMA Analytics Environment Utilities

Provides functions for environment detection, validation, and monitoring.
Follows library-first architecture with CLI interface support.
"""

import argparse
import json
import logging
import platform
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Union, Any
import importlib.util
import re
from dataclasses import dataclass, asdict
import os


@dataclass
class EnvironmentInfo:
    """Container for environment information."""
    python_version: str
    platform: str
    architecture: str
    conda_env: Optional[str] = None
    conda_version: Optional[str] = None


class EnvironmentValidator:
    """Validates and monitors development environment."""
    
    def __init__(self, verbose: bool = False):
        """Initialize environment validator."""
        self.verbose = verbose
        self.logger = self._setup_logging()
    
    def _setup_logging(self) -> logging.Logger:
        """Setup structured logging."""
        logger = logging.getLogger(__name__)
        
        if not logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter(
                '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "component": "environment", "message": "%(message)s"}'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.DEBUG if self.verbose else logging.INFO)
        
        return logger
    
    def validate_python_version(self, min_version: tuple = (3, 11), format: str = "dict") -> Union[Dict, str]:
        """Validate Python version meets requirements."""
        current_version = sys.version_info[:3]
        min_required = f"{min_version[0]}.{min_version[1]}.0"
        current_str = f"{current_version[0]}.{current_version[1]}.{current_version[2]}"
        
        is_valid = current_version >= min_version
        
        result = {
            "python_version": current_str,
            "min_required": min_required,
            "is_valid": is_valid,
            "platform": platform.platform(),
            "architecture": platform.machine()
        }
        
        if not is_valid:
            result["message"] = f"Python {min_required} or higher required (found: {current_str})"
            result["recommendation"] = "Please upgrade Python or use a compatible environment"
        else:
            result["message"] = f"Python version {current_str} meets requirements"
        
        self.logger.info(f"Python version validation: {result['message']}")
        
        if format == "json":
            return json.dumps(result, indent=2)
        return result
    
    def validate_dependencies(self, required_packages: Optional[List[str]] = None, format: str = "dict") -> Union[Dict, str]:
        """Validate required dependencies are installed."""
        if required_packages is None:
            required_packages = [
                "torch", "torchvision", "torchaudio",
                "pandas", "numpy", "sklearn",
                "cv2", "matplotlib", "seaborn",
                "requests", "beautifulsoup4",
                "jupyter", "pytest", "psutil"
            ]
        
        result = {
            "dependencies": [],
            "installed": [],
            "missing": [],
            "total_packages": len(required_packages),
            "installed_count": 0,
            "missing_count": 0,
            "success_rate": 0.0
        }
        
        for package in required_packages:
            import_name = self._get_import_name(package)
            
            try:
                spec = importlib.util.find_spec(import_name)
                if spec is not None:
                    result["installed"].append(package)
                    result["installed_count"] += 1
                else:
                    result["missing"].append(package)
                    result["missing_count"] += 1
                    
            except Exception as e:
                result["missing"].append(package)
                result["missing_count"] += 1
        
        result["success_rate"] = round((result["installed_count"] / result["total_packages"]) * 100, 1)
        
        self.logger.info(f"Dependency validation: {result['installed_count']}/{result['total_packages']} packages installed ({result['success_rate']}%)")
        
        if format == "json":
            return json.dumps(result, indent=2)
        return result
    
    def validate_gpu(self, format: str = "dict") -> Union[Dict, str]:
        """Validate GPU availability and CUDA functionality."""
        result = {
            "gpu_available": False,
            "cuda_available": False,
            "gpu_name": None,
            "gpu_memory_total_gb": 0,
            "gpu_memory_available_gb": 0,
            "cuda_version": None,
            "pytorch_cuda_available": False,
            "status": "fail",
            "message": "GPU validation failed"
        }
        
        try:
            # Check PyTorch CUDA availability
            import torch
            result["pytorch_cuda_available"] = torch.cuda.is_available()
            
            if torch.cuda.is_available():
                result["gpu_available"] = True
                result["cuda_available"] = True
                result["gpu_name"] = torch.cuda.get_device_name(0)
                result["gpu_memory_total_gb"] = round(torch.cuda.get_device_properties(0).total_memory / 1e9, 1)
                result["gpu_memory_available_gb"] = round(torch.cuda.memory_allocated(0) / 1e9, 1)
                result["status"] = "pass"
                result["message"] = f"GPU detected: {result['gpu_name']} with {result['gpu_memory_total_gb']}GB memory"
                
                self.logger.info(f"GPU validation: {result['message']}")
            else:
                result["message"] = "No CUDA-enabled GPU detected by PyTorch"
                self.logger.warning("GPU validation: No CUDA support found")
                
        except ImportError:
            result["message"] = "PyTorch not available for GPU validation"
            self.logger.error("GPU validation: PyTorch not installed")
        except Exception as e:
            result["message"] = f"GPU validation error: {str(e)}"
            self.logger.error(f"GPU validation: {result['message']}")
        
        # Try to get CUDA version from nvidia-smi
        try:
            import subprocess
            result_nvidia = subprocess.run(['nvidia-smi', '--query-gpu=driver_version,cuda_version', '--format=csv,noheader,nounits'], 
                                        capture_output=True, text=True, timeout=10)
            if result_nvidia.returncode == 0:
                driver_version, cuda_version = result_nvidia.stdout.strip().split(', ')
                result["cuda_version"] = cuda_version
                self.logger.info(f"CUDA version from nvidia-smi: {cuda_version}")
        except:
            pass
        
        if format == "json":
            return json.dumps(result, indent=2)
        return result
    
    def validate_system_resources(self, format: str = "dict") -> Union[Dict, str]:
        """Validate system resources (memory, disk space)."""
        import psutil
        
        result = {
            "system_memory_total_gb": round(psutil.virtual_memory().total / 1e9, 1),
            "system_memory_available_gb": round(psutil.virtual_memory().available / 1e9, 1),
            "system_memory_percent_used": psutil.virtual_memory().percent,
            "disk_total_gb": round(psutil.disk_usage('/').total / 1e9, 1),
            "disk_free_gb": round(psutil.disk_usage('/').free / 1e9, 1),
            "disk_percent_used": psutil.disk_usage('/').percent,
            "status": "pass",
            "message": "System resources validation completed"
        }
        
        # Check minimum requirements
        if result["system_memory_available_gb"] < 8:
            result["status"] = "warn"
            result["message"] = f"Low system memory: {result['system_memory_available_gb']}GB available (8GB recommended)"
        
        if result["disk_free_gb"] < 20:
            result["status"] = "warn" if result["status"] == "pass" else "fail"
            result["message"] += f", Low disk space: {result['disk_free_gb']}GB free (20GB recommended)"
        
        self.logger.info(f"System resources: {result['system_memory_available_gb']}GB RAM available, {result['disk_free_gb']}GB disk free")
        
        if format == "json":
            return json.dumps(result, indent=2)
        return result
    
    def _get_import_name(self, package_name: str) -> str:
        """Map package name to import name."""
        mapping = {
            "opencv": "cv2",
            "opencv-python": "cv2",
            "beautifulsoup4": "bs4",
            "scikit-learn": "sklearn",
            "pytorch": "torch",
            "torchvision": "torchvision",
            "torchaudio": "torchaudio"
        }
        return mapping.get(package_name.lower(), package_name.lower())


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Validate MMA Analytics development environment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m src.utils.environment                  # Validate all components
  python -m src.utils.environment --python        # Check Python version only
  python -m src.utils.environment --dependencies  # Check dependencies only
  python -m src.utils.environment --gpu           # Check GPU and CUDA functionality
  python -m src.utils.environment --system        # Check system resources
  python -m src.utils.environment --format json   # JSON output
  python -m src.utils.environment --verbose        # Verbose output
        """
    )
    
    parser.add_argument("--python", action="store_true", help="Validate Python version")
    parser.add_argument("--dependencies", action="store_true", help="Validate dependencies")
    parser.add_argument("--gpu", action="store_true", help="Validate GPU and CUDA functionality")
    parser.add_argument("--system", action="store_true", help="Validate system resources (memory, disk)")
    parser.add_argument("--format", choices=["dict", "json"], default="dict", help="Output format (default: dict)")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("--version", action="version", version="environment utils 1.0.0")
    
    args = parser.parse_args()
    
    try:
        validator = EnvironmentValidator(verbose=args.verbose)
        results = {}
        
        # If no specific checks requested, run all
        if not any([args.python, args.dependencies, args.gpu, args.system]):
            args.python = args.dependencies = args.gpu = args.system = True
        
        # Run requested checks
        if args.python:
            results["python"] = validator.validate_python_version(format=args.format)
        
        if args.dependencies:
            results["dependencies"] = validator.validate_dependencies(format=args.format)
        
        if args.gpu:
            results["gpu"] = validator.validate_gpu(format=args.format)
        
        if args.system:
            results["system"] = validator.validate_system_resources(format=args.format)
        
        # Output results
        if args.format == "json":
            print(json.dumps(results, indent=2))
        else:
            for key, result in results.items():
                print(f"\n=== {key.upper()} VALIDATION ===")
                if isinstance(result, dict):
                    for k, v in result.items():
                        print(f"{k}: {v}")
                else:
                    print(result)
        
        # Exit with appropriate code
        success = all(
            result.get("is_valid", result.get("success", True)) 
            if isinstance(result, dict) else True
            for result in results.values()
        )
        
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()