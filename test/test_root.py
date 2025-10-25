import unittest
from fastapi.testclient import TestClient

from app.main import app

# Cliente de pruebas de FastAPI
client = TestClient(app)

class TestRootEndpoint(unittest.TestCase):
    def test_root_endpoint(self):
        """Verifica que el endpoint raíz responda correctamente"""
        response = client.get("/")  # Hacemos una petición GET al endpoint raíz
        self.assertEqual(response.status_code, 200)  # Debe devolver 200 OK

        data = response.json()  # Convertimos la respuesta a JSON
        self.assertIn("mensaje", data)  # Debe contener la clave "mensaje"
        self.assertIn("/files", data["mensaje"])  # El texto debe mencionar /files
        self.assertIn("/files/{filename}", data["mensaje"])  # Y /files/{filename}

if __name__ == "__main__":
    unittest.main()
