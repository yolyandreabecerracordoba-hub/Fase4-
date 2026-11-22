"""Clase Reserva: integra cliente, servicio, duración y estado."""
from entidades import Entidad
from excepciones import (OperacionNoPermitidaError, ParametroFaltanteError, ReservaError,
                         ServicioInvalidoError, ServicioNoDisponibleError, SoftwareFJError)
from logger import log

PENDIENTE, CONFIRMADA, CANCELADA, FALLIDA = "PENDIENTE", "CONFIRMADA", "CANCELADA", "FALLIDA"


class Reserva(Entidad):
    def __init__(self, cliente=None, servicio=None, duracion=None) -> None:
        super().__init__()
        if cliente is None or servicio is None or duracion is None:
            log.error("Reserva rechazada: faltan parámetros.")
            raise ParametroFaltanteError("Cliente, servicio y duración son obligatorios.")
        self._cliente, self._servicio, self._duracion = cliente, servicio, duracion
        self._estado = PENDIENTE
        self._costo = None

    @property
    def estado(self) -> str:
        return self._estado

    @property
    def costo(self):
        return self._costo

    def confirmar(self, impuesto: float = 0.19) -> float:
        """Confirma la reserva: valida, calcula costo y cambia el estado."""
        try:
            if self._estado != PENDIENTE:
                raise OperacionNoPermitidaError(f"No se puede confirmar una reserva {self._estado}.")
            if not self._servicio.disponible:
                raise ServicioNoDisponibleError(f"'{self._servicio.nombre}' no está disponible.")
            self._costo = self._servicio.calcular_costo(self._duracion, impuesto=impuesto)
        except SoftwareFJError as e:
            self._estado = FALLIDA if self._estado == PENDIENTE else self._estado
            log.error("Reserva #%s no confirmada: %s", self.id, e)
            raise
        else:
            self._estado = CONFIRMADA
            log.info("Reserva #%s CONFIRMADA. Costo: $%s", self.id, f"{self._costo:,.2f}")
            return self._costo
        finally:
            log.info("Reserva #%s -> estado final del intento: %s", self.id, self._estado)

    def cancelar(self) -> None:
        if self._estado in (CANCELADA, FALLIDA):
            raise OperacionNoPermitidaError(f"La reserva #{self.id} ya está {self._estado}.")
        self._estado = CANCELADA
        log.info("Reserva #%s CANCELADA.", self.id)

    def procesar(self) -> str:
        """Procesa la reserva encadenando excepciones técnicas en un ReservaError."""
        try:
            costo = self.confirmar()
        except ServicioInvalidoError as e:
            raise ReservaError(f"No se pudo procesar la reserva #{self.id}") from e  # encadenamiento
        except SoftwareFJError as e:
            raise ReservaError(f"Fallo en la reserva #{self.id}: {e}") from e
        return f"Reserva #{self.id} procesada. Total: ${costo:,.2f}"

    def describir(self) -> str:
        return (f"Reserva #{self.id} | {self._cliente.nombre} | {self._servicio.nombre} | "
                f"{self._duracion}h | {self._estado}")
