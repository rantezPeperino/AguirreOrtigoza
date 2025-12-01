# app/validators.py

from app.main import AMOUNT, PAYMENT_METHOD, STATUS, STATUS_REGISTRADO

class PaymentValidator:
    """Estrategia base (Strategy)."""
    def is_valid(self, data: dict) -> bool:
        return True


class TarjetaValidator(PaymentValidator):
    def is_valid(self, data: dict) -> bool:
        # Regla 1: monto <= 10000
        if data[AMOUNT] > 10000:
            return False

        # Regla 2: máximo 2 pagos REGISTRADOS con tarjeta
        from app.main import load_all_payments  # import local para evitar ciclo

        counter = 0
        for p in load_all_payments().values():
            if p[PAYMENT_METHOD] == "tarjeta" and p[STATUS] == STATUS_REGISTRADO:
                counter += 1

        return counter < 2


class PayPalValidator(PaymentValidator):
    def is_valid(self, data: dict) -> bool:
        # PayPal permite montos <= 5000
        return data[AMOUNT] <= 5000


def PaymentValidatorFactory(method: str) -> PaymentValidator:
    """Devuelve la estrategia correcta según el método."""
    if method == "tarjeta":
        return TarjetaValidator()
    if method == "paypal":
        return PayPalValidator()
    # Si no existe, usa una estrategia genérica (siempre válida)
    return PaymentValidator()
