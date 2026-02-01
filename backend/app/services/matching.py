from typing import List, Dict, Any
from app.models import sql as models
from app.schemas import pydantic_models as schemas

# Rule Strategy Handlers

def check_min_fico(app, value):
    if app.fico_score < value:
        return False, f"FICO Score {app.fico_score} is below minimum {value}"
    return True, None

def check_min_tib_years(app, value):
    if app.years_in_business < value:
        return False, f"Time in Business {app.years_in_business} years is below minimum {value}"
    return True, None

def check_min_revenue(app, value):
    if app.annual_revenue < value:
        return False, f"Annual Revenue ${app.annual_revenue} is below minimum ${value}"
    return True, None

def check_max_amount(app, value):
    if app.amount_requested > value:
        return False, f"Requested Amount ${app.amount_requested} exceeds maximum ${value}"
    return True, None

def check_min_amount(app, value):
    if app.amount_requested < value:
        return False, f"Requested Amount ${app.amount_requested} is below minimum ${value}"
    return True, None

def check_excluded_states(app, value):
    if app.state in value:
        return False, f"State {app.state} is in excluded list"
    return True, None

def check_allowed_equipment_types(app, value):
    # Case-insensitive comparison
    allowed = [t.lower() for t in value]
    if app.equipment_type.lower() not in allowed:
        return False, f"Equipment Type {app.equipment_type} is not in allowed list"
    return True, None

def check_excluded_equipment_types(app, value):
    # Case-insensitive comparison
    excluded = [t.lower() for t in value]
    if app.equipment_type.lower() in excluded:
        return False, f"Equipment Type {app.equipment_type} is excluded"
    return True, None

def check_excluded_industries(app, value):
    # This assumes 'equipment_type' maps loosely to industry for now, 
    # or we would need an 'industry' field in Application.
    # Placeholder implementation
    return True, None 

def check_min_paynet(app, value):
    if app.paynet_score is None:
        # Policy requires paynet but app doesn't have it -> Reject or specialized handling
        return False, "PayNet score is required but missing"
    if app.paynet_score < value:
        return False, f"PayNet Score {app.paynet_score} is below minimum {value}"
    return True, None

# Registry
RULE_HANDLERS = {
    "min_fico": check_min_fico,
    "min_tib_years": check_min_tib_years,
    "min_revenue": check_min_revenue,
    "max_amount": check_max_amount,
    "min_amount": check_min_amount,
    "excluded_states": check_excluded_states,
    "allowed_equipment_types": check_allowed_equipment_types,
    "excluded_equipment_types": check_excluded_equipment_types,
    "excluded_industries": check_excluded_industries,
    "min_paynet": check_min_paynet
}

class RuleEvaluator:
    @staticmethod
    def evaluate(application: models.Application, rules: Dict[str, Any]) -> (bool, List[str]):
        """
        Evaluates an application against a set of rules using the registry.
        Returns: (is_eligible: bool, reasons: List[str])
        """
        reasons = []
        is_eligible = True

        for rule_key, rule_value in rules.items():
            handler = RULE_HANDLERS.get(rule_key)
            if handler:
                passed, reason = handler(application, rule_value)
                if not passed:
                    is_eligible = False
                    reasons.append(reason)
            # If a rule key is in the DB but not in our handlers, we ignore it (or could log a warning)
        
        return is_eligible, reasons

def match_application(application: models.Application, policies: List[models.Policy]) -> List[schemas.MatchResult]:
    results = []
    
    for policy in policies:
        eligible, reasons = RuleEvaluator.evaluate(application, policy.rules)
        
        # Simple scoring logic: 100 if eligible, else 0
        # In a real system, we might score based on how much they exceed the minimums
        score = 100.0 if eligible else 0.0
        
        results.append(schemas.MatchResult(
            lender_name=policy.lender.name,
            policy_name=policy.name,
            eligible=eligible,
            reasons=reasons,
            score=score
        ))
    
    # Sort by score descending
    results.sort(key=lambda x: x.score, reverse=True)
    return results
