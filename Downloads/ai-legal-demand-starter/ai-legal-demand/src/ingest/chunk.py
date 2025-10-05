from typing import List, Dict

def clean_text(s: str) -> str:
    return s.replace('\u00ad','').replace('-\n','').replace('\n',' ').strip()

def make_chunks(text: str, source: str, case_id: str, doc_type: str, page: int | None = None) -> List[Dict]:
    if not text:
        return []
    return [{
        "id": f"{source}-p{page or 0}",
        "text": text,
        "meta": {"case_id": case_id, "source": source, "page": page or 0, "doc_type": doc_type},
    }]
