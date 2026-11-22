"""Clase Cliente con validaciones robustas y encapsulación."""  # Docstring del módulo
import re  # Módulo de expresiones regulares para validar el email

from entidades import Entidad  # Clase abstracta de la que hereda Cliente
from excepciones import ClienteInvalidoError, ParametroFaltanteError  # Excepciones propias usadas aquí
from logger import log  # Logger para registrar eventos y errores

_EMAIL = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")  # Patrón de un email válido (texto@dominio.ext)


class Cliente(Entidad):  # Cliente hereda de Entidad
    """Cliente de Software FJ. Los datos personales son privados."""  # Docstring de la clase

    def __init__(self, nombre=None, email=None, telefono=None) -> None:  # Constructor; None permite detectar parámetros faltantes
        super().__init__()  # Llama al constructor de Entidad para asignar el id
        try:  # Inicia el bloque que puede producir errores de validación
            if nombre is None or email is None or telefono is None:  # Comprueba que no falte ningún dato
                raise ParametroFaltanteError("Nombre, email y teléfono son obligatorios.")  # Lanza el error de dato faltante
            self.__nombre = self._validar_nombre(nombre)  # Valida y guarda el nombre (atributo privado)
            self.__email = self._validar_email(email)  # Valida y guarda el email (atributo privado)
            self.__telefono = self._validar_telefono(telefono)  # Valida y guarda el teléfono (atributo privado)
        except (ParametroFaltanteError, ClienteInvalidoError) as e:  # Captura los errores propios del cliente
            log.error("Registro de cliente rechazado: %s", e)  # Registra el error en el archivo de log
            raise  # Vuelve a lanzar el error para que lo maneje quien llamó
        else:  # Se ejecuta solo si el try terminó sin errores
            log.info("Cliente registrado: id=%s nombre=%s", self.id, self.__nombre)  # Registra el éxito en el log

    # ---- validaciones reutilizables por el constructor y los setters ----
    @staticmethod  # Método que no necesita acceso a la instancia
    def _validar_nombre(nombre) -> str:  # Valida el nombre y lo devuelve normalizado
        if not isinstance(nombre, str) or len(nombre.strip()) < 3:  # Debe ser texto con al menos 3 caracteres
            raise ClienteInvalidoError("El nombre debe ser texto de al menos 3 caracteres.")  # Error si no cumple
        if any(ch.isdigit() for ch in nombre):  # Revisa si algún carácter es un número
            raise ClienteInvalidoError("El nombre no puede contener números.")  # Error si contiene dígitos
        return nombre.strip().title()  # Quita espacios y pone la primera letra de cada palabra en mayúscula

    @staticmethod  # Método estático de validación
    def _validar_email(email) -> str:  # Valida el email y lo devuelve normalizado
        if not isinstance(email, str) or not _EMAIL.match(email.strip()):  # Debe ser texto y coincidir con el patrón
            raise ClienteInvalidoError(f"Email inválido: {email!r}")  # Error con el valor recibido
        return email.strip().lower()  # Devuelve el email en minúsculas y sin espacios

    @staticmethod  # Método estático de validación
    def _validar_telefono(telefono) -> str:  # Valida el teléfono y lo devuelve como texto
        t = str(telefono).strip()  # Convierte a texto y quita espacios
        if not (t.isdigit() and len(t) == 10):  # Deben ser exactamente 10 dígitos
            raise ClienteInvalidoError(f"Teléfono inválido (deben ser 10 dígitos): {telefono!r}")  # Error si no cumple
        return t  # Devuelve el teléfono válido

    # ---- propiedades (encapsulación de los datos personales) ----
    @property  # Getter del nombre (solo lectura)
    def nombre(self) -> str:  # Devuelve el nombre del cliente
        return self.__nombre  # Accede al atributo privado

    @property  # Getter del email
    def email(self) -> str:  # Devuelve el email del cliente
        return self.__email  # Accede al atributo privado

    @email.setter  # Setter del email: permite cambiarlo con validación
    def email(self, valor) -> None:  # Recibe el nuevo email
        self.__email = self._validar_email(valor)  # Valida antes de guardar

    @property  # Getter del teléfono
    def telefono(self) -> str:  # Devuelve el teléfono del cliente
        return self.__telefono  # Accede al atributo privado

    @telefono.setter  # Setter del teléfono con validación
    def telefono(self, valor) -> None:  # Recibe el nuevo teléfono
        self.__telefono = self._validar_telefono(valor)  # Valida antes de guardar

    def describir(self) -> str:  # Implementa el método abstracto de Entidad
        return f"Cliente #{self.id}: {self.__nombre} <{self.__email}> Tel: {self.__telefono}"  # Texto descriptivo del cliente
