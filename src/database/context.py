"""Database context provider for MCP."""

from typing import Any, Dict
from mcp import Context, ContextProvider
from .search import DatabaseSearchEngine


class DatabaseContextProvider(ContextProvider):
    """Provides database search capabilities as context for MCP tools."""

    def __init__(self):
        """Initialize the database search engine."""
        self.search_engine = DatabaseSearchEngine()

    async def provide(self, request_context: Dict[str, Any]) -> Context:
        """Provide database search capabilities as context."""
        return Context(
            data={
                "search": {
                    "text_search": self.search_engine.text_search,
                    "vector_search": self.search_engine.vector_search,
                    "metadata": self.search_engine.get_available_collections
                }
            }
        )

    @property
    def name(self) -> str:
        return "database_search"

    @property
    def description(self) -> str:
        return "Provides search capabilities for connected databases" 