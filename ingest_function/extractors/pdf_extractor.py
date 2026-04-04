"""Extract text from PDF files."""

from __future__ import annotations

from io import BytesIO


def extract_pdf_text(content: bytes | str) -> str:
    """Return the plain-text content of a PDF.

    Parameters
    ----------
    content:
        Either raw PDF bytes or a file-system path (str) to a PDF file.

    Returns
    -------
    str
        The concatenated text of all pages, separated by newlines.

    Raises
    ------
    ImportError
        If *pypdf* is not installed.
    ValueError
        If *content* is neither bytes nor a valid file path.
    """
    try:
        import pypdf
    except ImportError as exc:
        raise ImportError(
            "pypdf is required for PDF extraction. "
            "Install it with: pip install pypdf"
        ) from exc

    if isinstance(content, (bytes, bytearray)):
        reader = pypdf.PdfReader(BytesIO(content))
    elif isinstance(content, str):
        reader = pypdf.PdfReader(content)
    else:
        raise ValueError(
            f"content must be bytes or a file path str, got {type(content)!r}"
        )

    pages: list[str] = []
    for page in reader.pages:
        page_text = page.extract_text() or ""
        pages.append(page_text)

    return "\n".join(pages).strip()
