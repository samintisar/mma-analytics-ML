#!/usr/bin/env python3
"""
UFCStats Scraping Contract Tests

Tests the UFCStats scraping interface according to the contract defined in:
specs/001-setup-tasks-set/contracts/ufcscrape.json

These tests MUST FAIL before implementation begins (TDD approach).
"""

import json
import pytest
import tempfile
from pathlib import Path
from typing import Dict, Any
import sys
import os

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

# Import the contract schema for validation
try:
    from jsonschema import validate, ValidationError
    CONTRACT_AVAILABLE = True
except ImportError:
    CONTRACT_AVAILABLE = False
    print("Warning: jsonschema not available, contract validation will be limited")

# Load the contract schema
CONTRACT_PATH = Path(__file__).parent.parent / 'specs' / '001-setup-tasks-set' / 'contracts' / 'ufcscrape.json'
if CONTRACT_PATH.exists():
    with open(CONTRACT_PATH, 'r') as f:
        CONTRACT_SCHEMA = json.load(f)
else:
    CONTRACT_SCHEMA = None


class TestUFCStatsContract:
    """Test suite for UFCStats scraping contract compliance."""
    
    def test_contract_schema_exists(self):
        """Test that the contract schema file exists."""
        assert CONTRACT_PATH.exists(), f"Contract schema not found at {CONTRACT_PATH}"
        assert CONTRACT_SCHEMA is not None, "Contract schema could not be loaded"
    
    def test_contract_schema_structure(self):
        """Test that the contract schema has the required structure."""
        if not CONTRACT_AVAILABLE:
            pytest.skip("jsonschema not available")
        
        required_properties = ['input', 'output']
        for prop in required_properties:
            assert prop in CONTRACT_SCHEMA, f"Missing required property: {prop}"
        
        # Test input schema structure
        input_schema = CONTRACT_SCHEMA['input']
        assert 'properties' in input_schema, "Input schema missing properties"
        assert 'scrape_type' in input_schema['properties'], "Missing scrape_type in input"
        assert 'output_dir' in input_schema['properties'], "Missing output_dir in input"
        
        # Test output schema structure  
        output_schema = CONTRACT_SCHEMA['output']
        assert 'properties' in output_schema, "Output schema missing properties"
        assert 'success' in output_schema['properties'], "Missing success in output"
        assert 'records_processed' in output_schema['properties'], "Missing records_processed in output"
    
    def test_input_validation_scrape_type_enum(self):
        """Test that scrape_type accepts only valid enum values."""
        if not CONTRACT_AVAILABLE:
            pytest.skip("jsonschema not available")
        
        valid_scrape_types = ['fighters', 'bouts', 'events', 'all']
        
        for scrape_type in valid_scrape_types:
            input_data = {
                'scrape_type': scrape_type,
                'output_dir': '/tmp/test'
            }
            try:
                validate(input_data, CONTRACT_SCHEMA['input'])
            except ValidationError:
                pytest.fail(f"Valid scrape_type '{scrape_type}' failed validation")
        
        # Test invalid scrape_type
        invalid_input = {
            'scrape_type': 'invalid_type',
            'output_dir': '/tmp/test'
        }
        with pytest.raises(ValidationError):
            validate(invalid_input, CONTRACT_SCHEMA['input'])
    
    def test_input_validation_required_fields(self):
        """Test that required fields are validated."""
        if not CONTRACT_AVAILABLE:
            pytest.skip("jsonschema not available")
        
        # Test missing required field
        invalid_input = {
            'scrape_type': 'fighters'
            # Missing output_dir
        }
        with pytest.raises(ValidationError):
            validate(invalid_input, CONTRACT_SCHEMA['input'])
    
    def test_input_validation_date_range(self):
        """Test that date_range validation works correctly."""
        if not CONTRACT_AVAILABLE:
            pytest.skip("jsonschema not available")
        
        # Valid date range
        valid_input = {
            'scrape_type': 'fighters',
            'output_dir': '/tmp/test',
            'date_range': {
                'start_date': '2024-01-01',
                'end_date': '2024-12-31'
            }
        }
        try:
            validate(valid_input, CONTRACT_SCHEMA['input'])
        except ValidationError:
            pytest.fail("Valid date range failed validation")
        
        # Invalid date format
        invalid_input = {
            'scrape_type': 'fighters',
            'output_dir': '/tmp/test',
            'date_range': {
                'start_date': 'invalid-date',
                'end_date': '2024-12-31'
            }
        }
        with pytest.raises(ValidationError):
            validate(invalid_input, CONTRACT_SCHEMA['input'])
    
    def test_output_schema_validation(self):
        """Test that output schema enforces correct structure."""
        if not CONTRACT_AVAILABLE:
            pytest.skip("jsonschema not available")
        
        # Valid output
        valid_output = {
            'success': True,
            'records_processed': 100,
            'output_files': [
                {
                    'filename': 'test.json',
                    'file_path': '/tmp/test.json',
                    'record_count': 100,
                    'file_size_bytes': 1024
                }
            ],
            'performance_metrics': {
                'duration_seconds': 60.0,
                'requests_per_second': 2.5,
                'records_per_second': 1.67
            }
        }
        try:
            validate(valid_output, CONTRACT_SCHEMA['output'])
        except ValidationError:
            pytest.fail("Valid output failed validation")
        
        # Missing required field in output
        invalid_output = {
            'success': True,
            # Missing records_processed
            'output_files': [],
            'performance_metrics': {
                'duration_seconds': 60.0,
                'requests_per_second': 2.5,
                'records_per_second': 1.67
            }
        }
        with pytest.raises(ValidationError):
            validate(invalid_output, CONTRACT_SCHEMA['output'])
    
    def test_output_files_validation(self):
        """Test that output_files array items are validated correctly."""
        if not CONTRACT_AVAILABLE:
            pytest.skip("jsonschema not available")
        
        # Valid output file item
        valid_file_item = {
            'filename': 'fighters.json',
            'file_path': '/tmp/fighters.json',
            'record_count': 50,
            'file_size_bytes': 2048
        }
        
        output_schema = CONTRACT_SCHEMA['output']
        files_schema = output_schema['properties']['output_files']['items']
        try:
            validate(valid_file_item, files_schema)
        except ValidationError:
            pytest.fail("Valid output file item failed validation")
        
        # Invalid output file item (missing required field)
        invalid_file_item = {
            'filename': 'fighters.json',
            # Missing file_path
            'record_count': 50,
            'file_size_bytes': 2048
        }
        with pytest.raises(ValidationError):
            validate(invalid_file_item, files_schema)
    
    def test_performance_metrics_validation(self):
        """Test that performance_metrics are validated correctly."""
        if not CONTRACT_AVAILABLE:
            pytest.skip("jsonschema not available")
        
        # Valid performance metrics
        valid_metrics = {
            'duration_seconds': 120.5,
            'requests_per_second': 1.8,
            'records_per_second': 0.9
        }
        
        output_schema = CONTRACT_SCHEMA['output']
        metrics_schema = output_schema['properties']['performance_metrics']
        try:
            validate(valid_metrics, metrics_schema)
        except ValidationError:
            pytest.fail("Valid performance metrics failed validation")
        
        # Invalid metrics (negative value)
        invalid_metrics = {
            'duration_seconds': -1.0,  # Invalid: negative
            'requests_per_second': 1.8,
            'records_per_second': 0.9
        }
        with pytest.raises(ValidationError):
            validate(invalid_metrics, metrics_schema)
    
    def test_errors_array_validation(self):
        """Test that errors array items are validated correctly."""
        if not CONTRACT_AVAILABLE:
            pytest.skip("jsonschema not available")
        
        # Valid error item
        valid_error = {
            'error_type': 'NetworkError',
            'error_message': 'Connection timeout',
            'timestamp': '2024-01-01T12:00:00'
        }
        
        output_schema = CONTRACT_SCHEMA['output']
        errors_schema = output_schema['properties']['errors']['items']
        try:
            validate(valid_error, errors_schema)
        except ValidationError:
            pytest.fail("Valid error item failed validation")
        
        # Invalid error item (missing timestamp)
        invalid_error = {
            'error_type': 'NetworkError',
            'error_message': 'Connection timeout'
            # Missing timestamp
        }
        with pytest.raises(ValidationError):
            validate(invalid_error, errors_schema)
    
    def test_batch_size_constraints(self):
        """Test that batch_size constraints are enforced."""
        if not CONTRACT_AVAILABLE:
            pytest.skip("jsonschema not available")
        
        # Valid batch sizes
        for batch_size in [1, 50, 500, 1000]:
            input_data = {
                'scrape_type': 'fighters',
                'output_dir': '/tmp/test',
                'batch_size': batch_size
            }
            try:
                validate(input_data, CONTRACT_SCHEMA['input'])
            except ValidationError:
                pytest.fail(f"Valid batch_size {batch_size} failed validation")
        
        # Invalid batch sizes
        for batch_size in [0, -1, 1001]:
            input_data = {
                'scrape_type': 'fighters',
                'output_dir': '/tmp/test',
                'batch_size': batch_size
            }
            with pytest.raises(ValidationError):
                validate(input_data, CONTRACT_SCHEMA['input'])
    
    def test_delay_seconds_constraints(self):
        """Test that delay_seconds constraints are enforced."""
        if not CONTRACT_AVAILABLE:
            pytest.skip("jsonschema not available")
        
        # Valid delay values
        for delay in [0.1, 1.0, 2.5, 5.0]:
            input_data = {
                'scrape_type': 'fighters',
                'output_dir': '/tmp/test',
                'delay_seconds': delay
            }
            try:
                validate(input_data, CONTRACT_SCHEMA['input'])
            except ValidationError:
                pytest.fail(f"Valid delay_seconds {delay} failed validation")
        
        # Invalid delay values
        for delay in [0.0, -0.1, 5.1]:
            input_data = {
                'scrape_type': 'fighters',
                'output_dir': '/tmp/test',
                'delay_seconds': delay
            }
            with pytest.raises(ValidationError):
                validate(input_data, CONTRACT_SCHEMA['input'])


if __name__ == '__main__':
    # Run the tests
    pytest.main([__file__, '-v'])