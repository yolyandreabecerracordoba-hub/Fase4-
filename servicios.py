"""Servicio abstracto y tres servicios especializados (polimorfismo)."""
from abc import abstractmethod
from functools import singledispatchmethod

from entidades import Entidad
from excepciones import CalculoInconsistenteError, ServicioInvalidoError
from logger import log


class Servicio(Entidad):
    """Clase abstracta Servicio."""

    def __init__(self, nombre: str, tarifa_hora: float) -> None:
        super().__init__()
        if not isinstance(nombre, str) or not nombre.strip():
            raise ServicioInvalidoError("El servicio requiere un nombre.")
        if not isinstance(tarifa_hora, (int, float)) or tarifa_hora <= 0:
            raise ServicioInvalidoError(f"Tarifa inválida: {tarifa_hora!r}")
        self._nombre = nombre.strip()
        self._tarifa_hora = float(tarifa_hora)
        self._disponible = True

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, valor: bool) -> None:
        self._disponible = bool(valor)

    # ---- métodos abstractos: cada servicio los sobrescribe ----
    @abstractmethod
    def calcular_costo(self, duracion: float, impuesto: float = 0.0, descuento: float = 0.0) -> float:
        """Costo con impuesto y descuento opcionales (sobrecarga por parámetros opcionales)."""

    @abstractmethod
    def validar_parametros(self, duracion: float) -> None:
        """Lanza ServicioInvalidoError si la duración no es válida."""

    # ---- método sobrecargado por tipo de argumento ----
    @singledispatchmethod
    def calcular_costo_total(self, extra, duracion: float) -> float:
        raise ServicioInvalidoError(f"Tipo de ajuste no soportado: {type(extra).__name__}")

    @calcular_costo_total.register(float)
    @calcular_costo_total.register(int)
    def _(self, extra, duracion: float) -> float:
        """Variante 1: un número = porcentaje de impuesto (0.19 = 19 %)."""
        return self.calcular_costo(duracion, impuesto=extra)

    @calcular_costo_total.register(dict)
    def _(self, extra: dict, duracion: float) -> float:
        """Variante 2: diccionario con 'impuesto' y/o 'descuento'."""
        return self.calcular_costo(duracion, extra.get("impuesto", 0.0), extra.get("descuento", 0.0))

    @calcular_costo_total.register(str)
    def _(self, extra: str, duracion: float) -> float:
        """Variante 3: código de cupón."""
        cupones = {"FJ10": 0.10, "FJ20": 0.20}
        if extra.upper() not in cupones:
            raise ServicioInvalidoError(f"Cupón inexistente: {extra}")
        return self.calcular_costo(duracion, impuesto=0.19, descuento=cupones[extra.upper()])

    def _aplicar_ajustes(self, base: float, impuesto: float, descuento: float) -> float:
        """Aplica impuesto y descuento y verifica que el resultado sea coherente."""
        if not (0 <= impuesto <= 1) or not (0 <= descuento < 1):
            raise CalculoInconsistenteError(f"Impuesto/descuento fuera de rango: {impuesto}, {descuento}")
        total = base * (1 - descuento) * (1 + impuesto)
        if total <= 0:
            raise CalculoInconsistenteError("El costo calculado no es positivo.")
        return round(total, 2)


class ReservaSala(Servicio):
    """Reserva de salas de reuniones."""

    def __init__(self, nombre: str, tarifa_hora: float, capacidad: int) -> None:
        super().__init__(nombre, tarifa_hora)
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise ServicioInvalidoError(f"Capacidad inválida: {capacidad!r}")
        self._capacidad = capacidad

    def validar_parametros(self, duracion: float) -> None:
        if not isinstance(duracion, (int, float)) or not (1 <= duracion <= 8):
            raise ServicioInvalidoError("Una sala se reserva entre 1 y 8 horas.")

    def calcular_costo(self, duracion, impuesto=0.0, descuento=0.0) -> float:
        self.validar_parametros(duracion)
        return self._aplicar_ajustes(self._tarifa_hora * duracion, impuesto, descuento)

    def describir(self) -> str:
        return f"Sala '{self._nombre}' (capacidad {self._capacidad}) - ${self._tarifa_hora:,.0f}/h"


class AlquilerEquipo(Servicio):
    """Alquiler de equipos (portátiles, proyectores...)."""

    def __init__(self, nombre: str, tarifa_hora: float, equipo: str, cantidad: int = 1) -> None:
        super().__init__(nombre, tarifa_hora)
        if not equipo or not isinstance(equipo, str):
            raise ServicioInvalidoError("Debe indicar el equipo a alquilar.")
        if not isinstance(cantidad, int) or cantidad < 1:
            raise ServicioInvalidoError(f"Cantidad inválida: {cantidad!r}")
        self._equipo, self._cantidad = equipo, cantidad

    def validar_parametros(self, duracion: float) -> None:
        if not isinstance(duracion, (int, float)) or not (1 <= duracion <= 72):
            raise ServicioInvalidoError("Un equipo se alquila entre 1 y 72 horas.")

    def calcular_costo(self, duracion, impuesto=0.0, descuento=0.0) -> float:
        self.validar_parametros(duracion)
        return self._aplicar_ajustes(self._tarifa_hora * duracion * self._cantidad, impuesto, descuento)

    def describir(self) -> str:
        return f"Alquiler de {self._cantidad} x {self._equipo} - ${self._tarifa_hora:,.0f}/h c/u"


class AsesoriaEspecializada(Servicio):
    """Asesoría con un especialista; el nivel senior tiene recargo."""

    RECARGO = {"junior": 1.0, "senior": 1.5}

    def __init__(self, nombre: str, tarifa_hora: float, especialidad: str, nivel: str = "junior") -> None:
        super().__init__(nombre, tarifa_hora)
        if nivel not in self.RECARGO:
            raise ServicioInvalidoError(f"Nivel inválido: {nivel!r} (use junior/senior)")
        if not especialidad:
            raise ServicioInvalidoError("Debe indicar la especialidad.")
        self._especialidad, self._nivel = especialidad, nivel

    def validar_parametros(self, duracion: float) -> None:
        if not isinstance(duracion, (int, float)) or not (0.5 <= duracion <= 6):
            raise ServicioInvalidoError("Una asesoría dura entre 0.5 y 6 horas.")

    def calcular_costo(self, duracion, impuesto=0.0, descuento=0.0) -> float:
        self.validar_parametros(duracion)
        base = self._tarifa_hora * duracion * self.RECARGO[self._nivel]
        return self._aplicar_ajustes(base, impuesto, descuento)

    def describir(self) -> str:
        return f"Asesoría de {self._especialidad} (nivel {self._nivel}) - ${self._tarifa_hora:,.0f}/h"
