"""Configuration settings for the MCP server."""

from typing import Any, Dict, List, Optional
from pydantic import BaseSettings

from .api.models import APIConfig


class DatabaseConfig(BaseSettings):
    """Database configuration settings."""
    # Database connection settings
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "mcp_db"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = ""
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    
    # Search configuration
    VECTOR_SIMILARITY_THRESHOLD: float = 0.7
    MAX_SEARCH_RESULTS: int = 100
    ENABLE_VECTOR_SEARCH: bool = True
    SEARCHABLE_COLLECTIONS: List[str] = []

    class Config:
        env_prefix = ""
        case_sensitive = True


class ServerConfig:
    """Server configuration settings."""

    def __init__(self) -> None:
        """Initialize with default configuration."""
        self.name: str = "MCP Server Template"
        self.description: str = (
            "A boilerplate for Model Context Protocol servers in Python"
        )
        self.version: str = "0.1.0"
        self.port: int = 8080
        self.host: str = "0.0.0.0"
        self.debug: bool = False
        self.log_level: str = "info"
        self.metadata: Dict[str, Any] = {
            "github": "https://github.com/yourusername/mcp-server-template-python",
        }
        self.db: DatabaseConfig = DatabaseConfig()
        self.api: APIConfig = APIConfig()

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "port": self.port,
            "host": self.host,
            "debug": self.debug,
            "log_level": self.log_level,
            "metadata": self.metadata,
        }


# Global configuration instance
config = ServerConfig()
