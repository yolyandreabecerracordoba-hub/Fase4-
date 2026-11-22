"""Clase abstracta que representa las entidades generales del sistema."""  # Docstring del módulo
from abc import ABC, abstractmethod  # ABC y abstractmethod permiten definir clases abstractas
from itertools import count  # count genera números consecutivos para los ids


class Entidad(ABC):  # Clase abstracta: no se puede instanciar directamente
    """Entidad base: todo objeto del sistema tiene un identificador único."""  # Docstring de la clase

    _contador = count(1)  # Generador compartido por todas las entidades: 1, 2, 3...

    def __init__(self) -> None:  # Constructor de la entidad
        self._id = next(Entidad._contador)  # Asigna el siguiente id disponible (atributo encapsulado)

    @property  # Expone el id como propiedad de solo lectura
    def id(self) -> int:  # Getter del identificador
        """Identificador de solo lectura."""  # Docstring del getter
        return self._id  # Devuelve el id sin permitir modificarlo

    @abstractmethod  # Obliga a las clases hijas a implementar este método
    def describir(self) -> str:  # Cada entidad debe poder describirse
        """Cada entidad debe describirse a sí misma."""  # Docstring del método abstracto

    def __str__(self) -> str:  # Método especial: texto al imprimir el objeto
        return self.describir()  # Usa la descripción propia de cada entidad (polimorfismo)
