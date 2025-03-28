"""Database search tools."""

from typing import Any, Dict, List
from mcp import tool


@tool()
async def search_database(
    context: Dict[str, Any],
    collection: str,
    query: str,
    limit: int = 10
) -> Dict[str, Any]:
    """
    Search the database using text-based search.
    
    Args:
        context: The context containing search capabilities
        collection: Name of the collection to search
        query: Search query text
        limit: Maximum number of results to return
        
    Returns:
        Dictionary containing search results
    """
    search = context["database_search"]["search"]
    results = await search["text_search"](collection, query, limit)
    return {"results": results}


@tool()
async def semantic_search(
    context: Dict[str, Any],
    collection: str,
    query: str,
    limit: int = 10
) -> Dict[str, Any]:
    """
    Search the database using semantic vector search.
    
    Args:
        context: The context containing search capabilities
        collection: Name of the collection to search
        query: Natural language query to convert to embedding
        limit: Maximum number of results to return
        
    Returns:
        Dictionary containing search results with similarity scores
    """
    # This would require integration with an embedding model
    embedding = await get_embedding(query)  # You'd need to implement this
    search = context["database_search"]["search"]
    results = await search["vector_search"](collection, embedding, limit)
    return {"results": results}


@tool()
async def list_searchable_collections(
    context: Dict[str, Any]
) -> Dict[str, Any]:
    """
    List all available searchable collections and their schemas.
    
    Returns:
        Dictionary containing collection information
    """
    search = context["database_search"]["search"]
    collections = await search["metadata"]()
    return {"collections": collections} 