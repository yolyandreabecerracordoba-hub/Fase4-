"""Clase abstracta que representa las entidades generales del sistema."""
from abc import ABC, abstractmethod
from itertools import count


class Entidad(ABC):
    """Entidad base: todo objeto del sistema tiene un identificador único."""

    _contador = count(1)  # generador compartido de ids

    def __init__(self) -> None:
        self._id = next(Entidad._contador)  # atributo encapsulado

    @property
    def id(self) -> int:
        """Identificador de solo lectura."""
        return self._id

    @abstractmethod
    def describir(self) -> str:
        """Cada entidad debe describirse a sí misma."""

    def __str__(self) -> str:
        return self.describir()
