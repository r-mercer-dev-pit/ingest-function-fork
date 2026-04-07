"""Extract text from raw email messages (RFC 2822 / MIME)."""

from __future__ import annotations

import email as _email
from email import policy as _policy


def extract_email_text(content: str | bytes) -> str:
    """Return the human-readable text body of an email message.

    The function prefers the ``text/plain`` part; if none exists it falls
    back to the ``text/html`` part (stripped of HTML tags).

    Parameters
    ----------
    content:
        A raw email message as a string or bytes (RFC 2822 / MIME format).

    Returns
    -------
    str
        Subject, sender, and body concatenated as plain text.

    Raises
    ------
    ValueError
        If no text content can be extracted.
    """
    if isinstance(content, bytes):
        msg = _email.message_from_bytes(content, policy=_policy.default)
    else:
        msg = _email.message_from_string(content, policy=_policy.default)

    subject = msg.get("Subject", "")
    sender = msg.get("From", "")

    body = _extract_body(msg)

    parts: list[str] = []
    if sender:
        parts.append(f"From: {sender}")
    if subject:
        parts.append(f"Subject: {subject}")
    if body:
        parts.append(body)

    if not parts:
        raise ValueError("No readable text content found in the email message.")

    return "\n".join(parts).strip()


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _extract_body(msg: _email.message.Message) -> str:
    """Walk the MIME tree and return the best plain-text representation."""
    plain_parts: list[str] = []
    html_parts: list[str] = []

    if msg.is_multipart():
        for part in msg.walk():
            ct = part.get_content_type()
            disposition = str(part.get("Content-Disposition", ""))
            if "attachment" in disposition:
                continue
            if ct == "text/plain":
                plain_parts.append(_decode_part(part))
            elif ct == "text/html":
                html_parts.append(_strip_html(_decode_part(part)))
    else:
        ct = msg.get_content_type()
        if ct == "text/plain":
            plain_parts.append(_decode_part(msg))
        elif ct == "text/html":
            html_parts.append(_strip_html(_decode_part(msg)))

    if plain_parts:
        return "\n".join(plain_parts)
    if html_parts:
        return "\n".join(html_parts)
    return ""


def _decode_part(part: _email.message.Message) -> str:
    """Decode a single MIME part to a string."""
    try:
        payload = part.get_payload(decode=True)
        if payload is None:
            return ""
        charset = part.get_content_charset() or "utf-8"
        return payload.decode(charset, errors="replace")
    except Exception:
        return ""


def _strip_html(html: str) -> str:
    """Very lightweight HTML → plain-text (no extra dependencies)."""
    import re

    # Remove script/style blocks
    html = re.sub(
        r"<(script|style)[^>]*>.*?</\1>", "", html, flags=re.DOTALL | re.IGNORECASE
    )
    # Replace block-level tags with newlines
    html = re.sub(r"<(br|p|div|h[1-6]|li|tr)[^>]*>", "\n", html, flags=re.IGNORECASE)
    # Remove remaining tags
    html = re.sub(r"<[^>]+>", "", html)
    # Decode common HTML entities
    html = html.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    html = html.replace("&nbsp;", " ").replace("&quot;", '"').replace("&#39;", "'")
    # Collapse whitespace
    html = re.sub(r"\n{3,}", "\n\n", html)
    return html.strip()
