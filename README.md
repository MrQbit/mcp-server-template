# MCP Server Template (Python)

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A ready-to-use template for building Model Context Protocol (MCP) servers in Python. This template helps you quickly create servers that can register and expose tools and prompts for AI models to use.

## 📚 Table of Contents

- [Quick Start](#quick-start)
- [Command Line Options](#command-line-options)
- [Creating Your Own Tools and Prompts](#creating-your-own-tools-and-prompts)
- [Database Support](#database-support)
- [Project Structure](#project-structure)
- [Deployment Options](#deployment-options)
- [Development Guide](#development-guide)
- [Need Help?](#need-help)

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or newer

### Setup in 3 Easy Steps

#### 1️⃣ Install the package

```bash
# Clone the repository
git clone https://github.com/mrqbit/mcp-server-template-python.git my-mcp-server
cd my-mcp-server

# Install in development mode
pip install -e ".[dev]"
```

#### 2️⃣ Run your server

```bash
# Run with Python
python -m src.main

# Or use the convenient CLI
mcp-server-template
```

#### 3️⃣ Your server is now live!

Access your MCP server at:
- 🌐 HTTP: http://localhost:8080
- 💻 Or use the stdio transport: `mcp-server-template --transport stdio`

You'll see log output confirming the server is running successfully.

## 🎮 Command Line Options

Customize your server behavior with these command-line options:

```bash
# Change port (default: 8080)
mcp-server-template --port 9000

# Enable debug mode for more detailed logs
mcp-server-template --debug

# Use stdio transport instead of HTTP
mcp-server-template --transport stdio

# Set logging level (options: debug, info, warning, error)
mcp-server-template --log-level debug
```

## 🛠️ Creating Your Own Tools and Prompts

### Add a Tool

Tools are functions that AI models can call. To add a new tool:

1. Edit `src/main.py` 
2. Add a new function with the `@mcp.tool()` decorator:

```python
@mcp.tool()
def your_tool_name(param1: str, param2: int) -> Dict[str, Any]:
    """
    Your tool description - this will be shown to the AI.
    
    Args:
        param1: Description of first parameter
        param2: Description of second parameter
        
    Returns:
        Dictionary with your results
    """
    # Your tool logic here
    return {"result": "your result"}
```

### Add a Prompt

Prompts are templates that AI models can access:

```python
@mcp.prompt()
def your_prompt_name(param: str) -> str:
    """Your prompt description."""
    return f"""
    Your formatted prompt with {param} inserted.
    Use this for structured prompt templates.
    """
```

## 📁 Project Structure

```
src/                      # Source code directory
├── main.py               # Server entry point with tools & prompts
├── config.py             # Configuration settings
├── utils/                # Utility functions
├── tools/                # Tools implementation
└── resources/            # Resource definitions
test/                     # Tests directory
pyproject.toml            # Package configuration
Dockerfile                # Docker support
```

## 🚢 Deployment Options

### Docker Deployment

```bash
# Build the Docker image
docker build -t my-mcp-server .

# Run the container
docker run -p 8080:8080 my-mcp-server
```

### Cloud Deployment

This template is designed to work well with various cloud platforms:
- Deploy as a container on AWS, GCP, or Azure
- Run on serverless platforms that support containerized applications
- Works with Kubernetes for orchestration

## 🧪 Development Guide

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black src test
isort src test

# Run linting
flake8 src test
```

## ❓ Need Help?

- 📚 MCP Documentation: [modelcontextprotocol.io](https://modelcontextprotocol.io)
- 🐛 File an issue: [GitHub Issues](https://github.com/mrqbit/mcp-server-template-python/issues)

## Database Support

This template includes support for connecting to external PostgreSQL databases. To use database features:

1. Copy `.env.example` to `.env` and configure your database connection:
   ```bash
   cp .env.example .env
   ```

2. Update the `.env` file with your database credentials:
   ```
   DB_HOST=your_database_host
   DB_PORT=5432
   DB_NAME=your_database_name
   DB_USER=your_username
   DB_PASSWORD=your_password
   ```

3. Use the database context in your tools:
   ```python
   @mcp.tool()
   async def query_database(query: str, context: Dict[str, Any]) -> Dict[str, Any]:
       """Execute a read-only SQL query."""
       session = context["database"]["db_session"]
       result = await session.execute(query)
       rows = result.fetchall()
       return {"results": [dict(row) for row in rows]}
   ```

The database context provider automatically manages connections and sessions, with proper connection pooling and cleanup.

---

Made with ❤️ for the AI developer community
