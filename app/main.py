
# app/main.py
from fastapi import FastAPI, HTTPException, status
from app.constants import (
    AMOUNT, PAYMENT_METHOD, STATUS,
    STATUS_REGISTRADO, STATUS_FALLIDO, STATUS_PAGADO
)
from app.repository import PAYMENTS_DIR
from app.facade import payments_facade



app = FastAPI()

@app.get("/payments")
async def get_all():
    return payments_facade.get_all()



@app.post("/payments/{payment_id}", status_code=status.HTTP_201_CREATED)
async def register(payment_id: str, amount: float, payment_method: str):
    try:
        data = payments_facade.register(payment_id, amount, payment_method)
        return {"payment_id": payment_id, "data": data}
    except FileExistsError:
        raise HTTPException(status_code=409, detail="El pago ya existe.")


@app.post("/payments/{payment_id}/update")
async def update(payment_id: str, amount: float | None, payment_method: str | None):
    try:
        data = payments_facade.update(payment_id, amount, payment_method)
        return {"payment_id": payment_id, "data": data}
    except KeyError:
        raise HTTPException(404, "No existe.")
    except ValueError as e:
        raise HTTPException(400, str(e))


@app.post("/payments/{payment_id}/pay")
async def pay(payment_id: str):
    try:
        data = payments_facade.pay(payment_id)
        return {"payment_id": payment_id, "data": data}
    except KeyError:
        raise HTTPException(404, "No existe.")


@app.post("/payments/{payment_id}/revert")
async def revert(payment_id: str):
    try:
        data = payments_facade.revert(payment_id)
        return {"payment_id": payment_id, "data": data}
    except KeyError:
        raise HTTPException(404, "No existe.")


@app.get("/")
async def root():
    return {"Estamos Arriba"}
