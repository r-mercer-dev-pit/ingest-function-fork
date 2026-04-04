"""LLM-powered summarisation via the OpenAI API."""

from __future__ import annotations

import os


_SYSTEM_PROMPT = (
    "You are a highly skilled summarisation assistant. "
    "Read the provided document and produce a clear, concise summary that captures "
    "the key points, main arguments, and any important conclusions. "
    "The summary should be accurate, well-structured, and written in plain English."
)


def summarize_text(text: str, model: str = "gpt-4o-mini") -> str:
    """Summarise *text* using the OpenAI Chat Completions API.

    Parameters
    ----------
    text:
        The extracted document text to summarise.
    model:
        OpenAI model name to use (default ``gpt-4o-mini``).

    Returns
    -------
    str
        The generated summary.

    Raises
    ------
    ImportError
        If *openai* is not installed.
    EnvironmentError
        If the ``OPENAI_API_KEY`` environment variable is not set.
    """
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise ImportError(
            "openai is required for summarisation. "
            "Install it with: pip install openai"
        ) from exc

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "OPENAI_API_KEY environment variable is not set. "
            "Set it before calling summarize_document()."
        )

    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": _SYSTEM_PROMPT},
            {"role": "user", "content": text},
        ],
        temperature=0.3,
    )

    content = response.choices[0].message.content
    if content is None:
        raise ValueError(
            "The OpenAI API returned an empty response. "
            "The document may have triggered a content policy filter."
        )
    return content.strip()
