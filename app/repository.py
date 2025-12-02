import json
from pathlib import Path

# Carpeta payments SIEMPRE dentro del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent
PAYMENTS_DIR = BASE_DIR / "payments"
PAYMENTS_DIR.mkdir(parents=True, exist_ok=True)

def _file(payment_id: str) -> Path:
    return PAYMENTS_DIR / f"{payment_id}.json"

def exists(payment_id: str) -> bool:
    return _file(payment_id).exists()

def load_all_payments():
    out = {}
    for p in PAYMENTS_DIR.glob("*.json"):
        try:
            out[p.stem] = json.loads(p.read_text(encoding="utf-8"))
        except:
            continue
    return out

def load(payment_id: str) -> dict:
    f = _file(payment_id)
    if not f.exists():
        raise KeyError
    return json.loads(f.read_text(encoding="utf-8"))

def save(payment_id: str, data: dict):
    _file(payment_id).write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
