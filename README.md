# Examen de Ingeniería de Software  
Autores:  
Felipe Aguirre  
Ruben Ortigoza  


# Aclaracion.
## Los cambios que se realizaron, se pensaron para utilizar los test que se realizaron el dia del examen.
## Los test son los mismos. No se agrego nada, no se modificaron, ni se borraron lineas.
## Los test se pensaron solamente desde el lado del cliente que consume los end point.


# 1. Descripción General
API pública para la gestión de pagos en línea.  
Permite registrar, actualizar, pagar y revertir transacciones.  
Aplica validaciones específicas según el método de pago mediante el patrón Strategy.  
El sistema almacena pagos en archivos JSON y soporta los estados: REGISTRADO, PAGADO y FALLIDO.  
Incluye pruebas automatizadas para validar todo el flujo.


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

# 8. Patrones 
se implementaron esto 3 patrones, 
Para facilitar el agregado de metodos de pago,
Pensando en versiones posteriores que puede cambiar la implementacion del negocio se aplico facade.
Se aplico repository para poder persistir en BD o otro medio sin tener que modificar la persistencia.


## Strategy Pattern
Permite cambiar la lógica de validación según el método de pago:

- Tarjeta: monto máximo 10000 y máximo dos pagos en estado REGISTRADO.  
- PayPal: monto máximo 5000.  
- Estrategia genérica: todo válido si no existe método específico.

Uso en el código:
PaymentValidatorFactory -> devuelve el validador adecuado.

## Facade
Aísla completamente a FastAPI de la lógica de validación, estados y reglas de negocio.<br> 
Permitiendo modificar internamente el sistema sin tocar los endpoints.

## Repository
Permite persistir pagos sin depender de FastAPI ni de la ubicación física de los archivos.<br> 
Habilitando reemplazar el JSON por base de datos real sin modificar la lógica del sistema.

------------------------------------------------------------

# 9. Notas Adicionales

Los archivos JSON se generan automáticamente en la carpeta:

./payments/

Cada archivo corresponde a una transacción independiente, identificada por payment_id.

------------------------------------------------------------

# 10. Diagrama
<a href="www.plantuml.com/plantuml/png/fPBVQnf14CVVzwyOyb1EyiEqZu9jn7h1DaGvHIWKPEfExOQzMzaTfIBvtplUUjUxjDYMvYKpusTcvplVkmkCdhUvLMpO4gHs--H04qnnxU0QKWmyc8xXKg8LQf8WeuqBXftVIp9ZZqphFIpG6erILGfNyW_c57Xe3HKC662eDkZPhCm6fN1n6lkvI78qnSrctxauKb9gSrFSvp8XnCS5_re6TKFQnd-k9gYlanhFsdYziz2xAWurlL2gtnUvQnD4fOydwVVL4AxV7bVjmNGocqDtSrgoUp3w-HtcRblmgrDncHD_Sre9VknAU-3BUUIJYZ3w2cBJ5KIwerHwfBCUq7U1GuFjg0okuwGlpbcbq38ykWYI0lchUWFkgFMAwCF-8HlTZsVpRF1-yjnHP0F19tpHNkbBZQLHkS78Ux6M2gsY5266FNXp-ng6df19moLyc4qUovF9eT3_yLB7h74NoLeownDOX_gt1oZrdBY5F16HsjIq_0xtINNJHTLMMmsc28p5YgeXZTzkJ5YMII8fIdTZcoLQkwoq91r8WhCEg016_qICrOeoJviLYxIr2oVZFMeNNkm2NTcaZAATCJnhvI4myZQ077jmtx3I5F_Kd0uU7iQn-nThRs7oiUbgHZloRFx2M5-I3MzZuJ_iFQ-Y-KMV4N4d6hUv_G40" target="_blank">Ir a Diagrama</a>

