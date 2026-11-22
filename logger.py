"""Configuración del archivo de logs (único uso permitido de archivos)."""  # Docstring del módulo
import logging  # Módulo estándar de Python para registrar eventos
import os  # Módulo para manejar rutas y carpetas del sistema

RUTA_LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs", "software_fj.log")  # Ruta del log: carpeta logs junto a este archivo


def obtener_logger() -> logging.Logger:  # Función que crea y devuelve el logger
    """Devuelve el logger del sistema; crea la carpeta y el archivo si no existen."""  # Docstring de la función
    logger = logging.getLogger("software_fj")  # Obtiene (o crea) un logger con nombre propio
    if not logger.handlers:  # Solo configura si aún no tiene handlers (evita duplicar líneas)
        os.makedirs(os.path.dirname(RUTA_LOG), exist_ok=True)  # Crea la carpeta logs si no existe
        handler = logging.FileHandler(RUTA_LOG, encoding="utf-8")  # Handler que escribe en el archivo de log
        handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s"))  # Formato: fecha | nivel | mensaje
        logger.addHandler(handler)  # Asocia el handler al logger
        logger.setLevel(logging.INFO)  # Registra eventos desde nivel INFO hacia arriba
    return logger  # Devuelve el logger configurado


log = obtener_logger()  # Instancia global que importan los demás módulos
