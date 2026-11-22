"""Clase Cliente con validaciones robustas y encapsulación."""
import re

from entidades import Entidad
from excepciones import ClienteInvalidoError, ParametroFaltanteError
from logger import log

_EMAIL = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")


class Cliente(Entidad):
    """Cliente de Software FJ. Los datos personales son privados."""

    def __init__(self, nombre=None, email=None, telefono=None) -> None:
        super().__init__()
        try:
            if nombre is None or email is None or telefono is None:
                raise ParametroFaltanteError("Nombre, email y teléfono son obligatorios.")
            self.__nombre = self._validar_nombre(nombre)
            self.__email = self._validar_email(email)
            self.__telefono = self._validar_telefono(telefono)
        except (ParametroFaltanteError, ClienteInvalidoError) as e:
            log.error("Registro de cliente rechazado: %s", e)
            raise
        else:
            log.info("Cliente registrado: id=%s nombre=%s", self.id, self.__nombre)

    # ---- validaciones (métodos estáticos reutilizables por los setters) ----
    @staticmethod
    def _validar_nombre(nombre) -> str:
        if not isinstance(nombre, str) or len(nombre.strip()) < 3:
            raise ClienteInvalidoError("El nombre debe ser texto de al menos 3 caracteres.")
        if any(ch.isdigit() for ch in nombre):
            raise ClienteInvalidoError("El nombre no puede contener números.")
        return nombre.strip().title()

    @staticmethod
    def _validar_email(email) -> str:
        if not isinstance(email, str) or not _EMAIL.match(email.strip()):
            raise ClienteInvalidoError(f"Email inválido: {email!r}")
        return email.strip().lower()

    @staticmethod
    def _validar_telefono(telefono) -> str:
        t = str(telefono).strip()
        if not (t.isdigit() and len(t) == 10):
            raise ClienteInvalidoError(f"Teléfono inválido (deben ser 10 dígitos): {telefono!r}")
        return t

    # ---- propiedades (encapsulación) ----
    @property
    def nombre(self) -> str:
        return self.__nombre

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, valor) -> None:
        self.__email = self._validar_email(valor)

    @property
    def telefono(self) -> str:
        return self.__telefono

    @telefono.setter
    def telefono(self, valor) -> None:
        self.__telefono = self._validar_telefono(valor)

    def describir(self) -> str:
        return f"Cliente #{self.id}: {self.__nombre} <{self.__email}> Tel: {self.__telefono}"
