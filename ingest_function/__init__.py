"""
ingest_function – document ingestion and summarisation for AI Agents.

Public API
----------
    summarize_document(content, input_type, output_format, ...)
"""

from .ingest import summarize_document

__all__ = ["summarize_document"]
