"""Simulación de 12 operaciones del sistema Software FJ (sin base de datos)."""
from cliente import Cliente
from excepciones import SoftwareFJError
from logger import log, RUTA_LOG
from reserva import Reserva
from servicios import AlquilerEquipo, AsesoriaEspecializada, ReservaSala

clientes, servicios, reservas = [], [], []


def ejecutar(num: int, titulo: str, accion) -> None:
    """Ejecuta una operación; cualquier error se registra y el sistema continúa."""
    print(f"\n[{num:02d}] {titulo}")
    log.info("--- Operación %s: %s ---", num, titulo)
    try:
        resultado = accion()
        print("   OK ->", resultado)
    except SoftwareFJError as e:
        log.error("Operación %s falló (%s): %s", num, type(e).__name__, e)
        print(f"   ERROR CONTROLADO -> {type(e).__name__}: {e}")
        if e.__cause__:
            print(f"      causa: {type(e.__cause__).__name__}: {e.__cause__}")
    except Exception as e:  # cualquier error imprevisto tampoco detiene el programa
        log.exception("Error inesperado en operación %s", num)
        print(f"   ERROR INESPERADO -> {type(e).__name__}: {e}")


def reg_cliente(*args, **kw):
    c = Cliente(*args, **kw)
    clientes.append(c)
    return c


def reg_servicio(clase, *args, **kw):
    s = clase(*args, **kw)
    servicios.append(s)
    return s


def nueva_reserva(cliente, servicio, dur):
    r = Reserva(cliente, servicio, dur)
    reservas.append(r)
    return r


def main() -> None:
    log.info("===== INICIO DE SIMULACIÓN =====")
    ejecutar(1, "Cliente válido", lambda: reg_cliente("ana gómez", "ana@correo.com", "3101234567"))
    ejecutar(2, "Cliente con email inválido", lambda: reg_cliente("Luis Pérez", "luis#correo", "3109876543"))
    ejecutar(3, "Cliente con parámetros faltantes", lambda: reg_cliente("Marta Ruiz"))
    ejecutar(4, "Sala válida", lambda: reg_servicio(ReservaSala, "Sala Innovación", 50000, 12))
    ejecutar(5, "Servicio con tarifa negativa", lambda: reg_servicio(AlquilerEquipo, "Portátiles", -100, "Laptop"))
    ejecutar(6, "Asesoría senior válida", lambda: reg_servicio(AsesoriaEspecializada, "Asesoría IA", 120000, "IA", "senior"))
    ejecutar(7, "Equipo válido", lambda: reg_servicio(AlquilerEquipo, "Proyector", 15000, "Proyector 4K", 2))
    ejecutar(8, "Reserva exitosa (sala 3h)",
             lambda: nueva_reserva(clientes[0], servicios[0], 3).procesar())
    ejecutar(9, "Reserva fallida (duración fuera de rango, error encadenado)",
             lambda: nueva_reserva(clientes[0], servicios[0], 20).procesar())
    ejecutar(10, "Reserva sobre servicio no disponible", lambda: (
        setattr(servicios[2], "disponible", False), nueva_reserva(clientes[0], servicios[2], 5).procesar())[1])
    ejecutar(11, "Cancelar dos veces la misma reserva", lambda: (
        reservas[0].cancelar(), reservas[0].cancelar())[1])
    ejecutar(12, "Costos sobrecargados (impuesto / dict / cupón)", lambda: [
        servicios[1].calcular_costo_total(0.19, 2),
        servicios[1].calcular_costo_total({"impuesto": 0.19, "descuento": 0.1}, 2),
        servicios[1].calcular_costo_total("FJ20", 2)])
    ejecutar(14, "Cupón inexistente", lambda: servicios[1].calcular_costo_total("NOEXISTE", 2))
    ejecutar(13, "Reserva sin cliente (parámetro faltante)", lambda: nueva_reserva(None, servicios[0], 2))

    print("\n=== Resumen final ===")
    for e in (*clientes, *servicios, *reservas):
        print(" ", e)
    print(f"\nLog de eventos y errores: {RUTA_LOG}")
    log.info("===== FIN DE SIMULACIÓN =====")


if __name__ == "__main__":
    main()
