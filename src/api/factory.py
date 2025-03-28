"""API tool factory for generating MCP tools from API specifications."""

import json
from typing import Any, Dict, List, Optional, Type, TypeVar
from urllib.parse import urljoin

import httpx
from mcp import Tool
from pydantic import BaseModel

from .models import APISpec, AuthConfig, RateLimitConfig

T = TypeVar("T", bound=BaseModel)


class APIToolFactory:
    """Converts API definitions into MCP tools."""

    def __init__(self):
        """Initialize the API tool factory."""
        self._http_client = httpx.AsyncClient()

    async def create_tool_from_openapi(
        self, spec_url: str, auth_config: Optional[AuthConfig] = None
    ) -> List[Tool]:
        """
        Create tools from an OpenAPI specification.
        
        Args:
            spec_url: URL to the OpenAPI specification
            auth_config: Optional authentication configuration
            
        Returns:
            List of generated MCP tools
        """
        spec = await self._fetch_spec(spec_url)
        tools = []
        
        for path, path_data in spec.get("paths", {}).items():
            for method, operation in path_data.items():
                if method not in ["get", "post", "put", "delete", "patch"]:
                    continue
                    
                tool = await self._create_tool_from_operation(
                    operation,
                    path,
                    method,
                    spec,
                    auth_config
                )
                if tool:
                    tools.append(tool)
        
        return tools

    async def create_tool_from_swagger(
        self, spec_url: str, auth_config: Optional[AuthConfig] = None
    ) -> List[Tool]:
        """
        Create tools from a Swagger specification.
        
        Args:
            spec_url: URL to the Swagger specification
            auth_config: Optional authentication configuration
            
        Returns:
            List of generated MCP tools
        """
        # Swagger 2.0 is a subset of OpenAPI 3.0
        return await self.create_tool_from_openapi(spec_url, auth_config)

    async def create_tool_from_graphql(
        self, schema_url: str, auth_config: Optional[AuthConfig] = None
    ) -> List[Tool]:
        """
        Create tools from a GraphQL schema.
        
        Args:
            schema_url: URL to the GraphQL schema
            auth_config: Optional authentication configuration
            
        Returns:
            List of generated MCP tools
        """
        # TODO: Implement GraphQL schema parsing and tool generation
        raise NotImplementedError("GraphQL support coming soon")

    async def _fetch_spec(self, url: str) -> Dict[str, Any]:
        """Fetch API specification from URL."""
        response = await self._http_client.get(url)
        response.raise_for_status()
        return response.json()

    async def _create_tool_from_operation(
        self,
        operation: Dict[str, Any],
        path: str,
        method: str,
        spec: Dict[str, Any],
        auth_config: Optional[AuthConfig] = None
    ) -> Optional[Tool]:
        """Create a tool from an OpenAPI operation."""
        operation_id = operation.get("operationId")
        if not operation_id:
            return None

        # Generate parameter types
        params = self._generate_parameters(operation, spec)
        
        # Generate response type
        response_type = self._generate_response_type(operation, spec)
        
        # Create tool function
        async def tool_function(**kwargs):
            # TODO: Implement actual API call with authentication and rate limiting
            return {"status": "not implemented"}
        
        # Create tool
        return Tool(
            name=operation_id,
            description=operation.get("description", ""),
            parameters=params,
            return_type=response_type,
            function=tool_function
        )

    def _generate_parameters(
        self, operation: Dict[str, Any], spec: Dict[str, Any]
    ) -> Dict[str, Type[BaseModel]]:
        """Generate parameter types from operation."""
        params = {}
        
        for param in operation.get("parameters", []):
            param_type = self._get_schema_type(param.get("schema", {}), spec)
            if param_type:
                params[param["name"]] = param_type
        
        return params

    def _generate_response_type(
        self, operation: Dict[str, Any], spec: Dict[str, Any]
    ) -> Type[BaseModel]:
        """Generate response type from operation."""
        responses = operation.get("responses", {})
        success_response = responses.get("200", {})
        schema = success_response.get("content", {}).get("application/json", {}).get("schema", {})
        return self._get_schema_type(schema, spec)

    def _get_schema_type(
        self, schema: Dict[str, Any], spec: Dict[str, Any]
    ) -> Optional[Type[BaseModel]]:
        """Convert OpenAPI schema to Pydantic model type."""
        # TODO: Implement schema to type conversion
        return Dict[str, Any] 