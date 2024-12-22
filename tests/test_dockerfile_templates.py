"""Tests for Dockerfile template generation."""
import pytest
from dockerfile_generator.dockerfile_templates import DockerfileTemplate

@pytest.fixture
def python_config():
    """Sample Python project configuration."""
    return {
        'language': 'python',
        'base_image': 'python:3.9-slim',
        'dependencies': {
            'install_command': 'pip install -r requirements.txt',
            'dependencies': ['flask==2.0.1', 'requests>=2.26.0']
        },
        'env_vars': {'PORT': '8000'},
        'ports': [8000],
        'working_dir': '/app'
    }

@pytest.fixture
def python_uv_config():
    """Sample Python project configuration using uv."""
    return {
        'language': 'python',
        'base_image': 'python:3.9-slim',
        'dependencies': {
            'install_command': 'uv pip install .',
            'dependencies': ['flask>=2.0.1', 'requests>=2.26.0']
        },
        'env_vars': {'PORT': '8000'},
        'ports': [8000],
        'working_dir': '/app'
    }

@pytest.fixture
def python_pyproject_config():
    """Sample Python project configuration using pyproject.toml."""
    return {
        'language': 'python',
        'base_image': 'python:3.9-slim',
        'dependencies': {
            'install_command': 'pip install .[dev]',
            'dependencies': ['flask>=2.0.1', 'requests>=2.26.0'],
            'dev_dependencies': ['pytest>=6.2.5', 'black>=22.0.0']
        },
        'env_vars': {'PORT': '8000'},
        'ports': [8000],
        'working_dir': '/app'
    }

@pytest.fixture
def node_config():
    """Sample Node.js project configuration."""
    return {
        'language': 'node',
        'base_image': 'node:18-slim',
        'dependencies': {
            'install_command': 'npm install',
            'dependencies': ['express@^4.17.1', 'axios@^0.24.0']
        },
        'env_vars': {'PORT': '3000'},
        'ports': [3000],
        'working_dir': '/app'
    }

def test_python_dockerfile_generation(python_config):
    """Test Dockerfile generation for Python projects."""
    generator = DockerfileTemplate(python_config)
    dockerfile = generator.generate()
    
    assert 'FROM python:3.9-slim' in dockerfile
    assert 'WORKDIR /app' in dockerfile
    assert 'RUN pip install' in dockerfile
    assert 'EXPOSE 8000' in dockerfile
    assert 'USER appuser' in dockerfile
    assert 'CMD ["python"' in dockerfile

def test_python_uv_dockerfile_generation(python_uv_config):
    """Test Dockerfile generation for Python projects using uv."""
    generator = DockerfileTemplate(python_uv_config)
    dockerfile = generator.generate()
    
    assert 'FROM python:3.9-slim' in dockerfile
    assert 'WORKDIR /app' in dockerfile
    assert 'RUN pip install uv' in dockerfile
    assert 'RUN uv pip install .' in dockerfile
    assert 'EXPOSE 8000' in dockerfile
    assert 'USER appuser' in dockerfile
    assert 'CMD ["python"' in dockerfile

def test_python_pyproject_dockerfile_generation(python_pyproject_config):
    """Test Dockerfile generation for Python projects using pyproject.toml."""
    generator = DockerfileTemplate(python_pyproject_config)
    dockerfile = generator.generate()
    
    assert 'FROM python:3.9-slim' in dockerfile
    assert 'WORKDIR /app' in dockerfile
    assert 'COPY pyproject.toml' in dockerfile
    assert 'RUN pip install .[dev]' in dockerfile
    assert 'EXPOSE 8000' in dockerfile
    assert 'USER appuser' in dockerfile
    assert 'CMD ["python"' in dockerfile

def test_node_dockerfile_generation(node_config):
    """Test Dockerfile generation for Node.js projects."""
    generator = DockerfileTemplate(node_config)
    dockerfile = generator.generate()
    
    assert 'FROM node:18-slim' in dockerfile
    assert 'WORKDIR /app' in dockerfile
    assert 'RUN npm ci' in dockerfile
    assert 'EXPOSE 3000' in dockerfile
    assert 'USER appuser' in dockerfile
    assert 'CMD ["node"' in dockerfile

def test_invalid_language_config():
    """Test behavior with invalid language configuration."""
    config = {
        'language': 'invalid',
        'base_image': 'invalid:latest'
    }
    
    generator = DockerfileTemplate(config)
    with pytest.raises(ValueError):
        generator.generate()

def test_dockerfile_security_measures(python_config):
    """Test security measures in generated Dockerfile."""
    generator = DockerfileTemplate(python_config)
    dockerfile = generator.generate()
    
    # Check for non-root user
    assert 'RUN groupadd -r appuser' in dockerfile
    assert 'USER appuser' in dockerfile
    
    # Check for proper permissions
    assert 'chown -R appuser:appuser' in dockerfile
