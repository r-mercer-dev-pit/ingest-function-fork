"""Tests for the document ingestion and summarisation function."""

from __future__ import annotations

import email as _email
import io
import textwrap
import types
import unittest
from unittest.mock import MagicMock, patch


# ---------------------------------------------------------------------------
# Extractor tests
# ---------------------------------------------------------------------------

class TestExtractPlainText(unittest.TestCase):
    """Tests for ingest_function.extractors.text_extractor."""

    def setUp(self):
        from ingest_function.extractors.text_extractor import extract_plain_text
        self.extract = extract_plain_text

    def test_returns_stripped_text(self):
        result = self.extract("  hello world  ")
        self.assertEqual(result, "hello world")

    def test_non_string_raises(self):
        with self.assertRaises(ValueError):
            self.extract(123)  # type: ignore[arg-type]

    def test_empty_string_raises(self):
        with self.assertRaises(ValueError):
            self.extract("   ")

    def test_multiline_text(self):
        text = "Line one.\nLine two.\nLine three."
        result = self.extract(text)
        self.assertEqual(result, text)


class TestExtractEmailText(unittest.TestCase):
    """Tests for ingest_function.extractors.email_extractor."""

    def setUp(self):
        from ingest_function.extractors.email_extractor import extract_email_text
        self.extract = extract_email_text

    def _make_email(self, subject: str, body: str, sender: str = "test@example.com") -> str:
        return (
            f"From: {sender}\r\n"
            f"Subject: {subject}\r\n"
            f"Content-Type: text/plain; charset=utf-8\r\n"
            f"\r\n"
            f"{body}"
        )

    def test_plain_text_email(self):
        raw = self._make_email("Test Subject", "Hello, this is the body.")
        result = self.extract(raw)
        self.assertIn("Test Subject", result)
        self.assertIn("Hello, this is the body.", result)
        self.assertIn("test@example.com", result)

    def test_bytes_input(self):
        raw = self._make_email("Bytes Subject", "Bytes body.").encode()
        result = self.extract(raw)
        self.assertIn("Bytes Subject", result)
        self.assertIn("Bytes body.", result)

    def test_empty_email_raises(self):
        with self.assertRaises(ValueError):
            self.extract("")

    def test_html_email_stripped(self):
        raw = (
            "From: sender@example.com\r\n"
            "Subject: HTML Email\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            "\r\n"
            "<html><body><p>Hello <b>world</b></p></body></html>"
        )
        result = self.extract(raw)
        self.assertIn("Hello", result)
        self.assertNotIn("<p>", result)
        self.assertNotIn("<b>", result)


class TestExtractPdfText(unittest.TestCase):
    """Tests for ingest_function.extractors.pdf_extractor."""

    def setUp(self):
        from ingest_function.extractors.pdf_extractor import extract_pdf_text
        self.extract = extract_pdf_text

    def test_missing_pypdf_raises_import_error(self):
        """If pypdf is not importable, a clear ImportError should be raised."""
        import sys
        with patch.dict(sys.modules, {"pypdf": None}):
            with self.assertRaises(ImportError):
                self.extract(b"%PDF-fake")

    def test_invalid_type_raises(self):
        with self.assertRaises((ValueError, Exception)):
            self.extract(12345)  # type: ignore[arg-type]

    def test_bytes_input_accepted(self):
        """Passing PDF bytes should not raise TypeError (actual parsing may fail)."""
        try:
            import pypdf  # noqa: F401
        except ImportError:
            self.skipTest("pypdf not installed")

        # We only verify it does NOT raise TypeError; invalid PDF bytes will
        # raise a pypdf-specific error which is acceptable.
        try:
            self.extract(b"not a real pdf")
        except TypeError:
            self.fail("extract_pdf_text raised TypeError for bytes input")
        except Exception:
            pass  # other errors (invalid PDF) are expected with fake bytes

    def test_file_path_accepted(self):
        """Passing a file path string should not raise TypeError."""
        try:
            import pypdf  # noqa: F401
        except ImportError:
            self.skipTest("pypdf not installed")

        try:
            self.extract("/nonexistent/path/to/file.pdf")
        except TypeError:
            self.fail("extract_pdf_text raised TypeError for str file path")
        except Exception:
            pass  # FileNotFoundError or pypdf error expected


