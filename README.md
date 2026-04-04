# ingest-function

A Python-based data ingestion function designed to reliably pull data from external sources and load it into a target data store. Built with a serverless-first mindset, it can be deployed as an Azure Function, AWS Lambda, or run standalone in any Python environment.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
- [Running the Function](#running-the-function)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [Development Workflow](#development-workflow)
- [GitHub Codespaces](#github-codespaces)
- [GitHub Spark](#github-spark)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

`ingest-function` is a lightweight, extensible ingestion pipeline component. It is responsible for:

- Fetching raw data from one or more upstream sources (APIs, files, queues, databases)
- Applying basic validation and transformation
- Writing processed records to a downstream data store (blob storage, database, data warehouse)
- Emitting structured logs and metrics for observability

The function is stateless by design, making it easy to scale horizontally and deploy to any serverless runtime.

---

## Architecture

```
┌─────────────────────┐        ┌───────────────────────┐        ┌────────────────────┐
│   Upstream Source   │──────▶ │   ingest-function      │──────▶ │  Target Data Store │
│  (API / Queue / DB) │        │  (validate, transform) │        │ (Blob / DB / DW)   │
└─────────────────────┘        └───────────────────────┘        └────────────────────┘
                                          │
                                          ▼
                                ┌─────────────────────┐
                                │  Logging & Metrics  │
                                │  (App Insights / CW)│
                                └─────────────────────┘
```

The function follows a simple three-stage pipeline:

1. **Extract** — connect to the upstream source and retrieve raw records
2. **Transform** — validate, clean, and shape records to the target schema
3. **Load** — write transformed records to the downstream store and emit a summary

---

## Features

- ⚡ **Serverless-ready** — deploys to Azure Functions, AWS Lambda, or runs as a standalone script
- 🔄 **Idempotent ingestion** — duplicate records are detected and skipped
- 🔍 **Schema validation** — input records are validated before loading
- 📊 **Structured logging** — JSON logs for easy querying in any observability platform
- 🧪 **Fully testable** — pure Python core with no framework lock-in
- 🔒 **Secrets management** — credentials loaded from environment variables or a secrets manager (never hardcoded)

---

## Getting Started

### Prerequisites

- Python 3.11 or higher
- `pip` or [`uv`](https://github.com/astral-sh/uv) (recommended)
- Access credentials for your upstream source and target store

### Installation

```bash
# Clone the repository
git clone https://github.com/r-mercer/ingest-function.git
cd ingest-function

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Or with uv (faster)
uv sync
```

### Configuration

All configuration is provided via environment variables. Copy the example file and fill in your values:

```bash
cp .env.example .env
```

| Variable | Description | Required |
|---|---|---|
| `SOURCE_URL` | URL or connection string for the upstream source | ✅ |
| `SOURCE_API_KEY` | API key for the upstream source | ✅ |
| `TARGET_CONNECTION_STRING` | Connection string for the target data store | ✅ |
| `TARGET_CONTAINER` | Container / table / bucket name in the target store | ✅ |
| `BATCH_SIZE` | Number of records to process per invocation (default: `500`) | ❌ |
| `LOG_LEVEL` | Logging verbosity: `DEBUG`, `INFO`, `WARNING`, `ERROR` (default: `INFO`) | ❌ |

> **Never commit `.env` to source control.** It is already listed in `.gitignore`.

---

## Running the Function

### Locally (standalone)

```bash
python -m ingest_function
```

### With Azure Functions Core Tools

```bash
func start
```

### With Docker

```bash
docker build -t ingest-function .
docker run --env-file .env ingest-function
```

---

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=ingest_function --cov-report=term-missing

# Run linter
ruff check .

# Run type checker
mypy ingest_function/
```

Tests live in the `tests/` directory and follow the `test_<module>.py` naming convention. Unit tests use `pytest` with `unittest.mock` for dependency isolation.

---

## Project Structure

```
ingest-function/
├── ingest_function/        # Main package
│   ├── __init__.py
│   ├── __main__.py         # Entry point for `python -m ingest_function`
│   ├── extractor.py        # Upstream source connection & data fetch
│   ├── transformer.py      # Validation and schema mapping
│   ├── loader.py           # Target store writes
│   └── config.py           # Environment variable loading
├── tests/
│   ├── test_extractor.py
│   ├── test_transformer.py
│   └── test_loader.py
├── .devcontainer/
│   └── devcontainer.json   # GitHub Codespaces configuration
├── .env.example            # Example environment variable file
├── .gitignore
├── pyproject.toml          # Project metadata, dependencies, tool config
└── README.md
```

---

## Development Workflow

1. **Branch** — create a feature branch from `main`
2. **Code** — make changes in the relevant module
3. **Lint** — run `ruff check .` and fix any issues
4. **Type-check** — run `mypy ingest_function/`
5. **Test** — run `pytest` and ensure all tests pass
6. **Commit** — write a descriptive commit message
7. **Pull Request** — open a PR; CI will run lint, type-check, and tests automatically

Commits follow [Conventional Commits](https://www.conventionalcommits.org/) (`feat:`, `fix:`, `chore:`, etc.).

---

## GitHub Codespaces

The repository includes a `.devcontainer/devcontainer.json` that gives you a fully configured, zero-setup cloud development environment in seconds.

### Launching a Codespace

1. Click the green **Code** button on the repository home page
2. Select the **Codespaces** tab
3. Click **Create codespace on main**

The Codespace will automatically:

- Provision a container with Python 3.11
- Install all project dependencies via `uv sync` (or `pip install -r requirements.txt`)
- Install recommended VS Code extensions (Pylance, Ruff, Python Test Explorer)
- Set up `pre-commit` hooks for linting and formatting
- Forward any necessary ports for local function execution

### Recommended Extensions (pre-installed in Codespace)

| Extension | Purpose |
|---|---|
| `ms-python.python` | Python language support |
| `ms-python.pylance` | Fast type-aware IntelliSense |
| `charliermarsh.ruff` | Lint & format on save |
| `ms-python.mypy-type-checker` | Inline type-checking |
| `hbenl.vscode-test-explorer` | Test Explorer UI |
| `ms-azuretools.vscode-azurefunctions` | Azure Functions local dev & deploy |

### Tips for Codespaces

- Use **Codespace Secrets** (under your GitHub profile → Codespaces → Secrets) to store `SOURCE_API_KEY`, `TARGET_CONNECTION_STRING`, and other sensitive values. They are automatically injected as environment variables.
- Pin a specific machine type (4-core recommended) under repository Codespace settings to ensure consistent performance.
- Use the **Ports** panel to expose the Azure Functions local runtime port (`7071`) for browser-based testing.
- Commit the `.devcontainer/devcontainer.json` to keep the environment reproducible for all contributors.

---

## GitHub Spark

[GitHub Spark](https://githubnext.com/projects/github-spark) is an AI-powered micro-app builder that lets you create small, focused tools that live alongside your repository. The following areas of this project are well-suited to Spark micro-apps:

### Suggested Spark Applications

#### 1. Ingestion Dashboard
A lightweight read-only dashboard that queries your target data store and displays:
- Total records ingested (today / this week / all time)
- Last successful run timestamp and record count
- Error rate trend chart

**Why Spark?** Spark excels at building small data-display apps with minimal boilerplate. A simple SQL or REST query → table/chart UI is exactly its sweet spot.

#### 2. Schema Explorer
An interactive tool that lets you paste or upload a sample JSON payload and instantly see:
- Auto-detected field types
- Validation rules that would be applied by the transformer
- A diff view comparing the sample against the current expected schema

**Why Spark?** The UI is entirely client-side (no backend deployment needed), and Spark's AI assistance can generate the schema-comparison logic quickly.

#### 3. Run Trigger UI
A simple form-based interface to manually trigger the ingest function with custom parameters (date range, batch size, source override) without needing CLI access. Useful for on-call engineers or non-technical stakeholders.

**Why Spark?** Replaces a curl/CLI command with a safe, discoverable UI that can be shared with anyone who has repository access.

#### 4. Environment Variable Validator
A Spark app that reads the `.env.example` file, presents a checklist of required variables, and lets you paste in values to validate format (URL syntax, key length, etc.) before adding them as Codespace or Actions secrets.

**Why Spark?** A zero-deployment helper that reduces onboarding friction with no infrastructure needed.

### How to Create a Spark App for This Project

1. Navigate to [https://githubnext.com/projects/github-spark](https://githubnext.com/projects/github-spark) and sign in with your GitHub account
2. Click **New Spark** and describe the app in natural language (e.g. *"Show me a table of the last 50 ingest runs from this Azure Table Storage account"*)
3. Iterate with the AI editor — paste in your schema, adjust the layout, add filters
4. **Share** the Spark app URL with your team — no deployment required
5. Optionally, embed the Spark app URL in this README or in a GitHub Issue template for discoverability

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository and create a branch: `git checkout -b feat/your-feature`
2. Make your changes and add tests
3. Ensure `ruff check .`, `mypy ingest_function/`, and `pytest` all pass
4. Open a Pull Request with a clear description of what and why

Please be respectful and constructive in all interactions.

---

## License

This project is licensed under the MIT License.
