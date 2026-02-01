from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.api import deps
from app import crud
from app.schemas import pydantic_models as schemas
from app.services import matching

router = APIRouter()

@router.post("/", response_model=schemas.Application)
def create_application(application: schemas.ApplicationCreate, db: Session = Depends(deps.get_db)):
    return crud.create_application(db=db, application=application)

@router.get("/{application_id}", response_model=schemas.Application)
def read_application(application_id: int, db: Session = Depends(deps.get_db)):
    db_app = crud.get_application(db, application_id=application_id)
    if db_app is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return db_app

@router.get("/{application_id}/matches", response_model=List[schemas.MatchResult])
def get_matches(application_id: int, db: Session = Depends(deps.get_db)):
    db_app = crud.get_application(db, application_id=application_id)
    if db_app is None:
        raise HTTPException(status_code=404, detail="Application not found")
    
    # Fetch all policies
    lenders = crud.get_lenders(db, limit=100)
    all_policies = []
    for lender in lenders:
        all_policies.extend(lender.policies)
        
    return matching.match_application(db_app, all_policies)
