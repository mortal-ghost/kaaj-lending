from pydantic import BaseModel
from typing import List, Optional, Any, Dict
from datetime import datetime

# --- Policy Schemas ---
class PolicyBase(BaseModel):
    name: str
    rules: Dict[str, Any]

class PolicyCreate(PolicyBase):
    pass

class Policy(PolicyBase):
    id: int
    lender_id: int
    version: int

    class Config:
        from_attributes = True

# --- Lender Schemas ---
class LenderBase(BaseModel):
    name: str
    slug: str
    type: str

class LenderCreate(LenderBase):
    pass

class Lender(LenderBase):
    id: int
    policies: List[Policy] = []

    class Config:
        from_attributes = True

# --- Application Schemas ---
class ApplicationBase(BaseModel):
    business_name: str
    amount_requested: float
    equipment_type: str
    fico_score: int
    years_in_business: float
    annual_revenue: float
    paynet_score: Optional[int] = None
    state: str
    city: str

class ApplicationCreate(ApplicationBase):
    pass

class Application(ApplicationBase):
    id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

# --- Match Result Schemas ---
class MatchResult(BaseModel):
    lender_name: str
    policy_name: str
    eligible: bool
    reasons: List[str]
    score: float
