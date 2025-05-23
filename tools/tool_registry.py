from typing import List, Callable, Literal, Optional, Dict, Any
from .calculator import calculator_tools
from .search import search_tools
from .media import media_tools

ToolCategory = Literal["calculator", "search", "media"]
Tool = Callable[..., Any]
ToolRegistry = Dict[ToolCategory, List[Tool]]

tool_registry: ToolRegistry = {
    "calculator": calculator_tools,
    "search": search_tools,
    "media": media_tools
}


def get_tools(categories: Optional[List[ToolCategory]] = None) -> List[Tool]:
    """Get tools by category or all tools if no category specified.

    Args:
        categories: List of categories to include, or None for all tools
    """
    if categories is None:
        all_tools: List[Tool] = []
        for _, value in tool_registry.items():
            all_tools.extend(value)
        return all_tools

    selected_tools: List[Tool] = []
    for category in categories:
        if category in tool_registry:
            selected_tools.extend(tool_registry[category])
    return selected_tools
