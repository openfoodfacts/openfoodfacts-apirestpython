# AGENTS.md — Guidelines for AI Coding Agents

Welcome to `openfoodfacts-apirestpython`! This repository is a Python/Flask REST API that interfaces with an Open Food Facts MongoDB database to query and serve product information.

This document establishes the ground rules, workflows, quality standards, and Pull Request conventions for AI coding agents (and human contributors using LLM tools). Following these rules ensures high code quality, protects reviewer time, and keeps token usage efficient.

---

## 1. Core Operating Principles

1. **Target Branch is `develop`**: All pull requests must be opened against the `develop` branch, never `master` or `main`.
2. **Semantic PR Titles**: PR titles **must** adhere to [Conventional Commits](https://www.conventionalcommits.org/) (e.g. `feat: ...`, `fix: ...`, `chore: ...`, `test: ...`, `docs: ...`) because `.github/workflows/semantic-pr.yml` and `release-please` enforce this.
3. **Surgical, Minimal Changes**: Make only changes requested or strictly necessary to solve the issue. Avoid touching unrelated formatting, re-sorting imports without reason, or rewriting working code.
4. **Mandatory LLM Disclosure**: Every PR with agent-generated or agent-assisted code must explicitly declare LLM assistance and human validation.
5. **Before-and-After Visual Proof**: Every PR must include side-by-side evidence:
   - For UI/templates/CSS/documentation changes: **Screenshots** or screen recordings.
   - For API/backend changes: **Before vs. After terminal/curl outputs and response diffs**.

---

## 2. Token & Context Conservation Rules

To minimize token consumption, latency, and context window bloat:

- **Targeted Reading**: Never read entire large files when you only need a specific function or route. Use line ranges or search tools.
- **Do Not Ingest Big Dumps**: Never dump raw MongoDB BSON/JSON dumps or multi-megabyte API responses into the context. Use `head -n 20` or extract only relevant fields.
- **Targeted Execution**:
  - Run `flake8` against the specific modified file first before running repo-wide checks:
    ```bash
    flake8 flask_rest_service/resources_products.py
    ```
  - Run specific pytest test cases rather than entire suites when iterating:
    ```bash
    pytest tests/test_products.py -k test_barcode_lookup
    ```
- **Inspect `git diff` Locally First**: Always review `git diff` before committing to catch accidental whitespace edits, debug logs (`print()`), or leftover scratch files.

---

## 3. Technology Stack & Key Files

| Component | Technology / Value | Notes |
| :--- | :--- | :--- |
| **Python** | `3.11` | Pinned in `.python-version` |
| **Framework** | Flask 2.0.x + Flask-RESTful | Core web framework |
| **Database** | MongoDB + Flask-PyMongo / PyMongo 4.x | Default collection: `off-fr.products` |
| **Entry Point** | `runApiRESTServer.py` | Local development server |
| **Application Package** | `flask_rest_service/` | REST resources, configuration, templates |
| **Linting** | `flake8` | Max line length: 127 |
| **Testing** | `pytest` | Unit tests & smoke tests |

### Directory Map
```text
.
├── .github/
│   ├── workflows/
│   │   ├── ci.yml            # Linting (flake8), pytest, and MongoDB smoke tests
│   │   ├── semantic-pr.yml   # Enforces conventional commit titles
│   │   └── release-please.yml# Automated release management
├── flask_rest_service/
│   ├── __init__.py           # Flask app factory, MongoDB init, JSON serializer
│   ├── resources_root.py     # GET / health and status check
│   ├── resources_products.py # GET /product/<barcode>, GET /products, GET /products/<facet>
│   ├── resources_stats.py    # GET /stats endpoint
│   ├── templates/            # HTML templates
│   └── static/               # CSS and JS assets
├── requirements.txt          # Python dependencies
├── runApiRESTServer.py       # Local development runner
└── .python-version           # Single source of truth for Python version (3.11.x)
```

---

## 4. Local Development & Verification Workflow

Agents must verify their work using the following steps before declaring a task complete:

### 4.1. Setup Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install flake8 pytest
```

### 4.2. Running Linters
CI enforces strict syntax checks and code style:
```bash
# Fail on syntax errors or undefined names
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

# Style checks (max line length 127)
flake8 . --count --max-complexity=10 --max-line-length=127 --statistics
```

### 4.3. Minimal Seed & Local Smoke Test
If MongoDB is running locally (`mongodb://localhost:27017/`), you can seed a minimal fixture and test endpoints:

```bash
# Seed minimal fixture for local verification
python -c "from pymongo import MongoClient; c=MongoClient('mongodb://localhost:27017/'); c['off-fr'].products.insert_many([{'code':'737628064502','product_name':'Stir-Fry Rice Noodles','created_t':1345799269},{'code':'3017620422003','product_name':'Nutella','brands':'Ferrero','created_t':1345799270}])"

# Run API in the background (or in a separate terminal)
MONGO_URL="mongodb://localhost:27017/off-fr" PORT=5000 python runApiRESTServer.py

# Verify endpoints
curl -sf http://localhost:5000/ | grep '"status": "OK"'
curl -sf http://localhost:5000/product/737628064502 | grep 'Stir-Fry'
curl -sf "http://localhost:5000/products?limit=1" | grep 'product_name'
```

---

## 5. Coding Standards & Security

1. **Prevent MongoDB Injections**:
   - Sanitize all query arguments received from `request.args`.
   - Never pass unvalidated user input directly into `$where` or regex constructs without escaping special regex characters (`re.escape`).
2. **Barcode Validation**:
   - Validate barcode strings (strip whitespace, ensure digits / EAN length check where applicable).
3. **Response Structure Consistency**:
   - Maintain the standard JSON envelope (`status`, `status_verbose`, `product` / `products`). Do not alter existing response keys or types without explicit approval.
4. **Performance & Memory**:
   - Always enforce limits on database queries (default `limit=50`).
   - Use projection (e.g. `short=1`) when querying lists of products to avoid loading massive documents into memory.

---

## 6. Pull Request Requirements

Reviewers are volunteers and maintainers whose time is valuable. Every PR submitted by an AI agent (or human using AI) must adhere to these standards:

### 6.1. PR Title Format
Follow Conventional Commits:
- `fix(products): handle invalid barcodes gracefully`
- `feat(api): add dietary fiber facet query`
- `chore(deps): bump flask from 2.0.2 to 2.0.3`
- `test(smoke): add test for allergen filter`

### 6.2. LLM Disclosure Requirement
Always disclose:
1. Which agent/model was used (e.g., `Antigravity / Claude 3.7 Sonnet`, `Gemini 2.5 Flash`, etc.).
2. Which files were modified by the LLM.
3. What verification steps were executed by a human or agent test runner.

### 6.3. Before-and-After Visual Evidence Requirement
- **UI / HTML / Web Views**: Attach side-by-side screenshots (Before vs. After).
- **REST API Endpoints**: Paste formatted curl commands and output differences:

```markdown
#### 📸 Before / After Evidence

**Endpoint:** `GET /product/00000000`

*Before (500 Error / Crash):*
```json
Internal Server Error: KeyError 'product'
```

*After (200 / Clean JSON 404):*
```json
{
  "status": 0,
  "status_verbose": "product not found"
}
```
```

---

## 7. Standard Pull Request Template

Copy and paste the template below when opening a Pull Request:

```markdown
## Summary
<!-- Concise 1-2 sentence explanation of the change -->

## Motivation & Context
<!-- Why is this change required? What issue does it fix? Link issue: Fixes #123 -->

## Type of Change
- [ ] 🐛 Bug fix (non-breaking change which fixes an issue)
- [ ] ✨ New feature (non-breaking change which adds functionality)
- [ ] 🧹 Code refactor / cleanup
- [ ] 📝 Documentation update
- [ ] 🧪 Tests addition / modification

## 📸 Before / After Evidence
<!-- 
MANDATORY:
- For Web/UI/Doc changes: Add Before and After screenshots/GIFs.
- For API/Backend changes: Add Before and After terminal output, curl responses, or JSON diffs.
-->

| Before | After |
| :---: | :---: |
| *(paste before screenshot or curl output)* | *(paste after screenshot or curl output)* |

## 🤖 LLM / AI Disclosure
- **Assisted by**: [e.g. Antigravity Agent / Claude / Gemini / Copilot]
- **Scope of Generation**: [e.g. Entire function `validate_barcode` and unit tests / Refactored existing query]
- **Verification**: [e.g. Ran pytest, executed smoke test with seeded MongoDB, checked flake8]

## Checklist
- [ ] My PR targets the `develop` branch.
- [ ] PR title follows [Conventional Commits](https://www.conventionalcommits.org/).
- [ ] `flake8 .` passes without errors or warnings.
- [ ] Local tests (`pytest` and/or smoke checks) pass.
- [ ] No extraneous debug statements, temporary files, or commented-out code left behind.
- [ ] Documentation updated if API contracts changed.
```

---

## 8. Agent Pre-Submission Checklist

Before finalizing any task, the AI agent must run through this checklist:

- [ ] Ran `git status` to verify no untracked files or unintentional edits exist.
- [ ] Ran `flake8` to confirm no linting violations.
- [ ] Tested the changed logic with edge cases (empty inputs, non-existent records, invalid query params).
- [ ] Verified that changes are backwards-compatible with existing API consumers.
- [ ] Prepared the PR title in Conventional Commit format.
- [ ] Prepared the PR body with the LLM Disclosure and Before/After verification data.
