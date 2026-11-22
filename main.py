"""Simulación de 15 operaciones del sistema Software FJ (sin base de datos)."""  # Docstring del módulo
from cliente import Cliente  # Clase Cliente
from excepciones import SoftwareFJError  # Excepción base del sistema
from logger import log, RUTA_LOG  # Logger y ruta del archivo de log
from reserva import Reserva  # Clase Reserva
from servicios import AlquilerEquipo, AsesoriaEspecializada, ReservaSala  # Servicios especializados

clientes, servicios, reservas = [], [], []  # Listas internas que reemplazan a una base de datos


def ejecutar(num: int, titulo: str, accion) -> None:  # Ejecuta una operación sin que un error detenga el programa
    """Ejecuta una operación; cualquier error se registra y el sistema continúa."""  # Docstring de la función
    print(f"\n[{num:02d}] {titulo}")  # Muestra el número y título de la operación
    log.info("--- Operación %s: %s ---", num, titulo)  # Registra el inicio de la operación en el log
    try:  # Intenta ejecutar la operación
        resultado = accion()  # Ejecuta la función recibida
        print("   OK ->", resultado)  # Muestra el resultado si salió bien
    except SoftwareFJError as e:  # Captura los errores propios del sistema
        log.error("Operación %s falló (%s): %s", num, type(e).__name__, e)  # Registra el error en el log
        print(f"   ERROR CONTROLADO -> {type(e).__name__}: {e}")  # Muestra el error en pantalla
        if e.__cause__:  # Si el error tiene una causa encadenada
            print(f"      causa: {type(e.__cause__).__name__}: {e.__cause__}")  # Muestra la causa original
    except Exception as e:  # Captura cualquier error imprevisto
        log.exception("Error inesperado en operación %s", num)  # Registra el error con todo su detalle
        print(f"   ERROR INESPERADO -> {type(e).__name__}: {e}")  # Muestra el error y el programa sigue


def reg_cliente(*args, **kw):  # Crea un cliente y lo guarda en la lista
    c = Cliente(*args, **kw)  # Crea el cliente (puede lanzar errores)
    clientes.append(c)  # Lo agrega a la lista solo si fue válido
    return c  # Devuelve el cliente creado


def reg_servicio(clase, *args, **kw):  # Crea un servicio de la clase indicada y lo guarda
    s = clase(*args, **kw)  # Crea el servicio (puede lanzar errores)
    servicios.append(s)  # Lo agrega a la lista solo si fue válido
    return s  # Devuelve el servicio creado


def nueva_reserva(cliente, servicio, dur):  # Crea una reserva y la guarda en la lista
    r = Reserva(cliente, servicio, dur)  # Crea la reserva (puede lanzar errores)
    reservas.append(r)  # La agrega a la lista solo si fue válida
    return r  # Devuelve la reserva creada


def main() -> None:  # Función principal de la simulación
    log.info("===== INICIO DE SIMULACIÓN =====")  # Marca el inicio en el log
    ejecutar(1, "Cliente válido", lambda: reg_cliente("ana gómez", "ana@correo.com", "3101234567"))  # Registro correcto
    ejecutar(2, "Cliente con email inválido", lambda: reg_cliente("Luis Pérez", "luis#correo", "3109876543"))  # Email mal formado
    ejecutar(3, "Cliente con parámetros faltantes", lambda: reg_cliente("Marta Ruiz"))  # Faltan email y teléfono
    ejecutar(4, "Sala válida", lambda: reg_servicio(ReservaSala, "Sala Innovación", 50000, 12))  # Servicio 1 correcto
    ejecutar(5, "Servicio con tarifa negativa", lambda: reg_servicio(AlquilerEquipo, "Portátiles", -100, "Laptop"))  # Tarifa inválida
    ejecutar(6, "Asesoría senior válida", lambda: reg_servicio(AsesoriaEspecializada, "Asesoría IA", 120000, "IA", "senior"))  # Servicio 2 correcto
    ejecutar(7, "Equipo válido", lambda: reg_servicio(AlquilerEquipo, "Proyector", 15000, "Proyector 4K", 2))  # Servicio 3 correcto
    ejecutar(8, "Reserva exitosa (sala 3h)",  # Reserva correcta
             lambda: nueva_reserva(clientes[0], servicios[0], 3).procesar())  # Crea y procesa la reserva
    ejecutar(9, "Reserva fallida (duración fuera de rango, error encadenado)",  # Reserva incorrecta
             lambda: nueva_reserva(clientes[0], servicios[0], 20).procesar())  # 20 horas excede el máximo de la sala
    ejecutar(10, "Reserva sobre servicio no disponible", lambda: (  # Servicio deshabilitado
        setattr(servicios[2], "disponible", False), nueva_reserva(clientes[0], servicios[2], 5).procesar())[1])  # Deshabilita el equipo y reserva
    ejecutar(11, "Cancelar dos veces la misma reserva", lambda: (  # Operación no permitida
        reservas[0].cancelar(), reservas[0].cancelar())[1])  # La segunda cancelación lanza error
    ejecutar(12, "Costos sobrecargados (impuesto / dict / cupón)", lambda: [  # Demuestra los métodos sobrecargados
        servicios[1].calcular_costo_total(0.19, 2),  # Variante con número (impuesto)
        servicios[1].calcular_costo_total({"impuesto": 0.19, "descuento": 0.1}, 2),  # Variante con diccionario
        servicios[1].calcular_costo_total("FJ20", 2)])  # Variante con cupón
    ejecutar(13, "Reserva sin cliente (parámetro faltante)", lambda: nueva_reserva(None, servicios[0], 2))  # Falta el cliente
    ejecutar(14, "Cupón inexistente", lambda: servicios[1].calcular_costo_total("NOEXISTE", 2))  # Cupón inválido
    ejecutar(15, "Cálculo inconsistente (impuesto del 150 %)",  # Cálculo incoherente
             lambda: servicios[0].calcular_costo(2, impuesto=1.5))  # Impuesto fuera de rango lanza CalculoInconsistenteError

    print("\n=== Resumen final ===")  # Encabezado del resumen
    for e in (*clientes, *servicios, *reservas):  # Recorre todas las entidades creadas
        print(" ", e)  # Imprime la descripción de cada una
    print(f"\nLog de eventos y errores: {RUTA_LOG}")  # Indica dónde quedó el log
    log.info("===== FIN DE SIMULACIÓN =====")  # Marca el fin en el log


if __name__ == "__main__":  # Solo ejecuta main() si se corre este archivo directamente
    main()  # Inicia la simulación
