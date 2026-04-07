# ingest-function

A Python function, callable by an AI Agent, that ingests documents and returns clear, concise summaries.

## Features

| Input type | Description |
|------------|-------------|
| `pdf` | Raw PDF bytes **or** a file path to a `.pdf` file |
| `email` | Raw email message (RFC 2822 / MIME) as `str` or `bytes` |
| `text` | Plain copy-pasted text (`str`) |

| Output format | Description |
|---------------|-------------|
| `text` | Plain-text summary with a header/footer (default) |
| `email` | Plain-text email message containing the summary |

Summarisation is powered by the **OpenAI Chat Completions API** (`gpt-4o-mini` by default).

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Set the `OPENAI_API_KEY` environment variable before calling the function:

```bash
export OPENAI_API_KEY="sk-..."
```

## Usage

```python
from ingest_function import summarize_document

# Summarise copy-pasted text → plain text output
result = summarize_document(
    content="The quarterly report shows a 12% increase in revenue...",
    input_type="text",
    output_format="text",
)
print(result)

# Summarise a PDF file → email output
result = summarize_document(
    content="/path/to/report.pdf",
    input_type="pdf",
    output_format="email",
    recipient_email="alice@example.com",
)
print(result)

# Summarise a raw email message → plain text output
with open("message.eml", "rb") as f:
    raw_email = f.read()

result = summarize_document(
    content=raw_email,
    input_type="email",
    output_format="text",
)
print(result)
```

### `summarize_document` parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `content` | `str \| bytes` | *required* | Document content (see Input types above) |
| `input_type` | `"pdf" \| "email" \| "text"` | *required* | Format of the input document |
| `output_format` | `"text" \| "email"` | `"text"` | Desired output format |
| `recipient_email` | `str` | `""` | `To:` address (email output only) |
| `sender_name` | `str` | `"Document Summary Service"` | `From:` name (email output only) |
| `email_subject` | `str` | `"Document Summary"` | Subject line (email output only) |
| `model` | `str` | `"gpt-4o-mini"` | OpenAI model used for summarisation |

## Project structure

```
ingest_function/
├── __init__.py          # Public API
├── ingest.py            # Main entry point (summarize_document)
├── summarizer.py        # OpenAI-powered summarisation
├── extractors/
│   ├── pdf_extractor.py    # PDF → text (pypdf)
│   ├── email_extractor.py  # Email → text (stdlib email)
│   └── text_extractor.py   # Plain text passthrough
└── formatters/
    ├── email_formatter.py  # Summary → email message
    └── text_formatter.py   # Summary → plain text
tests/
└── test_ingest.py       # Unit tests
```

## Running tests

```bash
pytest tests/
```
