"""Configuración del archivo de logs (único uso permitido de archivos)."""
import logging
import os

RUTA_LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs", "software_fj.log")


def obtener_logger() -> logging.Logger:
    """Devuelve el logger del sistema; crea la carpeta y el archivo si no existen."""
    logger = logging.getLogger("software_fj")
    if not logger.handlers:  # evita duplicar handlers
        os.makedirs(os.path.dirname(RUTA_LOG), exist_ok=True)
        handler = logging.FileHandler(RUTA_LOG, encoding="utf-8")
        handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s"))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger


log = obtener_logger()
