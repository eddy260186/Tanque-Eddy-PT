import logging
import sys

# Configuración base del log
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout) # Imprime en la consola del servidor
    ]
)

def obtener_logger(nombre_modulo: str):
    return logging.getLogger(nombre_modulo)