# Software FJ – Sistema integral de clientes, servicios y reservas

POO en Python sin base de datos. Ejecutar: `python main.py` (Python 3.8+). Los errores y eventos quedan en `logs/software_fj.log`.

| Archivo | Contenido |
|---|---|
| `entidades.py` | Clase abstracta `Entidad` |
| `cliente.py` | `Cliente` (encapsulación y validaciones) |
| `servicios.py` | `Servicio` (abstracta) + `ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada` |
| `reserva.py` | `Reserva` (confirmar, cancelar, procesar) |
| `excepciones.py` | Excepciones personalizadas |
| `logger.py` | Configuración del log |
| `main.py` | Simulación de 15 operaciones válidas e inválidas |
