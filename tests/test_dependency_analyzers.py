"""Tests for dependency analysis functionality."""
import pytest
from pathlib import Path
from dockerfile_generator.dependency_analyzers import DependencyAnalyzer

@pytest.fixture
def temp_project_dir(tmp_path):
    """Create a temporary project directory."""
    return tmp_path

def test_python_requirements_txt(temp_project_dir):
    """Test Python dependency analysis with requirements.txt."""
    requirements_content = """
    flask==2.0.1
    requests>=2.26.0
    pytest~=6.2.5
    """
    
    requirements_file = temp_project_dir / 'requirements.txt'
    requirements_file.write_text(requirements_content)
    
    analyzer = DependencyAnalyzer(temp_project_dir, 'python')
    result = analyzer.analyze()
    
    assert 'install_command' in result
    assert result['install_command'] == 'pip install -r requirements.txt'
    assert 'dependencies' in result
    assert len(result['dependencies']) == 3
    assert any('flask' in dep for dep in result['dependencies'])

def test_python_pyproject_toml(temp_project_dir):
    """Test Python dependency analysis with pyproject.toml."""
    pyproject_content = """
[project]
name = "test-project"
version = "0.1.0"
dependencies = [
    "flask>=2.0.1",
    "requests>=2.26.0"
]

[project.optional-dependencies]
dev = [
    "pytest>=6.2.5",
    "black>=22.0.0"
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
    """
    
    pyproject_file = temp_project_dir / 'pyproject.toml'
    pyproject_file.write_text(pyproject_content)
    
    analyzer = DependencyAnalyzer(temp_project_dir, 'python')
    result = analyzer.analyze()
    
    assert 'install_command' in result
    assert result['install_command'] == 'pip install .[dev]'
    assert len(result['dependencies']) == 2
    assert len(result['dev_dependencies']) == 2
    assert any('flask' in dep for dep in result['dependencies'])
    assert any('pytest' in dep for dep in result['dev_dependencies'])

def test_python_uv_project(temp_project_dir):
    """Test Python dependency analysis with uv build system."""
    pyproject_content = """
[project]
name = "test-project"
version = "0.1.0"
dependencies = [
    "flask>=2.0.1",
    "requests>=2.26.0"
]

[build-system]
requires = ["uv"]
build-backend = "uv.build"
    """
    
    pyproject_file = temp_project_dir / 'pyproject.toml'
    pyproject_file.write_text(pyproject_content)
    
    analyzer = DependencyAnalyzer(temp_project_dir, 'python')
    result = analyzer.analyze()
    
    assert 'install_command' in result
    assert result['install_command'] == 'uv pip install .'
    assert len(result['dependencies']) == 2
    assert any('flask' in dep for dep in result['dependencies'])

def test_python_requirements_dev_txt(temp_project_dir):
    """Test Python dependency analysis with requirements-dev.txt."""
    requirements_content = "flask==2.0.1\nrequests>=2.26.0"
    requirements_dev_content = "pytest>=6.2.5\nblack>=22.0.0"
    
    requirements_file = temp_project_dir / 'requirements.txt'
    requirements_file.write_text(requirements_content)
    
    requirements_dev_file = temp_project_dir / 'requirements-dev.txt'
    requirements_dev_file.write_text(requirements_dev_content)
    
    analyzer = DependencyAnalyzer(temp_project_dir, 'python')
    result = analyzer.analyze()
    
    assert len(result['dependencies']) == 2
    assert len(result['dev_dependencies']) == 2
    assert any('flask' in dep for dep in result['dependencies'])
    assert any('pytest' in dep for dep in result['dev_dependencies'])

def test_node_dependency_analysis(temp_project_dir):
    """Test Node.js dependency analysis."""
    package_json_content = """{
        "dependencies": {
            "express": "^4.17.1",
            "axios": "^0.24.0"
        },
        "devDependencies": {
            "jest": "^27.0.0"
        }
    }"""
    
    package_json = temp_project_dir / 'package.json'
    package_json.write_text(package_json_content)
    
    analyzer = DependencyAnalyzer(temp_project_dir, 'node')
    result = analyzer.analyze()
    
    assert 'install_command' in result
    assert 'dependencies' in result
    assert 'dev_dependencies' in result
    assert len(result['dependencies']) == 2
    assert len(result['dev_dependencies']) == 1

def test_missing_dependency_file(temp_project_dir):
    """Test behavior when dependency file is missing."""
    analyzer = DependencyAnalyzer(temp_project_dir, 'python')
    result = analyzer.analyze()
    
    assert result['dependencies'] == []
    assert 'install_command' in result

def test_invalid_language():
    """Test behavior with invalid language."""
    analyzer = DependencyAnalyzer(Path('.'), 'invalid_language')
    result = analyzer.analyze()
    
    assert result == {}
