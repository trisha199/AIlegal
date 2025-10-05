from typing import List, Dict

class VectorStore:
    def __init__(self):
        self.docs: List[Dict] = []

    def upsert(self, chunks: List[Dict]) -> None:
        self.docs.extend(chunks)

    def query(self, case_id: str, q: str, k: int = 8) -> List[Dict]:
        return [d for d in self.docs if d['meta']['case_id']==case_id][:k]

store = VectorStore()
