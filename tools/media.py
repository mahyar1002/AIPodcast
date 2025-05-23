from langchain_core.tools import tool
import pandas as pd
import os
from PIL import Image
from openai import OpenAI
from typing import Optional
from config.settings import settings
from typing import List, Dict


@tool
def file_reader(file_path: str) -> str:
    """Reads saved files.

    Args:
        file_path: path to the file
    """
    with open(file_path, "r") as file:
        content = file.read()
    return content


@tool
def audio_transcriber(file_path: str) -> str:
    """Transcribes audio files.

    Args:
        file_path: path to the audio file
    """
    audio = open(file_path, 'rb')
    client = OpenAI(api_key=os.getenv("OPEN_AI_KEY"))
    transcript = client.audio.transcriptions.create(
        model='whisper-1',
        file=audio
    )
    return transcript


@tool
def summarize_text(text: str, max_words: Optional[int] = 200, focus: Optional[str] = None) -> str:
    """Summarizes a piece of text using AI.

    Args:
        text: The text content to summarize
        max_words: Maximum number of words for the summary (default: 200)
        focus: Optional focus area for the summary (e.g., "technical details", "main arguments")

    Returns:
        A concise summary of the provided text
    """
    client = OpenAI(api_key=os.getenv("OPEN_AI_KEY"))

    # Build the prompt
    focus_instruction = f" with focus on {focus}" if focus else ""
    prompt = f"""
    Summarize the following text in {max_words} words or less{focus_instruction}.
    
    TEXT TO SUMMARIZE:
    {text}
    """

    # Generate the summary
    response = client.chat.completions.create(
        model=settings.OPENAI_LLM_MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that creates concise, accurate summaries."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1024
    )

    return response.choices[0].message.content.strip()


media_tools = [file_reader, audio_transcriber, summarize_text]
