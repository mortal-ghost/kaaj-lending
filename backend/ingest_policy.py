import sys
from app.db.session import SessionLocal
from app.models import sql as models
from app.services.parser import RegexPolicyParser, AIPolicyParser

def ingest(pdf_path, lender_name, use_ai=False):
    print(f"Ingesting {pdf_path} for {lender_name}...")
    
    # Select Strategy
    if use_ai:
        parser = AIPolicyParser()
    else:
        parser = RegexPolicyParser()
        
    rules = parser.parse(pdf_path)
    print("Extracted Rules:", rules)
    
    db = SessionLocal()
    
    slug = lender_name.lower().replace(" ", "_")
    lender = db.query(models.Lender).filter(models.Lender.slug == slug).first()
    if not lender:
        lender = models.Lender(name=lender_name, slug=slug, type="Genereated")
        db.add(lender)
        db.commit()
        db.refresh(lender)
        
    policy = models.Policy(name=f"Ingested from {pdf_path}", lender_id=lender.id, rules=rules)
    db.add(policy)
    db.commit()
    print("Policy saved to database.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python -m backend.ingest_policy <pdf_path> <lender_name> [--ai]")
    else:
        use_ai = "--ai" in sys.argv
        ingest(sys.argv[1], sys.argv[2], use_ai)
