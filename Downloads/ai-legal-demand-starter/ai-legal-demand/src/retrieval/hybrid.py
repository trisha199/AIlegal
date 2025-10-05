from typing import List, Dict
from src.vector.store import store

def retrieve(case_id: str, question: str, k: int = 8) -> List[Dict]:
    return store.query(case_id, question, k=k)
