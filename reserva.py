"""Clase Reserva: integra cliente, servicio, duración y estado."""  # Docstring del módulo
from entidades import Entidad  # Clase base abstracta
from excepciones import (OperacionNoPermitidaError, ParametroFaltanteError, ReservaError,  # Excepciones propias usadas aquí
                         ServicioInvalidoError, ServicioNoDisponibleError, SoftwareFJError)  # (continuación del import)
from logger import log  # Logger para registrar eventos y errores

PENDIENTE, CONFIRMADA, CANCELADA, FALLIDA = "PENDIENTE", "CONFIRMADA", "CANCELADA", "FALLIDA"  # Estados posibles de una reserva


class Reserva(Entidad):  # Reserva hereda de Entidad
    """Reserva que une un cliente, un servicio y una duración."""  # Docstring de la clase

    def __init__(self, cliente=None, servicio=None, duracion=None) -> None:  # Constructor; None permite detectar faltantes
        super().__init__()  # Asigna el id mediante Entidad
        if cliente is None or servicio is None or duracion is None:  # Verifica que lleguen los tres datos
            log.error("Reserva rechazada: faltan parámetros.")  # Registra el error en el log
            raise ParametroFaltanteError("Cliente, servicio y duración son obligatorios.")  # Lanza el error de dato faltante
        self._cliente, self._servicio, self._duracion = cliente, servicio, duracion  # Guarda los datos de la reserva
        self._estado = PENDIENTE  # Toda reserva nueva empieza pendiente
        self._costo = None  # El costo se calcula al confirmar

    @property  # Getter del estado
    def estado(self) -> str:  # Devuelve el estado actual
        return self._estado  # Retorna el estado

    @property  # Getter del costo
    def costo(self):  # Devuelve el costo calculado (o None)
        return self._costo  # Retorna el costo

    def confirmar(self, impuesto: float = 0.19) -> float:  # Confirma la reserva y devuelve su costo (IVA 19 % por defecto)
        """Confirma la reserva: valida, calcula costo y cambia el estado."""  # Docstring del método
        try:  # Bloque que puede producir errores
            if self._estado != PENDIENTE:  # Solo se confirman reservas pendientes
                raise OperacionNoPermitidaError(f"No se puede confirmar una reserva {self._estado}.")  # Error de operación no permitida
            if not self._servicio.disponible:  # Verifica la disponibilidad del servicio
                raise ServicioNoDisponibleError(f"'{self._servicio.nombre}' no está disponible.")  # Error de servicio no disponible
            self._costo = self._servicio.calcular_costo(self._duracion, impuesto=impuesto)  # Calcula el costo (puede lanzar errores)
        except SoftwareFJError as e:  # Captura cualquier error propio del sistema
            self._estado = FALLIDA if self._estado == PENDIENTE else self._estado  # Marca como fallida si estaba pendiente
            log.error("Reserva #%s no confirmada: %s", self.id, e)  # Registra el error en el log
            raise  # Relanza el error para que lo maneje quien llamó
        else:  # Se ejecuta solo si no hubo errores
            self._estado = CONFIRMADA  # Cambia el estado a confirmada
            log.info("Reserva #%s CONFIRMADA. Costo: $%s", self.id, f"{self._costo:,.2f}")  # Registra el éxito
            return self._costo  # Devuelve el costo calculado
        finally:  # Se ejecuta siempre, haya o no error
            log.info("Reserva #%s -> estado final del intento: %s", self.id, self._estado)  # Deja constancia del estado resultante

    def cancelar(self) -> None:  # Cancela la reserva
        """Cancela la reserva si aún es válido hacerlo."""  # Docstring del método
        if self._estado in (CANCELADA, FALLIDA):  # No se puede cancelar lo ya cancelado o fallido
            raise OperacionNoPermitidaError(f"La reserva #{self.id} ya está {self._estado}.")  # Error de operación no permitida
        self._estado = CANCELADA  # Cambia el estado a cancelada
        log.info("Reserva #%s CANCELADA.", self.id)  # Registra la cancelación

    def procesar(self) -> str:  # Procesa la reserva encadenando excepciones
        """Procesa la reserva encadenando excepciones técnicas en un ReservaError."""  # Docstring del método
        try:  # Intenta confirmar la reserva
            costo = self.confirmar()  # Confirma y obtiene el costo
        except ServicioInvalidoError as e:  # Si el servicio rechazó los parámetros
            raise ReservaError(f"No se pudo procesar la reserva #{self.id}") from e  # Encadena el error original como causa
        except SoftwareFJError as e:  # Cualquier otro error del sistema
            raise ReservaError(f"Fallo en la reserva #{self.id}: {e}") from e  # Encadena el error original como causa
        return f"Reserva #{self.id} procesada. Total: ${costo:,.2f}"  # Mensaje de éxito con el total

    def describir(self) -> str:  # Implementa el método abstracto de Entidad
        return (f"Reserva #{self.id} | {self._cliente.nombre} | {self._servicio.nombre} | "  # Primera parte de la descripción
                f"{self._duracion}h | {self._estado}")  # Duración y estado de la reserva
