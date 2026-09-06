# EduPulse AI — Durable File Map & Per-File Explanation Record

Status: LIVE — Updated after every file creation or modification.

---

## 1. PROJECT ARCHITECTURE FILE MAP

| File Path | Why it Exists (Architectural Gap) | What it Does (Plain Language) | Where to Start Reading | Latest Action / Changes Made |
|---|---|---|---|---|
| [`docs/DEVELOPMENT_RULES.md`](file:///c:/MindForge/Project/Agent%20Orchestration%20Framework%20with%20Lang%20Chain/docs/DEVELOPMENT_RULES.md) | Enforces development discipline & AI protocols | Defines testing, security, debugging, file-mapping, prompt authorization, and commit conventions | Section 11 (Conventional Commits) | Added Section 11 Lead Software Architect Conventional Commits rules |
| [`FILE-MAP.md`](file:///c:/MindForge/Project/Agent%20Orchestration%20Framework%20with%20Lang%20Chain/FILE-MAP.md) | Single source of truth for repository structure | Durable record explaining why files exist, what they do, and where to start | Section 1 (Table) | Logged api/app.py root endpoint and commit guidelines |
| [`src/core/lru_cache.py`](file:///c:/MindForge/Project/Agent%20Orchestration%20Framework%20with%20Lang%20Chain/src/core/lru_cache.py) | Bounds in-memory state complexity | Implements $O(1)$ Doubly Linked List + Hash Map LRU cache | `class LRUCache` constructor | Implemented $O(1)$ `get`, `put`, and sentinel nodes |
| [`tests/test_dsa_cache.py`](file:///c:/MindForge/Project/Agent%20Orchestration%20Framework%20with%20Lang%20Chain/tests/test_dsa_cache.py) | Validates LRU cache correctness & speed | Pytest suite testing eviction, edge cases, and $O(1)$ benchmark | `test_o1_benchmark()` | Verified 8 unit tests + 0.00028 ms performance benchmark |
| [`src/utils/logger.py`](file:///c:/MindForge/Project/Agent%20Orchestration%20Framework%20with%20Lang%20Chain/src/utils/logger.py) | Prevents unhandled log file growth | Rotating file & stream logger (5 MB max, 3 backups) | `def get_logger()` | Created idempotent logger utility |
| [`src/utils/exception.py`](file:///c:/MindForge/Project/Agent%20Orchestration%20Framework%20with%20Lang%20Chain/src/utils/exception.py) | Preserves enterprise error tracebacks | Wraps exceptions with exact file name and line number | `class CustomException` | Created CustomException error wrapper |
| [`src/core/config.py`](file:///c:/MindForge/Project/Agent%20Orchestration%20Framework%20with%20Lang%20Chain/src/core/config.py) | Manages system settings safely | Pydantic BaseSettings singleton loading `.env` variables | `class Settings` | Added `OPENROUTER_MODEL` and multi-key support |
| [`api/app.py`](file:///c:/MindForge/Project/Agent%20Orchestration%20Framework%20with%20Lang%20Chain/api/app.py) | Baseline backend entrypoint | Exposes `GET /` metadata and `GET /health` endpoints for Docker and Render | `read_root()` | Added `GET /` endpoint returning JSON metadata for clean web visits |
| [`.github/workflows/ci.yml`](file:///c:/MindForge/Project/Agent%20Orchestration%20Framework%20with%20Lang%20Chain/.github/workflows/ci.yml) | Automated quality control on push | Runs flake8 linting and pytest suite in CI runner | `jobs: lint-and-test` | Configured GitHub Actions CI pipeline |
| [`.github/workflows/cd.yml`](file:///c:/MindForge/Project/Agent%20Orchestration%20Framework%20with%20Lang%20Chain/.github/workflows/cd.yml) | Automated cloud continuous deployment | Triggers Render deploy hook upon successful CI build | `jobs: deploy` | Added safe env check for Render deploy hook |
| [`Dockerfile`](file:///c:/MindForge/Project/Agent%20Orchestration%20Framework%20with%20Lang%20Chain/Dockerfile) | Production containerization | Multi-stage build running non-root `edupulse` user on port 8000 | Runtime Stage | Created secure 2-stage Dockerfile |
| [`docker-compose.yml`](file:///c:/MindForge/Project/Agent%20Orchestration%20Framework%20with%20Lang%20Chain/docker-compose.yml) | Local service orchestration | Runs backend container with `./data` and `./logs` volume mounts | `services: backend` | Mapped port 8000:8000 and volume persistence |
| [`setup.py`](file:///c:/MindForge/Project/Agent%20Orchestration%20Framework%20with%20Lang%20Chain/setup.py) | Package distribution | Installs `edupulse-ai` package in editable mode (`pip install -e .`) | `setup()` call | Defined package metadata and structure |
