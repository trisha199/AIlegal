import argparse, os
from src.db.bootstrap import bootstrap_db
from src.ingest.pdf_extractor import extract_pdf
from src.ingest.chunk import make_chunks
from src.vector.store import store
from src.generation.compose import build_casefacts, build_passages
from src.generation.writer import generate_text_from_context, write_docx

def cmd_bootstrap_db(args):
    bootstrap_db()

def cmd_ingest(args):
    case_id, docs_dir = args.case, args.docs
    for fname in os.listdir(docs_dir):
        if not fname.lower().endswith(".pdf"):
            continue
        source = fname
        doc_type = ("police_report" if "police" in fname.lower()
                    else "medical" if "medical" in fname.lower()
                    else "financial" if "wage" in fname.lower()
                    else "correspondence" if "insurance" in fname.lower()
                    else "unknown")
        data = extract_pdf(os.path.join(docs_dir, fname))
        chunks = make_chunks(data.get('text',''), source, case_id, doc_type, page=1)
        store.upsert(chunks)
    print("✅ Ingestion complete (stub).")

def cmd_generate(args):
    case_id = args.case
    facts = build_casefacts(case_id)
    passages = build_passages(case_id)
    text = generate_text_from_context(facts, passages)
    path = write_docx(case_id, text, args.out)
    print("✅ Generated:", path)

def main(argv=None):
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)

    p1 = sub.add_parser("bootstrap-db")
    p1.set_defaults(func=cmd_bootstrap_db)

    p2 = sub.add_parser("ingest")
    p2.add_argument("--case", required=True)
    p2.add_argument("--docs", required=True)
    p2.set_defaults(func=cmd_ingest)

    p3 = sub.add_parser("generate")
    p3.add_argument("--case", required=True)
    p3.add_argument("--out", required=True)
    p3.set_defaults(func=cmd_generate)

    args = p.parse_args(argv)
    args.func(args)

if __name__ == "__main__":
    main()
