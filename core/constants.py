# core/constants.py

class Roles:
    """Definición estricta de los roles del sistema."""
    ADMIN = "admin"
    TRAINER = "entrenador"
    ALUMNO = "alumno"

class Permisos:
    """Catálogo de todas las acciones posibles en la plataforma."""
    VER_DASHBOARD_COACH = "ver_dashboard_coach"
    EDITAR_RUTINAS = "editar_rutinas"
    ENVIAR_WHATSAPP = "enviar_whatsapp"
    GESTIONAR_PAGOS = "gestionar_pagos"
    VER_FICHA_PROPIA = "ver_ficha_propia"