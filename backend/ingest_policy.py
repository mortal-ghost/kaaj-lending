import sys
import subprocess
import re
from app.db.session import SessionLocal
from app.models import sql as models

def extract_text(pdf_path):
    # Use pdftotext (system utility)
    try:
        result = subprocess.run(['pdftotext', pdf_path, '-'], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        print(f"Error running pdftotext: {e}")
        return ""

def parse_policy(text):
    rules = {}
    
    # Heuristic Regex Parsing
    
    # FICO
    fico_match = re.search(r'FICO.*?(\d{3})', text, re.IGNORECASE)
    if fico_match:
        rules['min_fico'] = int(fico_match.group(1))
        
    # Time in Business
    # matches "2 years", "3 years" etc
    tib_match = re.search(r'(\d+)\+?\s*years?.*?business', text, re.IGNORECASE)
    if tib_match:
        rules['min_tib_years'] = int(tib_match.group(1))
        
    # Max Amount
    # matches "$75,000", "$500,000"
    amount_match = re.search(r'\$(\d{1,3}(,\d{3})*)', text)
    if amount_match:
        # replace comma
        rules['max_amount'] = int(amount_match.group(1).replace(',', ''))
        
    return rules

def ingest(pdf_path, lender_name):
    print(f"Ingesting {pdf_path} for {lender_name}...")
    text = extract_text(pdf_path)
    if not text:
        print("No text extracted.")
        return

    rules = parse_policy(text)
    print("Extracted Rules:", rules)
    
    db = SessionLocal()
    
    # Find or Create Lender
    slug = lender_name.lower().replace(" ", "_")
    lender = db.query(models.Lender).filter(models.Lender.slug == slug).first()
    if not lender:
        lender = models.Lender(name=lender_name, slug=slug, type="Genereated")
        db.add(lender)
        db.commit()
        db.refresh(lender)
        
    # Create Policy
    policy = models.Policy(name=f"Ingested from {pdf_path}", lender_id=lender.id, rules=rules)
    db.add(policy)
    db.commit()
    print("Policy saved to database.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python -m backend.ingest_policy <pdf_path> <lender_name>")
    else:
        ingest(sys.argv[1], sys.argv[2])
