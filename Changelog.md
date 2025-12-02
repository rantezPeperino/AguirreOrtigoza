# Changelog
Todas las modificaciones relevantes de este proyecto serán documentadas aquí.
---

## [1.2] 
### Added
- Se incorporó el **Patrón Strategy** para validar pagos según método:
  - `TarjetaValidator` con reglas:
    - Monto ≤ 10000
    - Máximo 2 pagos REGISTRADOS en simultáneo
  - `PayPalValidator` con regla:
    - Monto ≤ 5000
  - `PaymentValidatorFactory` para obtener estrategia según `payment_method`.
- Implementación del **Patrón Facade** (`PaymentsFacade`) para desacoplar FastAPI de:
  - Persistencia
  - Validaciones
  - Reglas internas del dominio
- Implementación del **Patrón Repository** para manejar operaciones de almacenamiento:
  - `repository.save()`
  - `repository.load()`
  - `repository.load_all_payments()`
  - `repository.exists()`
- Persistencia mediante archivos JSON individuales (`payments/<id>.json`).

### Changed
- `PaymentsFacade.pay()` ahora delega la validación al Strategy adecuado.
- Ajustes en tests para validar reglas por método de pago.
- Endpoints ahora utilizan la fachada en lugar de llamar directamente a funciones internas.
- Simplificación de `main.py`: solo actúa como adaptador HTTP → dominio.
- Removida lógica de persistencia desde `main.py`, movida íntegramente al repositorio.
- Estructura del proyecto reorganizada para permitir cambiar la fuente de datos en el futuro (BD real, nube, etc.).


---

## [1.1]
### Fixed
- Corrección en los tests iniciales:
  - Ajuste en ruta de archivos
  - Reseteo del directorio `payments/` entre tests

---

## [1.0.0] 
### Added
- Endpoints:
  - `GET /payments`  
  - `POST /payments/{id}`
  - `POST /payments/{id}/update`
  - `POST /payments/{id}/pay`
  - `POST /payments/{id}/revert`
  - `GET /`
- Persistencia básica en archivos JSON sin estructura de repositorio.
- Tests iniciales para endpoints básicos.

---
