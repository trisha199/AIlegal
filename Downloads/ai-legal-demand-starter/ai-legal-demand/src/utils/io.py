from pathlib import Path

def ensure_dir(p: str | Path) -> None:
    Path(p).mkdir(parents=True, exist_ok=True)

def out_path(base: str | Path, filename: str) -> str:
    p = Path(base) / filename
    p.parent.mkdir(parents=True, exist_ok=True)
    return str(p)
