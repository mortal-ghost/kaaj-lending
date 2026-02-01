from sqlalchemy import Column, Integer, String, JSON, ForeignKey, DateTime, Float, Boolean, Enum
from sqlalchemy.orm import relationship
import enum
from datetime import datetime
from app.db.session import Base

class ApplicationStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class Lender(Base):
    __tablename__ = "lenders"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    slug = Column(String, unique=True, index=True)
    type = Column(String)  # Bank, Non-Bank-FI, Fintech, etc.
    
    policies = relationship("Policy", back_populates="lender")

class Policy(Base):
    __tablename__ = "policies"

    id = Column(Integer, primary_key=True, index=True)
    lender_id = Column(Integer, ForeignKey("lenders.id"))
    name = Column(String) # e.g. "Standard Program", "A-Credit Tier"
    version = Column(Integer, default=1)
    
    # The rules are stored as a JSON blob for flexibility
    # Example: {"min_fico": 650, "max_amount": 500000, "excluded_states": ["CA"]}
    rules = Column(JSON, default={})
    
    lender = relationship("Lender", back_populates="policies")

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    business_name = Column(String, index=True)
    amount_requested = Column(Float)
    equipment_type = Column(String) # e.g. "Truck", "Medical"
    
    # Financials
    fico_score = Column(Integer)
    years_in_business = Column(Float)
    annual_revenue = Column(Float)
    paynet_score = Column(Integer, nullable=True)
    
    # Location
    city = Column(String)
    state = Column(String)
    zip_code = Column(String)

    # Extensibility: Store arbitrary extra fields here (e.g., specific form data, AI-extracted metadata)
    data = Column(JSON, default={})

    status = Column(String, default=ApplicationStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)
