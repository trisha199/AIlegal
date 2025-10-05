from typing import Dict, List
from src.db.client import get_case_details, get_parties, get_financial_rollup, get_medical_total
from src.retrieval.hybrid import retrieve

def build_casefacts(case_id: str) -> Dict:
    case = get_case_details(case_id)
    parties = {
        "plaintiff": [dict(r) for r in get_parties(case_id, "plaintiff")],
        "defendant": [dict(r) for r in get_parties(case_id, "defendant")],
        "insurer": [dict(r) for r in get_parties(case_id, "insurer")],
    }
    med_total = float(get_medical_total(case_id) or 0.0)
    return {
        "case_id": case_id,
        "case": dict(case) if case else {},
        "parties": parties,
        "medical": {"total": med_total},
        "specials_total": med_total
    }

def build_passages(case_id: str) -> Dict[str, List[Dict]]:
    return {
        "liability": retrieve(case_id, "liability facts and fault determination"),
        "injuries": retrieve(case_id, "injuries, diagnoses, treatment, prognosis"),
        "wages": retrieve(case_id, "wage loss and employer verification"),
        "policy": retrieve(case_id, "policy limits, adjuster, insurer correspondence"),
    }
