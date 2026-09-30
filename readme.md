# Atlas Ops — Internal Operations API (v2.2.0)

[![CI Test Suite & Coverage Guard](https://github.com/philip-muhire/atlas_ops_pipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/philip-muhire/atlas_ops_pipeline/actions/workflows/ci.yml)
![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)
![Coverage 100%](https://img.shields.io/badge/coverage-100%25-brightgreen.svg)

A production-ready, cloud-backed internal operations pipeline and REST API built with **FastAPI**, **SQLAlchemy**, and **Pydantic V2**. Designed for high-reliability backend operations with strict Role-Based Access Control (RBAC), end-to-end request correlation, and 100% test coverage.

---

## Key Features & Architecture

* **Role-Based Access Control (RBAC):** Custom dependency-injected security middleware validating request identity via `X-User-Role` headers.
* **Observability & Request Correlation:** Every incoming request receives a unique `CorrelationID` tracked across API endpoints and database service interactions.
* **Idempotent Data Ingestion:** Automated ingestion engine for streaming, validating, and upserting operations datasets with full deduplication.
* **Full Test Coverage:** 100% line coverage enforced automatically via GitHub Actions CI pipeline on every push.

---

## Role Matrix (Access Control)

| Role | Read (Customers / Tickets / Orders) | Create Tickets | Create Customers & Orders |
| :--- | :---: | :---: | :---: |
| `viewer` | ✅ | ❌ | ❌ |
| `support_agent` | ✅ | ✅ | ❌ |
| `billing_admin` | ✅ | ✅ | ✅ |

---

## Tech Stack

* **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
* **ORM / Database:** [SQLAlchemy](https://www.sqlalchemy.org/) & SQLite
* **Data Validation:** [Pydantic V2](https://docs.pydantic.dev/latest/)
* **Testing & CI:** `pytest`, `pytest-cov`, GitHub Actions
* **Language:** Python 3.12

---

## Getting Started

### 1. Prerequisites
Ensure you have Python 3.12+ installed on your environment.

### 2. Installation & Setup
```bash
# Clone repository
git clone [https://github.com/philip-muhire/atlas_ops_pipeline.git](https://github.com/philip-muhire/atlas_ops_pipeline.git)
cd atlas_ops_pipeline

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
