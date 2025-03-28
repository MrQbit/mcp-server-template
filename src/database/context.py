"""Database context provider for MCP."""

from typing import Any, Dict
from mcp import Context, ContextProvider

from .connection import get_db_session


class DatabaseContextProvider(ContextProvider):
    """Provides database sessions as context for MCP tools."""

    async def provide(self, request_context: Dict[str, Any]) -> Context:
        """Provide a database session as context."""
        session = await get_db_session().__aenter__()
        
        async def cleanup():
            await session.__aexit__(None, None, None)
        
        return Context(
            data={"db_session": session},
            cleanup=cleanup
        )

    @property
    def name(self) -> str:
        return "database"

    @property
    def description(self) -> str:
        return "Provides database session for database operations" 