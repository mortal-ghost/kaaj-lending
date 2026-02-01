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

- Python 3.9+
- Node.js 18+
- `pdftotext` (optional, for PDF ingestion)

### 1. Backend Setup

```bash
cd backend
# Install dependencies
pip install -r requirements.txt

# Seed the database
python -m seed

# Run the API Server
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
