"""Dynamic tool provider for managing API tools."""

from typing import Any, Dict, List, Optional, Literal
from mcp import Tool

from .factory import APIToolFactory
from .models import APISpec, AuthConfig, RateLimitConfig


class DynamicToolProvider:
    """Manages dynamic tool registration from API definitions."""

    def __init__(self):
        """Initialize the dynamic tool provider."""
        self._factory = APIToolFactory()
        self._registered_tools: Dict[str, List[Tool]] = {}

    async def register_api_tools(
        self,
        spec_url: str,
        api_type: Literal["openapi", "swagger", "graphql"],
        auth_config: Optional[AuthConfig] = None,
        rate_limit_config: Optional[RateLimitConfig] = None
    ) -> List[str]:
        """
        Register tools from an API specification.
        
        Args:
            spec_url: URL to the API specification
            api_type: Type of API specification
            auth_config: Optional authentication configuration
            rate_limit_config: Optional rate limiting configuration
            
        Returns:
            List of registered tool names
        """
        tools = []
        
        if api_type == "openapi":
            tools = await self._factory.create_tool_from_openapi(spec_url, auth_config)
        elif api_type == "swagger":
            tools = await self._factory.create_tool_from_swagger(spec_url, auth_config)
        elif api_type == "graphql":
            tools = await self._factory.create_tool_from_graphql(spec_url, auth_config)
        
        # Store registered tools
        self._registered_tools[spec_url] = tools
        
        return [tool.name for tool in tools]

    def get_registered_tools(self, spec_url: Optional[str] = None) -> List[Tool]:
        """
        Get registered tools, optionally filtered by spec URL.
        
        Args:
            spec_url: Optional URL to filter tools by
            
        Returns:
            List of registered tools
        """
        if spec_url:
            return self._registered_tools.get(spec_url, [])
        return [tool for tools in self._registered_tools.values() for tool in tools]

    def unregister_tools(self, spec_url: str) -> None:
        """
        Unregister tools for a specific API specification.
        
        Args:
            spec_url: URL of the API specification
        """
        if spec_url in self._registered_tools:
            del self._registered_tools[spec_url] 