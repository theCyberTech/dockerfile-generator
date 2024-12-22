"""Tests for language detection functionality."""
import os
import pytest
from pathlib import Path
from dockerfile_generator.language_detectors import LanguageDetector

@pytest.fixture
def temp_project_dir(tmp_path):
    """Create a temporary project directory."""
    return tmp_path

def test_python_detection(temp_project_dir):
    """Test Python project detection."""
    # Create Python project files
    (temp_project_dir / 'requirements.txt').touch()
    (temp_project_dir / 'main.py').touch()
    
    detector = LanguageDetector(temp_project_dir)
    result = detector.detect_language()
    
    assert result is not None
    assert result['language'] == 'python'
    assert 'python' in result['base_image']

def test_node_detection(temp_project_dir):
    """Test Node.js project detection."""
    # Create Node.js project files
    (temp_project_dir / 'package.json').touch()
    (temp_project_dir / 'index.js').touch()
    
    detector = LanguageDetector(temp_project_dir)
    result = detector.detect_language()
    
    assert result is not None
    assert result['language'] == 'node'
    assert 'node' in result['base_image']

def test_multiple_language_files(temp_project_dir):
    """Test detection with multiple language files present."""
    # Create files for multiple languages
    (temp_project_dir / 'requirements.txt').touch()
    (temp_project_dir / 'package.json').touch()
    (temp_project_dir / 'main.py').touch()
    (temp_project_dir / 'index.js').touch()
    
    detector = LanguageDetector(temp_project_dir)
    result = detector.detect_language()
    
    # Should detect based on confidence score
    assert result is not None
    assert 'language' in result
    assert 'confidence_score' in result

def test_no_recognized_language(temp_project_dir):
    """Test behavior when no recognized language is found."""
    # Create some random files
    (temp_project_dir / 'random.txt').touch()
    
    detector = LanguageDetector(temp_project_dir)
    result = detector.detect_language()
    
    assert result is None

def test_language_specific_config():
    """Test language-specific configuration retrieval."""
    detector = LanguageDetector(Path('.'))
    
    python_config = detector.get_language_specific_config('python')
    assert python_config['package_manager'] == 'pip'
    assert 'dependency_file' in python_config
    assert 'typical_ports' in python_config
    
    node_config = detector.get_language_specific_config('node')
    assert node_config['package_manager'] == 'npm'
    assert 'dependency_file' in node_config
    assert 'typical_ports' in node_config
