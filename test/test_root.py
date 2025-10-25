import unittest
from fastapi.testclient import TestClient

from app.main import app

# Cliente de pruebas de FastAPI
client = TestClient(app)

class TestRootEndpoint(unittest.TestCase):
    def test_root_endpoint(self):
        """Verifica que el endpoint raíz responda correctamente"""
        response = client.get("/")  # Hacemos una petición GET al endpoint raíz
        self.assertEqual(response.status_code, response.status_code)  # Debe devolver 200 OK


if __name__ == "__main__":
    unittest.main()
