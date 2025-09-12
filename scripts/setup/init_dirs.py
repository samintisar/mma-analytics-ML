#!/usr/bin/env python3
"""
MMA Analytics Directory Structure Initialization Script

Creates the complete directory structure for the MMA Analytics project foundation.
Follows library-first architecture principles with proper CLI interface.
"""

import argparse
import json
import logging
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Union
import time


class DirectoryInitializer:
    """Handles directory structure creation and validation."""
    
    def __init__(self, base_dir: Union[str, Path], force: bool = False, verbose: bool = False):
        """Initialize directory creator.
        
        Args:
            base_dir: Base directory for project structure
            force: Force overwrite existing directories
            verbose: Enable verbose output
        """
        self.base_dir = Path(base_dir).resolve()
        self.force = force
        self.verbose = verbose
        self.created_dirs = []
        self.errors = []
        
        # Setup logging
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup structured logging."""
        log_level = logging.DEBUG if self.verbose else logging.INFO
        logging.basicConfig(
            level=log_level,
            format='{"timestamp": "%(asctime)s", "level": "%(levelname)s", "component": "init_dirs", "message": "%(message)s"}',
            handlers=[logging.StreamHandler(sys.stdout)]
        )
        self.logger = logging.getLogger(__name__)
    
    def create_directory_structure(self) -> Dict:
        """Create the complete directory structure.
        
        Returns:
            Dict with creation results
        """
        start_time = time.time()
        
        self.logger.info(f"Starting directory initialization in {self.base_dir}")
        
        # Define directory structure
        directories = self._get_directory_structure()
        
        # Create each directory
        for dir_path in directories:
            try:
                full_path = self.base_dir / dir_path
                self._create_directory(full_path, dir_path)
            except Exception as e:
                error_msg = f"Failed to create {dir_path}: {str(e)}"
                self.errors.append(error_msg)
                self.logger.error(error_msg)
        
        # Compile results
        results = {
            "base_directory": str(self.base_dir),
            "created_directories": self.created_dirs,
            "errors": self.errors,
            "total_created": len(self.created_dirs),
            "total_errors": len(self.errors),
            "success": len(self.errors) == 0,
            "execution_time_seconds": round(time.time() - start_time, 2)
        }
        
        self.logger.info(f"Directory initialization completed: {results['total_created']} created, {results['total_errors']} errors")
        
        return results
    
    def _get_directory_structure(self) -> List[str]:
        """Get the complete directory structure definition.
        
        Returns:
            List of directory paths to create
        """
        return [
            # Source code structure
            "src/",
            "src/ingest/",
            "src/video/",
            "src/utils/",
            
            # Data structure
            "data/",
            "data/raw/",
            "data/processed/",
            "data/fixtures/",
            "data/fixtures/sample_ufcstats/",
            "data/fixtures/sample_videos/",
            
            # Test structure
            "tests/",
            "tests/contract/",
            "tests/integration/",
            "tests/unit/",
            "tests/performance/",
            
            # Scripts structure
            "scripts/",
            "scripts/setup/",
            "scripts/runners/",
            
            # Documentation and notebooks
            "notebooks/",
            "notebooks/analysis/",
            "notebooks/templates/",
            "docs/",
            
            # Model storage (Git LFS tracked)
            "models/",
            
            # Configuration and specifications
            "specs/",
            "specs/001-setup-tasks-set/",
            "specs/001-setup-tasks-set/contracts/",
            
            # Memory and logs
            "memory/",
            "logs/",
        ]
    
    def _create_directory(self, full_path: Path, relative_path: str):
        """Create a single directory with proper error handling.
        
        Args:
            full_path: Full path to directory
            relative_path: Relative path for logging
        """
        if full_path.exists():
            if not self.force:
                self.logger.debug(f"Directory already exists: {relative_path}")
                return
            
            # Force mode - remove existing directory
            try:
                if full_path.is_dir():
                    # Check if directory is empty
                    if any(full_path.iterdir()):
                        self.logger.warning(f"Removing non-empty directory: {relative_path}")
                        import shutil
                        shutil.rmtree(full_path)
                    else:
                        full_path.rmdir()
                else:
                    full_path.unlink()
            except Exception as e:
                raise Exception(f"Failed to remove existing {relative_path}: {str(e)}")
        
        # Create directory
        try:
            full_path.mkdir(parents=True, exist_ok=True)
            self.created_dirs.append(relative_path)
            self.logger.debug(f"Created directory: {relative_path}")
            
            # Create .gitkeep file to ensure directory is tracked
            gitkeep_path = full_path / ".gitkeep"
            gitkeep_path.touch()
            
        except PermissionError as e:
            raise Exception(f"Permission denied creating {relative_path}: {str(e)}")
        except OSError as e:
            raise Exception(f"OS error creating {relative_path}: {str(e)}")
    
    def validate_structure(self) -> Dict:
        """Validate that directory structure matches requirements.
        
        Returns:
            Validation results
        """
        required_dirs = self._get_directory_structure()
        missing_dirs = []
        existing_dirs = []
        
        for dir_path in required_dirs:
            full_path = self.base_dir / dir_path
            if full_path.exists() and full_path.is_dir():
                existing_dirs.append(dir_path)
            else:
                missing_dirs.append(dir_path)
        
        return {
            "required_directories": len(required_dirs),
            "existing_directories": len(existing_dirs),
            "missing_directories": len(missing_dirs),
            "missing_directory_list": missing_dirs,
            "validation_passed": len(missing_dirs) == 0,
            "completeness_percentage": round((len(existing_dirs) / len(required_dirs)) * 100, 1)
        }


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Initialize MMA Analytics project directory structure",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/setup/init_dirs.py --base-dir /path/to/project
  python scripts/setup/init_dirs.py --force --verbose
  python scripts/setup/init_dirs.py --validate
  python scripts/setup/init_dirs.py --format json
        """
    )
    
    parser.add_argument(
        "--base-dir", 
        type=str, 
        default=".",
        help="Base directory for project structure (default: current directory)"
    )
    
    parser.add_argument(
        "--force", 
        action="store_true",
        help="Force overwrite existing directories"
    )
    
    parser.add_argument(
        "--verbose", 
        action="store_true",
        help="Enable verbose output"
    )
    
    parser.add_argument(
        "--validate", 
        action="store_true",
        help="Validate existing structure without creating directories"
    )
    
    parser.add_argument(
        "--format", 
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)"
    )
    
    parser.add_argument(
        "--version", 
        action="version",
        version="init_dirs 1.0.0"
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize directory creator
        initializer = DirectoryInitializer(
            base_dir=args.base_dir,
            force=args.force,
            verbose=args.verbose
        )
        
        if args.validate:
            # Validate existing structure
            results = initializer.validate_structure()
        else:
            # Create directory structure
            results = initializer.create_directory_structure()
        
        # Output results
        if args.format == "json":
            print(json.dumps(results, indent=2))
        else:
            _print_text_results(results, args.validate)
        
        # Exit with appropriate code
        sys.exit(0 if results.get("success", results.get("validation_passed", False)) else 1)
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


def _print_text_results(results: Dict, is_validation: bool):
    """Print results in text format.
    
    Args:
        results: Results dictionary
        is_validation: Whether this is validation output
    """
    if is_validation:
        print(f"Structure Validation Results:")
        print(f"  Required directories: {results['required_directories']}")
        print(f"  Existing directories: {results['existing_directories']}")
        print(f"  Missing directories: {results['missing_directories']}")
        print(f"  Completeness: {results['completeness_percentage']}%")
        print(f"  Status: {'PASS' if results['validation_passed'] else 'FAIL'}")
        
        if results['missing_directory_list']:
            print("\nMissing directories:")
            for dir_path in results['missing_directory_list']:
                print(f"  - {dir_path}")
    else:
        print(f"Directory Initialization Results:")
        print(f"  Base directory: {results['base_directory']}")
        print(f"  Directories created: {results['total_created']}")
        print(f"  Errors encountered: {results['total_errors']}")
        print(f"  Execution time: {results['execution_time_seconds']}s")
        print(f"  Status: {'SUCCESS' if results['success'] else 'FAILED'}")
        
        if results['created_directories']:
            print(f"\nCreated directories:")
            for dir_path in results['created_directories']:
                print(f"  + {dir_path}")
        
        if results['errors']:
            print(f"\nErrors:")
            for error in results['errors']:
                print(f"  x {error}")


if __name__ == "__main__":
    main()