# ---------------------------------------------------------------------------
# Formatter tests
# ---------------------------------------------------------------------------

class TestFormatAsText(unittest.TestCase):
    """Tests for ingest_function.formatters.text_formatter."""

    def setUp(self):
        from ingest_function.formatters.text_formatter import format_as_text
        self.fmt = format_as_text

    def test_contains_summary(self):
        result = self.fmt("My summary.")
        self.assertIn("My summary.", result)

    def test_contains_header(self):
        result = self.fmt("Some text.")
        self.assertIn("DOCUMENT SUMMARY", result)

    def test_separator_present(self):
        result = self.fmt("x")
        self.assertIn("=" * 60, result)


class TestFormatAsEmail(unittest.TestCase):
    """Tests for ingest_function.formatters.email_formatter."""

    def setUp(self):
        from ingest_function.formatters.email_formatter import format_as_email
        self.fmt = format_as_email

    def test_contains_summary(self):
        result = self.fmt("My summary.")
        self.assertIn("My summary.", result)

    def test_contains_subject(self):
        result = self.fmt("x", subject="Test Subject")
        self.assertIn("Subject: Test Subject", result)

    def test_contains_recipient(self):
        result = self.fmt("x", recipient="alice@example.com")
        self.assertIn("To: alice@example.com", result)

    def test_no_recipient_omits_to_line(self):
        result = self.fmt("x")
        self.assertNotIn("To:", result)

    def test_default_sender(self):
        result = self.fmt("x")
        self.assertIn("Document Summary Service", result)


# ---------------------------------------------------------------------------
# Integration / ingest.py tests (mocked LLM)
# ---------------------------------------------------------------------------

class TestSummarizeDocument(unittest.TestCase):
    """End-to-end tests for summarize_document with a mocked summariser."""

    def setUp(self):
        from ingest_function.ingest import summarize_document
        self.fn = summarize_document

    def _mock_summarizer(self):
        """Return a context manager that patches summarize_text."""
        return patch(
            "ingest_function.ingest.summarize_text",
            return_value="Mocked summary.",
        )

    # -- input_type: text -----------------------------------------------------

    def test_text_input_text_output(self):
        with self._mock_summarizer():
            result = self.fn("Some document content.", input_type="text")
        self.assertIn("Mocked summary.", result)
        self.assertIn("DOCUMENT SUMMARY", result)

    def test_text_input_email_output(self):
        with self._mock_summarizer():
            result = self.fn(
                "Some document content.",
                input_type="text",
                output_format="email",
                recipient_email="bob@example.com",
            )
        self.assertIn("Mocked summary.", result)
        self.assertIn("Subject:", result)
        self.assertIn("bob@example.com", result)

    # -- input_type: email ----------------------------------------------------

    def test_email_input_text_output(self):
        raw_email = (
            "From: sender@example.com\r\n"
            "Subject: Hello\r\n"
            "Content-Type: text/plain; charset=utf-8\r\n"
            "\r\n"
            "Body text here."
        )
        with self._mock_summarizer():
            result = self.fn(raw_email, input_type="email")
        self.assertIn("Mocked summary.", result)

    # -- invalid input_type ---------------------------------------------------

    def test_invalid_input_type_raises(self):
        with self.assertRaises(ValueError):
            self.fn("content", input_type="docx")  # type: ignore[arg-type]

    def test_invalid_output_format_raises(self):
        with self._mock_summarizer():
            with self.assertRaises(ValueError):
                self.fn("content", input_type="text", output_format="html")  # type: ignore[arg-type]

    # -- empty content --------------------------------------------------------

    def test_empty_text_raises(self):
        with self.assertRaises(ValueError):
            self.fn("   ", input_type="text")

    # -- case insensitivity ---------------------------------------------------

    def test_input_type_case_insensitive(self):
        with self._mock_summarizer():
            result = self.fn("Some content.", input_type="TEXT")  # type: ignore[arg-type]
        self.assertIn("Mocked summary.", result)

    def test_output_format_case_insensitive(self):
        with self._mock_summarizer():
            result = self.fn(
                "Some content.", input_type="text", output_format="EMAIL"  # type: ignore[arg-type]
            )
        self.assertIn("Subject:", result)


if __name__ == "__main__":
    unittest.main()
