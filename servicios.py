"""Servicio abstracto y tres servicios especializados (polimorfismo)."""  # Docstring del módulo
from abc import abstractmethod  # Para declarar métodos abstractos
from functools import singledispatchmethod  # Permite sobrecarga de métodos según el tipo de argumento

from entidades import Entidad  # Clase base abstracta
from excepciones import CalculoInconsistenteError, ServicioInvalidoError  # Excepciones propias usadas aquí
from logger import log  # Logger (disponible para registrar eventos)


class Servicio(Entidad):  # Clase abstracta Servicio, hereda de Entidad
    """Clase abstracta Servicio."""  # Docstring de la clase

    def __init__(self, nombre: str, tarifa_hora: float) -> None:  # Constructor común a todos los servicios
        super().__init__()  # Asigna el id mediante Entidad
        if not isinstance(nombre, str) or not nombre.strip():  # El nombre debe ser texto no vacío
            raise ServicioInvalidoError("El servicio requiere un nombre.")  # Error si falta el nombre
        if not isinstance(tarifa_hora, (int, float)) or tarifa_hora <= 0:  # La tarifa debe ser un número positivo
            raise ServicioInvalidoError(f"Tarifa inválida: {tarifa_hora!r}")  # Error si la tarifa no es válida
        self._nombre = nombre.strip()  # Guarda el nombre sin espacios sobrantes
        self._tarifa_hora = float(tarifa_hora)  # Guarda la tarifa como número decimal
        self._disponible = True  # Todo servicio nuevo inicia disponible

    @property  # Getter del nombre
    def nombre(self) -> str:  # Devuelve el nombre del servicio
        return self._nombre  # Retorna el atributo protegido

    @property  # Getter de la disponibilidad
    def disponible(self) -> bool:  # Indica si el servicio puede reservarse
        return self._disponible  # Retorna el estado actual

    @disponible.setter  # Setter de la disponibilidad
    def disponible(self, valor: bool) -> None:  # Recibe el nuevo estado
        self._disponible = bool(valor)  # Convierte a booleano y guarda

    # ---- métodos abstractos: cada servicio hijo debe sobrescribirlos ----
    @abstractmethod  # Obliga a implementar el cálculo en cada servicio
    def calcular_costo(self, duracion: float, impuesto: float = 0.0, descuento: float = 0.0) -> float:  # Impuesto y descuento son opcionales (sobrecarga)
        """Costo con impuesto y descuento opcionales."""  # Docstring del método abstracto

    @abstractmethod  # Obliga a implementar la validación en cada servicio
    def validar_parametros(self, duracion: float) -> None:  # Valida la duración solicitada
        """Lanza ServicioInvalidoError si la duración no es válida."""  # Docstring del método abstracto

    # ---- método sobrecargado según el tipo del argumento ----
    @singledispatchmethod  # Método genérico: elige la variante según el tipo de 'extra'
    def calcular_costo_total(self, extra, duracion: float) -> float:  # Variante por defecto (tipo no soportado)
        raise ServicioInvalidoError(f"Tipo de ajuste no soportado: {type(extra).__name__}")  # Error si el tipo no está registrado

    @calcular_costo_total.register(float)  # Variante para números decimales
    @calcular_costo_total.register(int)  # Variante para números enteros
    def _(self, extra, duracion: float) -> float:  # Implementación cuando 'extra' es un número
        """Variante 1: un número = porcentaje de impuesto (0.19 = 19 %)."""  # Docstring de la variante
        return self.calcular_costo(duracion, impuesto=extra)  # Calcula el costo aplicando solo impuesto

    @calcular_costo_total.register(dict)  # Variante para diccionarios
    def _(self, extra: dict, duracion: float) -> float:  # Implementación cuando 'extra' es un diccionario
        """Variante 2: diccionario con 'impuesto' y/o 'descuento'."""  # Docstring de la variante
        return self.calcular_costo(duracion, extra.get("impuesto", 0.0), extra.get("descuento", 0.0))  # Usa 0 si falta alguna clave

    @calcular_costo_total.register(str)  # Variante para texto (cupón)
    def _(self, extra: str, duracion: float) -> float:  # Implementación cuando 'extra' es un código de cupón
        """Variante 3: código de cupón."""  # Docstring de la variante
        cupones = {"FJ10": 0.10, "FJ20": 0.20}  # Cupones válidos y su porcentaje de descuento
        if extra.upper() not in cupones:  # Comprueba si el cupón existe
            raise ServicioInvalidoError(f"Cupón inexistente: {extra}")  # Error si el cupón no existe
        return self.calcular_costo(duracion, impuesto=0.19, descuento=cupones[extra.upper()])  # Aplica IVA 19 % y el descuento del cupón

    def _aplicar_ajustes(self, base: float, impuesto: float, descuento: float) -> float:  # Aplica impuesto y descuento a un costo base
        """Aplica impuesto y descuento y verifica que el resultado sea coherente."""  # Docstring del método
        if not (0 <= impuesto <= 1) or not (0 <= descuento < 1):  # Impuesto entre 0 y 100 %; descuento menor a 100 %
            raise CalculoInconsistenteError(f"Impuesto/descuento fuera de rango: {impuesto}, {descuento}")  # Error de cálculo inconsistente
        total = base * (1 - descuento) * (1 + impuesto)  # Fórmula: base, menos descuento, más impuesto
        if total <= 0:  # El costo final debe ser positivo
            raise CalculoInconsistenteError("El costo calculado no es positivo.")  # Error si el resultado no tiene sentido
        return round(total, 2)  # Devuelve el total redondeado a 2 decimales


