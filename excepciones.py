"""Excepciones personalizadas del sistema Software FJ."""


class SoftwareFJError(Exception):
    """Excepción base de la que heredan todos los errores del sistema."""


class ParametroFaltanteError(SoftwareFJError):
    """Se omitió un parámetro obligatorio."""


class ClienteInvalidoError(SoftwareFJError):
    """Los datos de un cliente no cumplen las validaciones."""


class ServicioInvalidoError(SoftwareFJError):
    """Los parámetros de un servicio son inválidos."""


class ServicioNoDisponibleError(SoftwareFJError):
    """El servicio solicitado no está disponible."""


class ReservaError(SoftwareFJError):
    """Error general durante la gestión de una reserva."""


class OperacionNoPermitidaError(ReservaError):
    """La operación no es válida para el estado actual de la reserva."""


class CalculoInconsistenteError(SoftwareFJError):
    """Un cálculo de costos produjo un resultado inconsistente."""
