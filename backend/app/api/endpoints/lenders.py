from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.api import deps
from app import crud
from app.schemas import pydantic_models as schemas

router = APIRouter()

@router.post("/", response_model=schemas.Lender)
def create_lender(lender: schemas.LenderCreate, db: Session = Depends(deps.get_db)):
    return crud.create_lender(db=db, lender=lender)

@router.get("/", response_model=List[schemas.Lender])
def read_lenders(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    return crud.get_lenders(db, skip=skip, limit=limit)

@router.post("/{lender_id}/policies/", response_model=schemas.Policy)
def create_policy_for_lender(
    lender_id: int, policy: schemas.PolicyCreate, db: Session = Depends(deps.get_db)
):
    return crud.create_policy(db=db, policy=policy, lender_id=lender_id)