class ReservaSala(Servicio):  # Servicio especializado 1: salas de reuniones
    """Reserva de salas de reuniones."""  # Docstring de la clase

    def __init__(self, nombre: str, tarifa_hora: float, capacidad: int) -> None:  # Constructor con capacidad de la sala
        super().__init__(nombre, tarifa_hora)  # Valida y guarda nombre y tarifa en la clase base
        if not isinstance(capacidad, int) or capacidad <= 0:  # La capacidad debe ser un entero positivo
            raise ServicioInvalidoError(f"Capacidad inválida: {capacidad!r}")  # Error si no es válida
        self._capacidad = capacidad  # Guarda la capacidad de la sala

    def validar_parametros(self, duracion: float) -> None:  # Sobrescribe la validación para salas
        if not isinstance(duracion, (int, float)) or not (1 <= duracion <= 8):  # Una sala se reserva de 1 a 8 horas
            raise ServicioInvalidoError("Una sala se reserva entre 1 y 8 horas.")  # Error si está fuera de rango

    def calcular_costo(self, duracion, impuesto=0.0, descuento=0.0) -> float:  # Sobrescribe el cálculo de costo
        self.validar_parametros(duracion)  # Valida la duración antes de calcular
        return self._aplicar_ajustes(self._tarifa_hora * duracion, impuesto, descuento)  # Costo = tarifa x horas, con ajustes

    def describir(self) -> str:  # Sobrescribe la descripción
        return f"Sala '{self._nombre}' (capacidad {self._capacidad}) - ${self._tarifa_hora:,.0f}/h"  # Texto descriptivo de la sala


class AlquilerEquipo(Servicio):  # Servicio especializado 2: alquiler de equipos
    """Alquiler de equipos (portátiles, proyectores...)."""  # Docstring de la clase

    def __init__(self, nombre: str, tarifa_hora: float, equipo: str, cantidad: int = 1) -> None:  # Constructor con equipo y cantidad
        super().__init__(nombre, tarifa_hora)  # Valida y guarda nombre y tarifa
        if not equipo or not isinstance(equipo, str):  # El equipo debe ser texto no vacío
            raise ServicioInvalidoError("Debe indicar el equipo a alquilar.")  # Error si falta el equipo
        if not isinstance(cantidad, int) or cantidad < 1:  # La cantidad debe ser un entero de al menos 1
            raise ServicioInvalidoError(f"Cantidad inválida: {cantidad!r}")  # Error si no es válida
        self._equipo, self._cantidad = equipo, cantidad  # Guarda el equipo y la cantidad

    def validar_parametros(self, duracion: float) -> None:  # Sobrescribe la validación para equipos
        if not isinstance(duracion, (int, float)) or not (1 <= duracion <= 72):  # Un equipo se alquila de 1 a 72 horas
            raise ServicioInvalidoError("Un equipo se alquila entre 1 y 72 horas.")  # Error si está fuera de rango

    def calcular_costo(self, duracion, impuesto=0.0, descuento=0.0) -> float:  # Sobrescribe el cálculo de costo
        self.validar_parametros(duracion)  # Valida la duración antes de calcular
        return self._aplicar_ajustes(self._tarifa_hora * duracion * self._cantidad, impuesto, descuento)  # Costo = tarifa x horas x cantidad

    def describir(self) -> str:  # Sobrescribe la descripción
        return f"Alquiler de {self._cantidad} x {self._equipo} - ${self._tarifa_hora:,.0f}/h c/u"  # Texto descriptivo del alquiler


class AsesoriaEspecializada(Servicio):  # Servicio especializado 3: asesorías
    """Asesoría con un especialista; el nivel senior tiene recargo."""  # Docstring de la clase

    RECARGO = {"junior": 1.0, "senior": 1.5}  # Multiplicador de tarifa según el nivel

    def __init__(self, nombre: str, tarifa_hora: float, especialidad: str, nivel: str = "junior") -> None:  # Constructor con especialidad y nivel
        super().__init__(nombre, tarifa_hora)  # Valida y guarda nombre y tarifa
        if nivel not in self.RECARGO:  # El nivel debe ser uno de los permitidos
            raise ServicioInvalidoError(f"Nivel inválido: {nivel!r} (use junior/senior)")  # Error si el nivel no existe
        if not especialidad:  # La especialidad no puede estar vacía
            raise ServicioInvalidoError("Debe indicar la especialidad.")  # Error si falta la especialidad
        self._especialidad, self._nivel = especialidad, nivel  # Guarda especialidad y nivel

    def validar_parametros(self, duracion: float) -> None:  # Sobrescribe la validación para asesorías
        if not isinstance(duracion, (int, float)) or not (0.5 <= duracion <= 6):  # Una asesoría dura de 0.5 a 6 horas
            raise ServicioInvalidoError("Una asesoría dura entre 0.5 y 6 horas.")  # Error si está fuera de rango

    def calcular_costo(self, duracion, impuesto=0.0, descuento=0.0) -> float:  # Sobrescribe el cálculo de costo
        self.validar_parametros(duracion)  # Valida la duración antes de calcular
        base = self._tarifa_hora * duracion * self.RECARGO[self._nivel]  # Base = tarifa x horas x recargo por nivel
        return self._aplicar_ajustes(base, impuesto, descuento)  # Aplica impuesto y descuento sobre la base

    def describir(self) -> str:  # Sobrescribe la descripción
        return f"Asesoría de {self._especialidad} (nivel {self._nivel}) - ${self._tarifa_hora:,.0f}/h"  # Texto descriptivo de la asesoría
