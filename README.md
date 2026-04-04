# ingest-function

A Python function, callable by an AI Agent, that ingests documents and returns clear, concise summaries.

---

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Running Tests](#running-tests)
- [Development Workflow](#development-workflow)
- [GitHub Codespaces](#github-codespaces)
- [GitHub Spark](#github-spark)
- [Contributing](#contributing)
- [License](#license)

---

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

---

## Installation

```bash
pip install -r requirements.txt
```

---

## Configuration

Set the `OPENAI_API_KEY` environment variable before calling the function:

```bash
export OPENAI_API_KEY="sk-..."
```

---

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

---

## Project Structure

```
ingest-function/
├── ingest_function/
│   ├── __init__.py          # Public API (summarize_document)
│   ├── ingest.py            # Main entry point
│   ├── summarizer.py        # OpenAI-powered summarisation
│   ├── extractors/
│   │   ├── __init__.py
│   │   ├── pdf_extractor.py    # PDF → text (pypdf)
│   │   ├── email_extractor.py  # Email → text (stdlib email)
│   │   └── text_extractor.py   # Plain text passthrough
│   └── formatters/
│       ├── __init__.py
│       ├── email_formatter.py  # Summary → email message
│       └── text_formatter.py   # Summary → plain text
├── tests/
│   └── test_ingest.py       # Unit tests
├── .devcontainer/
│   └── devcontainer.json    # GitHub Codespaces configuration
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Running Tests

```bash
pytest tests/
```

---

## Development Workflow

1. **Branch** — create a feature branch from `main`
2. **Code** — make changes in the relevant module
3. **Test** — run `pytest tests/` and ensure all tests pass
4. **Commit** — write a descriptive commit message
5. **Pull Request** — open a PR with a clear description of what and why

---

## GitHub Codespaces

The repository includes a `.devcontainer/devcontainer.json` that gives you a fully configured, zero-setup cloud development environment in seconds.

### Launching a Codespace

1. Click the green **Code** button on the repository home page
2. Select the **Codespaces** tab
3. Click **Create codespace on main**

The Codespace will automatically:

- Provision a container with Python 3.11
- Install all project dependencies from `requirements.txt`
- Install recommended VS Code extensions (Pylance, Ruff, Python Test Explorer)

### Recommended Extensions (pre-installed in Codespace)

| Extension | Purpose |
|---|---|
| `ms-python.python` | Python language support |
| `ms-python.pylance` | Fast type-aware IntelliSense |
| `charliermarsh.ruff` | Lint & format on save |
| `ms-python.mypy-type-checker` | Inline type-checking |
| `hbenl.vscode-test-explorer` | Test Explorer UI |
| `GitHub.copilot` | AI-assisted code completion |
| `GitHub.copilot-chat` | In-editor AI chat |

### Tips for Codespaces

- Use **Codespace Secrets** (your GitHub profile → Settings → Codespaces → Secrets) to store your `OPENAI_API_KEY`. It will be automatically injected as an environment variable when the Codespace starts.
- Pin a specific machine type (4-core recommended) under repository Codespace settings for consistent performance.
- Commit `.devcontainer/devcontainer.json` to keep the environment reproducible for all contributors.

---

## GitHub Spark

[GitHub Spark](https://githubnext.com/projects/github-spark) is an AI-powered micro-app builder that lets you create small, focused tools that live alongside your repository. Several areas of this project are well-suited to Spark micro-apps:

### Suggested Spark Applications

#### 1. Document Summarisation UI
A simple form where a user can paste text or a URL and immediately receive a plain-text or email-formatted summary — no CLI knowledge required.

**Why Spark?** The entire interaction is a single function call (`summarize_document`). Spark's AI assistance can wire up a clean input/output form in minutes with no deployment overhead.

#### 2. Summarisation History Log
A read-only dashboard that displays recent summarisation requests: input type, output format, token usage, and the generated summary — useful for auditing or demos.

**Why Spark?** A simple table/card layout backed by a lightweight log file or storage endpoint is exactly the kind of small data-display app Spark handles well.

#### 3. Prompt Tuner
An interactive playground where you can adjust the summarisation prompt, change the model (`gpt-4o-mini`, `gpt-4o`, etc.), and compare outputs side-by-side without touching the codebase.

**Why Spark?** Iterating on prompt text benefits from a tight feedback loop. Spark lets you build a quick compare-UI without spinning up a separate app.

#### 4. API Key Validator
A simple tool that accepts an OpenAI API key, makes a lightweight test call, and confirms the key is valid and has sufficient quota — useful during onboarding.

**Why Spark?** A zero-deployment helper that reduces "why isn't it working?" friction for new contributors.

### How to Create a Spark App for This Project

1. Navigate to [https://githubnext.com/projects/github-spark](https://githubnext.com/projects/github-spark) and sign in with your GitHub account
2. Click **New Spark** and describe the app in natural language (e.g. *"Build a form that lets me paste text and get a summary using the OpenAI API"*)
3. Iterate with the AI editor — paste in your function signature, adjust the layout, add input validation
4. **Share** the Spark app URL with your team — no deployment required
5. Optionally, embed the Spark app URL in this README or in a GitHub Issue template for discoverability

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository and create a branch: `git checkout -b feat/your-feature`
2. Make your changes and add tests
3. Ensure `pytest tests/` passes
4. Open a Pull Request with a clear description of what and why

Please be respectful and constructive in all interactions.

---

## License

This project is licensed under the MIT License.

