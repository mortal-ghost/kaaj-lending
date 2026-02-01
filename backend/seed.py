from sqlalchemy.orm import Session
from app.db.session import SessionLocal, engine
from app.models import sql as models

# Create tables
models.Base.metadata.create_all(bind=engine)

def seed_data():
    db = SessionLocal()
    
    # helper to get or create
    def create_lender_policy(name, slug, l_type, policy_name, rules):
        lender = db.query(models.Lender).filter(models.Lender.slug == slug).first()
        if not lender:
            lender = models.Lender(name=name, slug=slug, type=l_type)
            db.add(lender)
            db.commit()
            db.refresh(lender)
        
        # Check if policy exists
        existing_policy = db.query(models.Policy).filter(models.Policy.lender_id == lender.id, models.Policy.name == policy_name).first()
        if not existing_policy:
            policy = models.Policy(name=policy_name, lender_id=lender.id, rules=rules)
            db.add(policy)
            db.commit()
            print(f"Created policy for {name}")

    # 1. Advantage+ Financing
    # Max $75k, FICO 680+
    create_lender_policy(
        "Advantage+ Financing", 
        "advantage_plus", 
        "Lender", 
        "Standard Broker Program", 
        {
            "max_amount": 75000, 
            "min_fico": 680,
            "min_tib_years": 2, # Assumed from context of "Start-Ups" needing more
            "excluded_states": []
        }
    )

    # 2. Apex Commercial Capital
    # Tier A: 5 years TIB, 700+ FICO
    create_lender_policy(
        "Apex Commercial Capital", 
        "apex", 
        "Lender", 
        "Tier A", 
        {
            "min_amount": 10000,
            "max_amount": 500000,
            "min_tib_years": 5,
            "min_fico": 700,
            "excluded_equipment_types": ["Trucking", "Cannabis"],
            "excluded_states": ["CA", "NV", "ND", "VT"]
        }
    )
    # Tier B: 3 years TIB, 670+ FICO
    create_lender_policy(
        "Apex Commercial Capital", 
        "apex", 
        "Lender", 
        "Tier B", 
        {
            "min_amount": 10000,
            "max_amount": 250000,
            "min_tib_years": 3,
            "min_fico": 670,
            "excluded_states": ["CA", "NV", "ND", "VT"]
        }
    )

    # 3. Stearns Bank (Credit Box)
    # Tier 1: FICO 725, TIB 3
    create_lender_policy(
        "Stearns Bank", 
        "stearns", 
        "Bank", 
        "Tier 1", 
        {
            "min_fico": 725,
            "min_tib_years": 3,
            "min_paynet": 685,
            "excluded_industries": ["Gaming", "Oil & Gas"]
        }
    )
    
    print("Seeding complete.")
    db.close()

if __name__ == "__main__":
    seed_data()
