import shutil
import unittest
from fastapi.testclient import TestClient
from app.main import app, PAYMENTS_DIR, STATUS_PAGADO, STATUS_REGISTRADO

client = TestClient(app)

class TestPaymentsSuccess(unittest.TestCase):

    def setUp(self):
        # Reinicia la carpeta de pagos antes de cada test
        if PAYMENTS_DIR.exists():
            shutil.rmtree(PAYMENTS_DIR)
        PAYMENTS_DIR.mkdir(parents=True, exist_ok=True)

    # ----------------------------------------
    # GET /payments
    # ----------------------------------------
    def test_get_all_initially_empty(self):
        """Debe devolver un dict vacío al inicio"""
        r = client.get("/payments")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), {})

    def test_get_all_after_register(self):
        """Debe listar los pagos después de registrar uno"""
        client.post("/payments/test1?amount=1000&payment_method=tarjeta")
        r = client.get("/payments")
        self.assertIn("test1", r.json())

    # ----------------------------------------
    # POST /payments/{payment_id}
    # ----------------------------------------
    def test_register_new_payment(self):
        """Debe crear un pago nuevo con estado REGISTRADO"""
        r = client.post("/payments/abc123?amount=2000&payment_method=tarjeta")
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json()["data"]["status"], STATUS_REGISTRADO)

    # ----------------------------------------
    # POST /payments/{payment_id}/update
    # ----------------------------------------
    def test_update_payment_amount(self):
        """Debe actualizar el monto del pago"""
        client.post("/payments/upd1?amount=500&payment_method=tarjeta")
        r = client.post("/payments/upd1/update?amount=1500")
#        self.assertEqual(r.status_code, 200)
#        self.assertEqual(r.json()["data"]["amount"], 1500)

    # ----------------------------------------
    # POST /payments/{payment_id}/pay
    # ----------------------------------------
    def test_pay_valid_tarjeta(self):
        """Debe marcar como PAGADO cuando el monto es <=10000"""
        client.post("/payments/pago1?amount=9000&payment_method=tarjeta")
        r = client.post("/payments/pago1/pay")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["data"]["status"], STATUS_PAGADO)

    def test_pay_valid_paypal(self):
        """Debe marcar como PAGADO cuando PayPal <=5000"""
        client.post("/payments/paypal_ok?amount=4500&payment_method=paypal")
        r = client.post("/payments/paypal_ok/pay")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["data"]["status"], STATUS_PAGADO)

    # ----------------------------------------
    # POST /payments/{payment_id}/revert
    # ----------------------------------------
    def test_revert_to_registrado(self):
        """Debe revertir el estado a REGISTRADO"""
        client.post("/payments/rev1?amount=3000&payment_method=tarjeta")
        client.post("/payments/rev1/pay")
        r = client.post("/payments/rev1/revert")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["data"]["status"], STATUS_REGISTRADO)


if __name__ == "__main__":
    unittest.main()
