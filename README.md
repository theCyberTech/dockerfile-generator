# Dockerfile Generator

A CLI tool that analyzes your codebase and generates an optimized Dockerfile with best practices.

## Features

- Automatic language detection
- Dependency analysis
- Security best practices
- Multi-language support (Python, Node.js, Java, Go, Ruby)
- Optimized base images
- Environment variable detection
- Port configuration

## Installation

```bash
pip install dockerfile-generator
```

## Usage

```bash
# Basic usage
dockerfile-generator PROJECT_PATH

# Command line options
dockerfile-generator [OPTIONS] PROJECT_PATH

Options:
  -o, --output PATH  Specify custom output path for the Dockerfile
                    (default: PROJECT_PATH/Dockerfile)
  -v, --verbose     Enable verbose debug logging
  --help           Show this help message and exit
```

### Examples

```bash
# Generate Dockerfile in project directory
dockerfile-generator /path/to/your/project

# Generate Dockerfile at specific location
dockerfile-generator /path/to/your/project -o /custom/path/Dockerfile

# Enable verbose logging
dockerfile-generator /path/to/your/project -v

# Show help message
dockerfile-generator --help
```

The verbose flag (`-v`) enables detailed debug logging that shows:
- Project analysis details (file counts, paths)
- Language detection process and confidence scores
- Dependency file detection and analysis
- Dockerfile generation steps

## Supported Languages

- Python
- Node.js
- Java
- Go
- Ruby

## Security Features

- Uses slim/minimal base images
- Runs as non-root user
- Follows security best practices
- Minimal dependency installation

## Development

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Install in development mode:
```bash
pip install -e .
```

## Testing

```bash
pytest
```

## License

MIT License
