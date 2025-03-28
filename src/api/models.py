"""API configuration models."""

from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field


class AuthConfig(BaseModel):
    """Authentication configuration for API endpoints."""
    type: str = Field(..., description="Authentication type (api_key, bearer, oauth2)")
    key: Optional[str] = Field(None, description="API key for api_key auth")
    token: Optional[str] = Field(None, description="Bearer token for bearer auth")
    client_id: Optional[str] = Field(None, description="OAuth2 client ID")
    client_secret: Optional[str] = Field(None, description="OAuth2 client secret")


class RateLimitConfig(BaseModel):
    """Rate limiting configuration for API endpoints."""
    requests_per_minute: Optional[int] = Field(None, description="Maximum requests per minute")
    requests_per_hour: Optional[int] = Field(None, description="Maximum requests per hour")
    requests_per_day: Optional[int] = Field(None, description="Maximum requests per day")


class APISpec(BaseModel):
    """API specification configuration."""
    name: str = Field(..., description="Unique name for the API")
    url: str = Field(..., description="URL to the API specification")
    type: str = Field(..., description="API specification type (openapi, swagger, graphql)")
    auth: Optional[AuthConfig] = Field(None, description="Authentication configuration")
    rate_limits: Optional[RateLimitConfig] = Field(None, description="Rate limiting configuration")


class APIConfig(BaseModel):
    """API integration configuration."""
    specs: List[APISpec] = Field(default_factory=list, description="List of API specifications to load")
    auth: Dict[str, AuthConfig] = Field(default_factory=dict, description="Authentication configurations")
    rate_limits: Dict[str, RateLimitConfig] = Field(default_factory=dict, description="Rate limiting configurations") 