"""Format a summary as a plain email message."""

from __future__ import annotations

import textwrap


def format_as_email(
    summary: str,
    *,
    recipient: str = "",
    sender: str = "Document Summary Service",
    subject: str = "Document Summary",
) -> str:
    """Wrap *summary* in a simple plain-text email format.

    Parameters
    ----------
    summary:
        The document summary text.
    recipient:
        The ``To`` address (optional).
    sender:
        The ``From`` name / address.
    subject:
        The email subject line.

    Returns
    -------
    str
        A plain-text string formatted as an email message body.
    """
    lines: list[str] = []

    if recipient:
        lines.append(f"To: {recipient}")
    lines.append(f"From: {sender}")
    lines.append(f"Subject: {subject}")
    lines.append("")
    lines.append("Hello,")
    lines.append("")
    lines.append("Please find below a summary of the document you submitted:")
    lines.append("")
    lines.extend(textwrap.wrap(summary, width=80) if summary else [summary])
    lines.append("")
    lines.append("Kind regards,")
    lines.append(sender)

    return "\n".join(lines)
