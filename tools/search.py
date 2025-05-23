from langchain_core.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.document_loaders import WikipediaLoader
from langchain_community.document_loaders import ArxivLoader
from utils.util import format_document
from typing import List, Dict


@tool
def wiki_search(query: str) -> str:
    """Search Wikipedia for a query and return maximum 2 results.

    Args:
        query: The search query."""
    search_docs = WikipediaLoader(query=query, load_max_docs=2).load()

    formatted_search_docs = "\n\n---\n\n".join(
        [
            format_document(doc)
            for doc in search_docs
        ])

    return {"wiki_results": formatted_search_docs}


@tool
def web_search(query: str) -> str:
    """Search Tavily for a query and return maximum 5 results.

    Args:
        query: The search query."""
    search_tool = TavilySearchResults(max_results=5)
    search_docs = search_tool.invoke({"query": query})

    formatted_search_docs = "\n\n---\n\n".join(
        [
            f'<Document source="{doc.get("source", doc.get("url", "Unknown"))}" page="{doc.get("page", "")}"/>\n{doc.get("content", doc.get("page_content", "No content available"))}\n</Document>'
            for doc in search_docs
        ])

    return {"web_results": formatted_search_docs}


@tool
def arvix_search(query: str) -> str:
    """Search Arxiv for a query and return maximum 3 result.

    Args:
        query: The search query."""
    search_docs = ArxivLoader(query=query, load_max_docs=3).load()
    formatted_search_docs = "\n\n---\n\n".join(
        [
            f'<Document source="{doc.metadata["source"]}" page="{doc.metadata.get("page", "")}"/>\n{doc.page_content[:1000]}\n</Document>'
            for doc in search_docs
        ])
    return {"arvix_results": formatted_search_docs}


search_tools = [wiki_search, web_search, arvix_search]
