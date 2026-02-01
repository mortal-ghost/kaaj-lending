from sqlalchemy.orm import Session
from app.models import sql as models
from app.schemas import pydantic_models as schemas

def get_lender(db: Session, lender_id: int):
    return db.query(models.Lender).filter(models.Lender.id == lender_id).first()

def get_lenders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Lender).offset(skip).limit(limit).all()

def create_lender(db: Session, lender: schemas.LenderCreate):
    db_lender = models.Lender(name=lender.name, slug=lender.slug, type=lender.type)
    db.add(db_lender)
    db.commit()
    db.refresh(db_lender)
    return db_lender

def create_policy(db: Session, policy: schemas.PolicyCreate, lender_id: int):
    db_policy = models.Policy(**policy.dict(), lender_id=lender_id)
    db.add(db_policy)
    db.commit()
    db.refresh(db_policy)
    return db_policy

def create_application(db: Session, application: schemas.ApplicationCreate):
    db_application = models.Application(**application.dict(), status=models.ApplicationStatus.PENDING)
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return db_application

def get_application(db: Session, application_id: int):
    return db.query(models.Application).filter(models.Application.id == application_id).first()

def get_applications(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Application).offset(skip).limit(limit).all()
