# Examen Ingeniería de Software
Alumnos:<br>
Felipe Aguirre<br>
Ruben Ortigoza

#Contenido<br>
API pública para la gestión de pagos en línea que permite registrar, pagar, actualizar y revertir transacciones, con validaciones específicas según el método de pago (tarjeta o PayPal).
Soporta distintos estados del flujo de pago (REGISTRADO, PAGADO, FALLIDO) y endpoints para pruebas integrales.


## Ejecución del proyecto de Forma Local

Clonar el repositorio
```bash
https://github.com/rantezPeperino/AguirreOrtigoza
cd AguirreOrtigoza

Instalar dependencias
pip install -r requirements.txt



Para ejecutar el proyecto desde la raíz:

```bash
fastapi dev app/main.py

##Ejecutar el test

##Linux
python3 -m unittest discover -s test -p "test_*.py"

##Windows
python -m unittest discover -s test -p "test_*.py"


Las urls para hacer test
http://127.0.0.1:8000




#  Registrar pago

POST http://localhost:8000/payments/123?amount=4000&payment_method=tarjeta


#  Listar todos

GET http://localhost:8000/payments


#  Pagar

POST http://localhost:8000/payments/123/pay


#  Revertir

POST http://localhost:8000/payments/123/revert


#  Actualizar

POST http://localhost:8000/payments/124/update?amount=99&payment_method=tarjeta




############
En forma remota se debe cambiar http://localhost:8000 https://aguirreortigoza.onrender.com


# Registrar pago

POST https://aguirreortigoza.onrender.com/payments/123?amount=4000&payment_method=tarjeta

bash
Copiar código

# Listar todos

GET https://aguirreortigoza.onrender.com/payments

bash
Copiar código

# Pagar
POST https://aguirreortigoza.onrender.com/payments/123/pay

bash
Copiar código

# Revertir
POST https://aguirreortigoza.onrender.com/payments/123/revert

bash
Copiar código

# Actualizar
POST https://aguirreortigoza.onrender.com/payments/124/update?amount=99&payment_method=tarjeta


Hoja de Ruta
Se dividio el equipo en 2 uno Devops y otro como Tlbr>
Se realizo el pipeline CI/CD en github con Render, con del deploy incluidobr>
Se realizo el analisis de los endpoint para generar los test necesarios.br>



