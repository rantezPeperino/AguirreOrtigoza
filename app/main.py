import json
from pathlib import Path
from fastapi import FastAPI, HTTPException, Query, status

STATUS = "status"
AMOUNT = "amount"
PAYMENT_METHOD = "payment_method"
STATUS_REGISTRADO = "REGISTRADO"
STATUS_FALLIDO = "FALLIDO"
STATUS_PAGADO = "PAGADO"

PAYMENTS_DIR = Path("../payments/")
PAYMENTS_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI()

def _file(payment_id: str) -> Path:
    return PAYMENTS_DIR / f"{payment_id}.json"

def load_all_payments():
    out = {}
    for p in PAYMENTS_DIR.glob("*.json"):
        try:
            out[p.stem] = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
    return out

def load_payment(payment_id: str):
    f = _file(payment_id)
    if not f.exists():
        raise KeyError
    return json.loads(f.read_text(encoding="utf-8"))

def save_payment_data(payment_id: str, data: dict):
    _file(payment_id).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

def request_is_valid(data: dict) -> bool:
    if data[PAYMENT_METHOD] == "tarjeta":
        if data[AMOUNT] > 10000:
            return False
        for p in load_all_payments().values():
           if p[PAYMENT_METHOD] == "tarjeta" and p[STATUS] == STATUS_REGISTRADO:
               return False
    if data[PAYMENT_METHOD] == "paypal":
        if data[AMOUNT] > 5000:
            return False
    return True

@app.get("/payments")
async def get_all():
    return load_all_payments()

@app.post("/payments/{payment_id}", status_code=status.HTTP_201_CREATED)
async def register(payment_id: str, amount: float, payment_method: str):
    if _file(payment_id).exists():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El pago ya existe.")
    save_payment_data(payment_id, {
        AMOUNT: amount,
        PAYMENT_METHOD: payment_method,
        STATUS: STATUS_REGISTRADO,
    })
    return {"payment_id": payment_id, "data": load_payment(payment_id)}

@app.post("/payments/{payment_id}/update")
async def update(payment_id: str, amount: float | None, payment_method: str | None):
    try:
        data = load_payment(payment_id)
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No existe.")
    if amount is None and payment_method is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nada para actualizar.")
    if amount is not None:
        data[AMOUNT] = amount
    if payment_method is not None:
        data[PAYMENT_METHOD] = payment_method
    save_payment_data(payment_id, data)
    return {"payment_id": payment_id, "data": data}

@app.post("/payments/{payment_id}/pay")
async def pay(payment_id: str):
    try:
        data = load_payment(payment_id)
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No existe.")
    if request_is_valid(data):
        data[STATUS] = STATUS_PAGADO
    else:
        data[STATUS] = STATUS_FALLIDO
    save_payment_data(payment_id, data)
    return {"payment_id": payment_id, "data": data}

@app.post("/payments/{payment_id}/revert")
async def revert(payment_id: str):
    try:
        data = load_payment(payment_id)
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No existe.")
    data[STATUS] = STATUS_REGISTRADO
    save_payment_data(payment_id, data)
    return {"payment_id": payment_id, "data": data}
