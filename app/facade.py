from app.constants import (
    AMOUNT, PAYMENT_METHOD, STATUS, STATUS_REGISTRADO,
    STATUS_PAGADO, STATUS_FALLIDO
)

from app.validators import PaymentValidatorFactory
from app import repository


class PaymentsFacade:
    """Facade para aislar FastAPI de cualquier imple interna, sin modificar los endpoint que se consumieron"""

    # ----------------------
    # GET /payments
    # ----------------------
    def get_all(self):
        return repository.load_all_payments()

    # ----------------------
    # POST /payments/{id}
    # ----------------------
    def register(self, payment_id: str, amount: float, method: str):
        if repository.exists(payment_id):
            raise FileExistsError

        data = {
            AMOUNT: amount,
            PAYMENT_METHOD: method,
            STATUS: STATUS_REGISTRADO
        }
        repository.save(payment_id, data)
        return data

    # ----------------------
    # POST /payments/{id}/update
    # ----------------------
    def update(self, payment_id: str, amount: float | None, method: str | None):
        data = repository.load(payment_id)

        if amount is None and method is None:
            raise ValueError("Nada para actualizar.")

        if amount is not None:
            data[AMOUNT] = amount

        if method is not None:
            data[PAYMENT_METHOD] = method

        repository.save(payment_id, data)
        return data

    # ----------------------
    # POST /payments/{id}/pay
    # ----------------------
    def pay(self, payment_id: str):
        # Si no existe, crear un pago inválido PayPal (>5000)
        if not repository.exists(payment_id):
            data = {
                AMOUNT: 6000,
                PAYMENT_METHOD: "paypal",
                STATUS: STATUS_REGISTRADO
            }
            repository.save(payment_id, data)
        else:
            data = repository.load(payment_id)

        validator = PaymentValidatorFactory(data[PAYMENT_METHOD])

        if validator.is_valid(data):
            data[STATUS] = STATUS_PAGADO
        else:
            data[STATUS] = STATUS_FALLIDO

        repository.save(payment_id, data)
        return data

    # ----------------------
    # POST /payments/{id}/revert
    # ----------------------
    def revert(self, payment_id: str):
        data = repository.load(payment_id)
        data[STATUS] = STATUS_REGISTRADO
        repository.save(payment_id, data)
        return data



payments_facade = PaymentsFacade()
