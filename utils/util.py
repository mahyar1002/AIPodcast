import requests
from pathlib import Path
import tempfile
import os
import re


def download_task_file(task_id: str, file_name: str) -> str:
    """Downloads file related to a specific task.

    Args:
        task_id: The task identifier
        file_name: Name of the file to download
    """
    url = f'https://agents-course-unit4-scoring.hf.space/files/{task_id}'
    response = requests.get(url, timeout=15)
    tmp_dir = Path(tempfile.gettempdir()) / "project_files"
    tmp_dir.mkdir(exist_ok=True)
    filepath = os.path.join(tmp_dir, file_name)
    with open(filepath, "wb") as f:
        f.write(response.content)

    return filepath


def format_document(doc):
    """Format a document regardless of whether it's a Document object or dictionary."""
    try:
        # Try to access as a Document object
        source = doc.metadata.get("source", "Wikipedia") if hasattr(
            doc, "metadata") else "Wikipedia"
        page = doc.metadata.get("page", "") if hasattr(doc, "metadata") else ""
        content = doc.page_content if hasattr(
            doc, "page_content") else str(doc)
    except AttributeError:
        # Fall back to dictionary access
        try:
            source = doc.get("source", "Wikipedia")
            page = doc.get("page", "")
            content = doc.get("content", doc.get(
                "page_content", "No content available"))
        except:
            # Ultimate fallback
            source = "Wikipedia"
            page = ""
            content = str(doc)

    return f'<Document source="{source}" page="{page}"/>\n{content}\n</Document>'


def clean_text(text: str) -> str:
    # Remove text between brackets including the brackets
    text = re.sub(r"\[.*?\]", "", text)
    # Replace multiple newlines with a single newline
    text = re.sub(r"\n{2,}", "\n\n", text)
    # Remove everything up to and including the first colon
    text = re.sub(r"^[^:]*:\s*", "", text, count=1)
    # Strip leading/trailing whitespace
    return text.strip()
