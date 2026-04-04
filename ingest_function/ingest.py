"""Main entry point for the document ingestion and summarisation function.

This module exposes ``summarize_document``, the single function an AI Agent
needs to call in order to ingest a document and receive a clear, concise
summary in the requested output format.
"""

from __future__ import annotations

from typing import Literal

from .extractors.email_extractor import extract_email_text
from .extractors.pdf_extractor import extract_pdf_text
from .extractors.text_extractor import extract_plain_text
from .formatters.email_formatter import format_as_email
from .formatters.text_formatter import format_as_text
from .summarizer import summarize_text

# Supported input and output types (used for validation and type hints)
InputType = Literal["pdf", "email", "text"]
OutputFormat = Literal["email", "text"]


def summarize_document(
    content: str | bytes,
    input_type: InputType,
    output_format: OutputFormat = "text",
    *,
    recipient_email: str = "",
    sender_name: str = "Document Summary Service",
    email_subject: str = "Document Summary",
    model: str = "gpt-4o-mini",
) -> str:
    """Ingest a document and return a clear, concise summary.

    This function is designed to be called directly by an AI Agent.  It
    accepts documents in PDF, email (RFC 2822 / MIME), or plain-text form,
    extracts the textual content, generates a summary using an LLM, and
    returns the result in the requested output format.

    Parameters
    ----------
    content:
        The document to summarise.

        * ``"pdf"`` – raw PDF bytes **or** a filesystem path (``str``) to a
          ``.pdf`` file.
        * ``"email"`` – raw email message as a ``str`` or ``bytes``
          (RFC 2822 / MIME format).
        * ``"text"`` – plain text string (copy-pasted or otherwise).

    input_type:
        One of ``"pdf"``, ``"email"``, or ``"text"``.

    output_format:
        One of ``"text"`` (default) or ``"email"``.

        * ``"text"`` – returns a plain-text summary with a simple
          header/footer.
        * ``"email"`` – returns a formatted plain-text email message
          containing the summary.

    recipient_email:
        (Optional) The ``To:`` address used when *output_format* is
        ``"email"``.

    sender_name:
        Sender name / address used in the ``From:`` line when
        *output_format* is ``"email"`` (default: ``"Document Summary
        Service"``).

    email_subject:
        Subject line used when *output_format* is ``"email"`` (default:
        ``"Document Summary"``).

    model:
        OpenAI model to use for summarisation (default: ``"gpt-4o-mini"``).

    Returns
    -------
    str
        The document summary, formatted according to *output_format*.

    Raises
    ------
    ValueError
        If *input_type* or *output_format* is not one of the supported
        values, or if the document content is empty / unreadable.
    EnvironmentError
        If the ``OPENAI_API_KEY`` environment variable is not set.
    ImportError
        If a required optional dependency (``pypdf``, ``openai``) is not
        installed.

    Examples
    --------
    Plain-text summary of copy-pasted text::

        from ingest_function import summarize_document

        result = summarize_document(
            content="The quarterly report shows a 12 % increase in revenue...",
            input_type="text",
            output_format="text",
        )
        print(result)

    Email-formatted summary of a PDF file::

        result = summarize_document(
            content="/path/to/report.pdf",
            input_type="pdf",
            output_format="email",
            recipient_email="alice@example.com",
        )
        print(result)
    """
    # ------------------------------------------------------------------
    # 1. Extract plain text from the document
    # ------------------------------------------------------------------
    input_type = input_type.lower()  # type: ignore[assignment]

    if input_type == "pdf":
        extracted_text = extract_pdf_text(content)
    elif input_type == "email":
        extracted_text = extract_email_text(content)
    elif input_type == "text":
        extracted_text = extract_plain_text(content)
    else:
        raise ValueError(
            f"Unsupported input_type {input_type!r}. "
            "Must be one of: 'pdf', 'email', 'text'."
        )

    # ------------------------------------------------------------------
    # 2. Summarise
    # ------------------------------------------------------------------
    summary = summarize_text(extracted_text, model=model)

    # ------------------------------------------------------------------
    # 3. Format output
    # ------------------------------------------------------------------
    output_format = output_format.lower()  # type: ignore[assignment]

    if output_format == "text":
        return format_as_text(summary)
    elif output_format == "email":
        return format_as_email(
            summary,
            recipient=recipient_email,
            sender=sender_name,
            subject=email_subject,
        )
    else:
        raise ValueError(
            f"Unsupported output_format {output_format!r}. "
            "Must be one of: 'text', 'email'."
        )
