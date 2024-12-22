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
dockerfile-generator /path/to/your/project

# Specify output location
dockerfile-generator /path/to/your/project -o /path/to/output/Dockerfile

# Enable verbose logging
dockerfile-generator /path/to/your/project -v
```

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
