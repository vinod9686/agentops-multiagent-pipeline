# tools.py -- the agent's tools: a text analyzer and longest word finder
import re
from langchain_core.tools import tool

@tool
def analyze_text(text: str) -> str:
    """Analyze a piece of text and report its word count,
    sentence count, character count and reading time."""
    words = text.split()
    sentences = [s for s in re.split(r"[.!?]+", text) if s.strip()]
    minutes = len(words) / 200  # adults read about 200 words/minute
    return (
        f"Words: {len(words)}, Sentences: {len(sentences)}, "
        f"Characters: {len(text)}, Reading time: {minutes:.1f} min"
    )

@tool
def find_longest_word(text: str) -> str:
    """Find and return the longest word in the text."""
    words = re.findall(r"\b\w+\b", text)
    if not words:
        return "No words found."
    longest = max(words, key=len)
    return f"Longest word: '{longest}' ({len(longest)} characters)"
