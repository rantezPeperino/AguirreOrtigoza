# Examen de Ingeniería de Software  
Autores:  
Felipe Aguirre  
Ruben Ortigoza  

# 1. Descripción General
API pública para la gestión de pagos en línea.  
Permite registrar, actualizar, pagar y revertir transacciones.  
Aplica validaciones específicas según el método de pago mediante el patrón Strategy.  
El sistema almacena pagos en archivos JSON y soporta los estados: REGISTRADO, PAGADO y FALLIDO.  
Incluye pruebas automatizadas para validar todo el flujo.

------------------------------------------------------------

Se aplico el patrón Strategy, permitiendo separar las reglas de validación según el método de pago (tarjeta, etc)
Evitamos sobrecargar de condicionales los endpoints.  
Facilitando agregar nuevos métodos de pago sin modificar el código. 


# 2. Estructura del Proyecto

A continuación se muestra el árbol de carpetas en texto plano:

AguirreOrtigoza/  
├── app/  
│   ├── main.py  
│   ├── validators.py  
│   └── __init__.py  
├── payments/        (se generan los archivos .json de pagos)  
├── test/  
│   ├── test_root.py  
│   ├── test_pay.py  
│   └── __init__.py  
├── requirements.txt  
└── README.md  

------------------------------------------------------------

# 3. Instalación y Ejecución Local

## Clonar el repositorio
git clone https://github.com/rantezPeperino/AguirreOrtigoza  
cd AguirreOrtigoza

## Instalar dependencias
pip install -r requirements.txt

## Ejecutar la API
fastapi dev app/main.py

La API queda disponible en:
http://127.0.0.1:8000

------------------------------------------------------------

# 4. Ejecución de Tests

## Ejecutar todos los tests (Linux)
python3 -m unittest discover -s test -p "test_*.py"

## Ejecutar todos los tests (Windows)
python -m unittest discover -s test -p "test_*.py"

## Ejecutar tests individuales
python3 -m unittest test/test_root.py  
python3 -m unittest test/test_pay.py  

------------------------------------------------------------

# 5. Endpoints Locales

## Registrar un pago
POST http://localhost:8000/payments/123?amount=4000&payment_method=tarjeta

## Listar todos los pagos
GET http://localhost:8000/payments

## Pagar un pago existente
POST http://localhost:8000/payments/123/pay

## Revertir un pago
POST http://localhost:8000/payments/123/revert

## Actualizar un pago
POST http://localhost:8000/payments/124/update?amount=99&payment_method=tarjeta

------------------------------------------------------------

# 6. Endpoints Remotos (Render)

Cambiar localhost por la URL del despliegue:

https://aguirreortigoza.onrender.com

## Registrar pago
POST https://aguirreortigoza.onrender.com/payments/123?amount=4000&payment_method=tarjeta

## Listar
GET https://aguirreortigoza.onrender.com/payments

## Pagar
POST https://aguirreortigoza.onrender.com/payments/123/pay

## Revertir
POST https://aguirreortigoza.onrender.com/payments/123/revert

## Actualizar
POST https://aguirreortigoza.onrender.com/payments/124/update?amount=99&payment_method=tarjeta

------------------------------------------------------------

# 7. Hoja de Ruta del Proyecto

1. División del equipo en dos roles principales: Desarrollo y DevOps.  
2. Implementación del pipeline CI/CD mediante GitHub + Render para despliegue automático.  
3. Análisis funcional y técnico de la API.  
4. Diseño de las pruebas automatizadas en función de los casos de uso.  
5. Implementación del patrón Strategy para las validaciones por método de pago.  

------------------------------------------------------------

# 8. Patrones y Buenas Prácticas

## Strategy Pattern
Permite cambiar la lógica de validación según el método de pago:

- Tarjeta: monto máximo 10000 y máximo dos pagos en estado REGISTRADO.  
- PayPal: monto máximo 5000.  
- Estrategia genérica: todo válido si no existe método específico.

Uso en el código:
PaymentValidatorFactory -> devuelve el validador adecuado.

------------------------------------------------------------

# 9. Notas Adicionales

Los archivos JSON se generan automáticamente en la carpeta:

./payments/

Cada archivo corresponde a una transacción independiente, identificada por payment_id.

------------------------------------------------------------

Fin del documento.
