"""Pass-through extractor for plain copy-pasted text."""

from __future__ import annotations


def extract_plain_text(content: str) -> str:
    """Return the content as-is after basic normalisation.

    Parameters
    ----------
    content:
        Raw text string (copy-pasted or otherwise supplied as plain text).

    Returns
    -------
    str
        The normalised text.

    Raises
    ------
    ValueError
        If *content* is empty or not a string.
    """
    if not isinstance(content, str):
        raise ValueError(
            f"content must be a str for plain-text extraction, got {type(content)!r}"
        )
    normalised = content.strip()
    if not normalised:
        raise ValueError("content is empty.")
    return normalised
