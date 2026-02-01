from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.api_v1 import api_router
from app.db.session import engine
from app.models import sql as models

# Create tables (In production use Alembic!)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Lender Matching API")

# CORS (Allow Frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, set to specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Lender Matching Platform API (Production Structure)"}
