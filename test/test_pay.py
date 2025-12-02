import shutil
import unittest
from fastapi.testclient import TestClient
import sys; sys.path.append("..")
from app.main import app, STATUS_PAGADO, STATUS_REGISTRADO, STATUS, STATUS_FALLIDO, PAYMENTS_DIR
from pathlib import Path
BASE_DIR = Path(__file__).parent 
print(BASE_DIR)

client = TestClient(app)

class TestPaymentsSuccess(unittest.TestCase):

    def test_00_setUp(self):
        # Reinicia la carpeta de pagos antes de cada test
        if PAYMENTS_DIR.exists():
            shutil.rmtree(PAYMENTS_DIR)
        PAYMENTS_DIR.mkdir(parents=True, exist_ok=True)

    # ----------------------------------------
    # GET /payments
    # ----------------------------------------
    def test_01_register_new_payment(self):
        """Debe crear un pago nuevo con estado REGISTRADO"""
        r = client.post(
            "/payments/test1",
            params={"amount": 4000, "payment_method": "paypal"},
        )
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json()["data"][STATUS], STATUS_REGISTRADO)

        r = client.post(
            "/payments/test2",
            params={"amount": 9000, "payment_method": "tarjeta"},
        )
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json()["data"][STATUS], STATUS_REGISTRADO)


    # ----------------------------------------
    # POST /payments/{payment_id}
    # ----------------------------------------
    def test_register_new_payment(self):
        """Debe crear un pago nuevo con estado REGISTRADO"""
        r = client.post("/payments/abc123?amount=2000&payment_method=tarjeta")

        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json()["data"][STATUS], STATUS_REGISTRADO)

    # ----------------------------------------
    # POST /payments/{payment_id}/update
    # ----------------------------------------
    def test_02_update_payment_amount(self):
        """Debe actualizar el monto del pago"""
        r = client.post(
            "/payments/test1/update",
            params={"amount": 3000, "payment_method": "paypal"},
        )
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["data"]["amount"], 3000)

    # ----------------------------------------
    # POST /payments/{payment_id}/pay
    # ----------------------------------------

    def test_03_pay_valid_paypal(self):
        """Debe marcar como PAGADO porque PayPal <=5000"""
        r = client.post("/payments/test1/pay")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["data"][STATUS], STATUS_PAGADO)

    def test_04_pay_valid_tarjeta(self):
        """Debe marcar como PAGADO porque el monto es <=10000"""
        r = client.post("/payments/test2/pay")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["data"][STATUS], STATUS_PAGADO)

    def test_05_invalid_paypal_over_limit(self):
        """Debe marcar como FALLIDO porque PayPal >5000"""
        r = client.post("/payments/test3/pay")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["data"][STATUS], STATUS_FALLIDO)

    def test_06_invalid_tarjeta_over_limit(self):
        """Debe marcar como FALLIDO porque el monto es >10000"""
        client.post("/payments/test4", params={"amount": 11000, "payment_method": "tarjeta"})
        r = client.post("/payments/test4/pay")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["data"][STATUS], STATUS_FALLIDO)

    # ----------------------------------------
    # POST /payments/{payment_id}/revert
    # ----------------------------------------
    def test_07_revert_to_registrado(self):
        """Debe revertir el estado a REGISTRADO"""
        r = client.post("/payments/test4/revert")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["data"][STATUS], STATUS_REGISTRADO)

    # ----------------------------------------
    # Caso especial: límite de 2 pagos con tarjeta REGISTRADOS
    # ----------------------------------------
    def test_08_limit_two_tarjeta_registrados(self):
        """Debe permitir solo 2 pagos con tarjeta en estado REGISTRADO"""
        
        # Primer pago con tarjeta (el test4 updateado)
        client.post("/payments/test4/update", params={"amount": 9000, "payment_method": "tarjeta"})

        # Segundo pago con tarjeta
        r = client.post("/payments/test5", params={"amount": 8000, "payment_method": "tarjeta"})
        self.assertEqual(r.status_code, 201)

        # Intento pagar el test4 (debe fallar porque ya hay uno registrado)
        r = client.post("/payments/test4/pay")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["data"][STATUS], STATUS_FALLIDO)

        # Intento pagar el test5 (NO debe fallar porque ya no hay ninguno registrado)
        r = client.post("/payments/test5/pay")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["data"][STATUS], STATUS_PAGADO)

        # Revierto el test4 a REGISTRADO
        r = client.post("/payments/test4/revert")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["data"][STATUS], STATUS_REGISTRADO)

        # Intento pagar el test4 nuevamente (ahora sí debe funcionar)
        r = client.post("/payments/test4/pay")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["data"][STATUS], STATUS_PAGADO)

    # ----------------------------------------
    # GET /payments
    # ----------------------------------------
    def test_09_get_all_after_register(self):
        """Debe listar los pagos después de registrar uno"""
        r = client.get("/payments")
        body = r.json()
        self.assertIn("data", body)
        self.assertTrue(body["data"])

if __name__ == "__main__":
    unittest.main()
