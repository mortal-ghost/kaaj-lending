# Lender Matching Platform

A full-stack application to match business loan applications with lender credit policies.

## Features

- **Policy Engine**: flexible, JSON-based rule engine to evaluate FICO, Time in Business, Revenue, etc.
- **Lender Management**: Support for seeding and ingesting lender PDF guidelines.
- **Matching Algorithm**: Returns eligible lenders with reasoning for rejections.
- **Modern UI**: React + Tailwind + Vite.

## Architecture

Reference Production-Grade Structure:

```text
backend/app/
├── api/            # Routes (v1/endpoints)
├── core/           # Configs
├── db/             # Session & Migrations
├── models/         # SQLAlchemy Models
├── schemas/        # Pydantic Schemas
├── services/       # Business Logic (Matching Engine)
└── main.py         # App Entry
```

- **Backend**: FastAPI (Python)
- **Database**: SQLite (Local) / PostgreSQL (Production ready)
- **Frontend**: React (TypeScript)

## Setup Instructions

### Prerequisites

- Python 3.10+
- Node.js 18+
- Docker & Docker Compose (for PostgreSQL)
- `pdftotext` (optional, for PDF ingestion)

### 1. Backend Setup

1.  **Configure Environment**:
    Create a `.env` file in `backend/.env`:

    ```env
    DATABASE_URL=postgresql://postgres:postgres@localhost:5433/lender_app
    ```

    _(Port 5433 is used to avoid conflicts with local Postgres)_

2.  **Start Database**:

    ```bash
    # From project root
    docker compose up -d
    ```

3.  **Install & Run**:

    ```bash
    cd backend
    # Recommended: Create Virtual Env
    python -m venv venv
    source venv/bin/activate

    # Install Deps
    pip install -r requirements.txt
    pip install psycopg2-binary python-dotenv

    # Build Schema & Seed
    python -m seed

    # Start API
    uvicorn app.main:app --reload
    ```

API will be running at `http://localhost:8000`. Docs at `/docs`.

### 2. Frontend Setup

```bash
cd frontend
# Install dependencies
npm install

# Run the Development Server
npm run dev
```

Frontend will be running at `http://localhost:5173`.

## Usage

1. Open the Frontend.
2. Click "New Application".
3. Fill in the business details (try FICO 600 vs 720 to see different matches).
4. View the "Matching Results" to see which lenders accepted/rejected the deal and why.

## Adding New Lenders

You can ingest a new PDF guideline using the script:

```bash
cd backend
python -m ingest_policy path/to/guidelines.pdf "New Lender Name"
```
