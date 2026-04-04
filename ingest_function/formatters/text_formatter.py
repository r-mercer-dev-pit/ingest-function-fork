"""Format a summary as plain text."""

from __future__ import annotations


def format_as_text(summary: str) -> str:
    """Return *summary* as plain text with a minimal header.

    Parameters
    ----------
    summary:
        The document summary text.

    Returns
    -------
    str
        The summary wrapped with a simple header/footer.
    """
    separator = "=" * 60
    return f"{separator}\nDOCUMENT SUMMARY\n{separator}\n\n{summary}\n\n{separator}"
