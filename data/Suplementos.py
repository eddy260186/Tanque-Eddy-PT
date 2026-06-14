# ==========================================
# BASE DE DATOS DE SUPLEMENTACIÓN GENERAL
# ==========================================
# Organizada por MOMENTO del día.
# El agente la envía a la hora correspondiente,
# calculada según la hora de entreno de cada alumno.
#
# Editá libremente: agregá, quitá o cambiá dosis.
# Cada item: {"nombre", "dosis", "nota" (opcional)}
# ==========================================

suplementos_db = {

    # Al despertar / con el desayuno
    "manana": [
        {"nombre": "Omega-3", "dosis": "1-2 g", "nota": "con la comida"},
        {"nombre": "Vitamina D3", "dosis": "2000 UI"},
        {"nombre": "Multivitamínico", "dosis": "1 cápsula"},
    ],

    # 30-45 min ANTES de entrenar
    "pre_entreno": [
        {"nombre": "Cafeína", "dosis": "200 mg", "nota": "energía y foco"},
        {"nombre": "Beta-alanina", "dosis": "3 g", "nota": "resistencia muscular"},
        {"nombre": "Citrulina Malato", "dosis": "6 g", "nota": "bombeo / congestión"},
    ],

    # Inmediatamente DESPUÉS de entrenar
    "post_entreno": [
        {"nombre": "Proteína Whey", "dosis": "30 g", "nota": "recuperación"},
        {"nombre": "Creatina Monohidrato", "dosis": "5 g", "nota": "todos los días, también en descanso"},
    ],

    # Antes de dormir
    "noche": [
        {"nombre": "Magnesio", "dosis": "300 mg", "nota": "relajación y sueño"},
        {"nombre": "Caseína / ZMA", "dosis": "según producto", "nota": "recuperación nocturna"},
    ],
}


# ==========================================
# DOSIS DE CREATINA EN DÍAS SIN ENTRENO
# (igual se toma, para mantener saturación)
# ==========================================
creatina_dia_descanso = {
    "nombre": "Creatina Monohidrato",
    "dosis": "5 g",
    "nota": "mantené la dosis aunque hoy no entrenes",
}