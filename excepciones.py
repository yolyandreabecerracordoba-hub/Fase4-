"""Excepciones personalizadas del sistema Software FJ."""  # Docstring: describe el propósito del módulo


class SoftwareFJError(Exception):  # Excepción base: todas las demás heredan de ella
    """Excepción base de la que heredan todos los errores del sistema."""  # Permite capturar cualquier error del sistema con un solo except


class ParametroFaltanteError(SoftwareFJError):  # Error cuando falta un dato obligatorio
    """Se omitió un parámetro obligatorio."""  # Ejemplo: crear un cliente sin email


class ClienteInvalidoError(SoftwareFJError):  # Error de validación de datos del cliente
    """Los datos de un cliente no cumplen las validaciones."""  # Ejemplo: email o teléfono mal formado


class ServicioInvalidoError(SoftwareFJError):  # Error de validación de datos o parámetros de un servicio
    """Los parámetros de un servicio son inválidos."""  # Ejemplo: tarifa negativa o duración fuera de rango


class ServicioNoDisponibleError(SoftwareFJError):  # Error cuando el servicio está deshabilitado
    """El servicio solicitado no está disponible."""  # Ejemplo: reservar un equipo ya no disponible


class ReservaError(SoftwareFJError):  # Error general de la gestión de reservas
    """Error general durante la gestión de una reserva."""  # Se usa para encadenar errores técnicos


class OperacionNoPermitidaError(ReservaError):  # Error por una operación inválida según el estado
    """La operación no es válida para el estado actual de la reserva."""  # Ejemplo: cancelar dos veces


class CalculoInconsistenteError(SoftwareFJError):  # Error cuando un cálculo da un resultado incoherente
    """Un cálculo de costos produjo un resultado inconsistente."""  # Ejemplo: impuesto mayor al 100 %
