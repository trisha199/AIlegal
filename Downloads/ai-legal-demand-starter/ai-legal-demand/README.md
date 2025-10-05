# AI Legal Demand — Starter Skeleton
Quick-start scaffold for the Legal AI Demand Letter challenge.

## Run
```bash
python -m src.app bootstrap-db
python -m src.app ingest --case 2024-PI-001 --docs ./data/sample_docs/2024-PI-001
python -m src.app generate --case 2024-PI-001 --out ./output
```
