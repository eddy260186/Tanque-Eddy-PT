"""
MOTOR DE SUPLEMENTACIÓN AUTOMÁTICA
Asigna el stack ideal segun el perfil del alumno,
leyendo del catalogo data/suplementos.py.

Funciona POR DETRAS: el alumno nunca lo ve en su panel,
solo recibe los avisos por WhatsApp a su hora.

REGLA DE SEGURIDAD:
Si la alumna esta embarazada/lactancia o el alumno
declara una enfermedad/condicion medica, el motor NO
inventa un stack: marca el caso para revision manual
del entrenador.
"""

from database.conexion import supabase
from utils.logger import obtener_logger

# Catalogo de respaldo: si data/suplementos.py no carga,
# el motor igual asigna un stack basico universal.
_RESPALDO = {
    "manana": [
        {"nombre": "Omega-3", "dosis": "1-2 g", "nota": "con el desayuno"},
        {"nombre": "Vitamina D3", "dosis": "2000 UI"},
        {"nombre": "Vitamina C", "dosis": "1000 mg"},
        {"nombre": "Multivitamínico", "dosis": "1 cápsula"},
    ],
    "pre_entreno": [
        {"nombre": "Cafeína", "dosis": "200 mg", "nota": "energía y foco"},
        {"nombre": "Beta-Alanina", "dosis": "3 g"},
        {"nombre": "Citrulina Malato", "dosis": "6 g"},
        {"nombre": "L-Carnitina", "dosis": "2 g", "nota": "quema de grasa"},
    ],
    "post_entreno": [
        {"nombre": "Proteína Whey", "dosis": "30 g", "nota": "recuperación"},
        {"nombre": "Creatina Monohidrato", "dosis": "5 g", "nota": "todos los días"},
    ],
    "noche": [
        {"nombre": "Magnesio", "dosis": "300-400 mg", "nota": "descanso"},
        {"nombre": "ZMA", "dosis": "según producto"},
    ],
}

try:
    from data.suplementos import suplementos_db
    if not suplementos_db:
        suplementos_db = _RESPALDO
except Exception:
    suplementos_db = _RESPALDO

logger = obtener_logger("SuplementosIA")


# =========================================================
# DETECCION DE CASOS QUE REQUIEREN REVISION MANUAL
# =========================================================

PALABRAS_EMBARAZO = [
    "embaraz", "encinta", "gestac",
    "lactancia", "amamant", "lactando"
]

# Solo condiciones GRAVES que contraindican suplementos.
# Condiciones leves (colesterol, intolerancias) NO bloquean:
# el alumno recibe su stack normal.
PALABRAS_ENFERMEDAD = [
    "diabetes", "diabetic",
    "hipertension", "hipertensión", "presion alta", "presión alta",
    "renal", "riñon", "riñón", "rinon", "nefro",
    "higado", "hígado", "hepat", "cirrosis",
    "corazon", "corazón", "cardiac", "cardíac", "cardio",
    "tiroide", "epileps", "convuls",
    "cancer", "cáncer", "oncolog", "quimio",
    "anticoagul", "marcapasos", "arritmia",
    "insuficiencia"
]


def requiere_revision_manual(atleta: dict):

    """
    Devuelve (True, motivo) si el alumno NO debe recibir
    suplementacion automatica por seguridad.
    """

    # Campo de embarazo (puede ser bool o texto)
    embarazo = atleta.get("embarazo")

    if embarazo in (True, "true", "True", "si", "sí", "SI"):
        return True, "embarazo / lactancia"

    # Buscar en campos de texto libre
    textos = " ".join([
        str(atleta.get("embarazo") or ""),
        str(atleta.get("lesiones") or ""),
        str(atleta.get("restricciones_alimentarias") or ""),
        str(atleta.get("condiciones_medicas") or ""),
        str(atleta.get("enfermedades") or "")
    ]).lower()

    for palabra in PALABRAS_EMBARAZO:
        if palabra in textos:
            return True, "embarazo / lactancia"

    for palabra in PALABRAS_ENFERMEDAD:
        if palabra in textos:
            return True, f"condición médica declarada"

    return False, ""


# =========================================================
# SELECCION DE SUPLEMENTOS POR OBJETIVO
# =========================================================
# Para cada momento, elegimos los esenciales segun el
# objetivo. Usamos el nombre exacto del catalogo.
# =========================================================

def _buscar(momento: str, nombres: list):

    """Devuelve los items del catalogo cuyo nombre
    contiene alguno de los nombres dados. Si no encuentra
    ninguno, devuelve los primeros 3 de ese momento como
    respaldo (asi el motor nunca queda vacio)."""

    catalogo = suplementos_db.get(momento) or []

    elegidos = []

    for item in catalogo:

        nombre_item = str(item.get("nombre", "")).lower()

        for buscado in nombres:

            # Coincidencia flexible: contiene la palabra clave
            clave = buscado.lower().split()[0]  # primera palabra

            if clave in nombre_item:
                elegidos.append(item)
                break

    # Respaldo: si no matcheo nada, tomar los primeros del momento
    if not elegidos and catalogo:
        elegidos = catalogo[:3]

    return elegidos


def generar_stack_automatico(atleta: dict):

    """
    Arma el diccionario {momento: [suplementos]} ideal
    segun objetivo, sexo, edad y nivel del alumno.

    Stack base seguro y universal para personas sanas.
    """

    objetivo = str(
        atleta.get("objetivo_actual")
        or atleta.get("objetivo_principal")
        or ""
    ).lower()

    genero = str(atleta.get("genero") or "").lower()

    stack = {}

    # -----------------------------------------------------
    # BASE UNIVERSAL (todos los sanos)
    # -----------------------------------------------------

    stack["manana"] = _buscar("manana", [
        "Omega-3", "Vitamina D3", "Multivitamínico"
    ])

    stack["post_entreno"] = _buscar("post_entreno", [
        "Proteína Whey (Concentrado)",
        "Creatina Monohidrato"
    ])

    stack["noche"] = _buscar("noche", [
        "Magnesio"
    ])

    # -----------------------------------------------------
    # SEGUN OBJETIVO
    # -----------------------------------------------------

    if any(x in objetivo for x in [
        "grasa", "definición", "definicion",
        "perder", "bajar", "deficit", "déficit"
    ]):

        # Perdida de grasa: pre-entreno con cafeina + carnitina
        stack["pre_entreno"] = _buscar("pre_entreno", [
            "Cafeína Anhidra",
            "L-Carnitina (Tartrato)"
        ])

    elif any(x in objetivo for x in [
        "musculo", "músculo", "volumen",
        "masa", "fuerza", "hipertrofia"
    ]):

        # Volumen / fuerza: pre con citrulina + beta-alanina
        stack["pre_entreno"] = _buscar("pre_entreno", [
            "Cafeína Anhidra",
            "Citrulina Malato",
            "Beta-Alanina"
        ])

    else:

        # Recomposición / mantenimiento: pre suave
        stack["pre_entreno"] = _buscar("pre_entreno", [
            "Cafeína Anhidra",
            "Citrulina Malato"
        ])

    # -----------------------------------------------------
    # AJUSTE POR SEXO (mujer: refuerzo de hierro/calcio
    # solo si no hay condiciones, ya filtrado antes)
    # -----------------------------------------------------

    if genero in ("f", "femenino", "mujer"):

        extra = _buscar("manana", ["Hierro", "Calcio"])

        # Evitar duplicados
        nombres_actuales = {
            s["nombre"] for s in stack["manana"]
        }

        for e in extra:
            if e["nombre"] not in nombres_actuales:
                stack["manana"].append(e)

    # Limpiar momentos vacios
    stack = {
        m: items for m, items in stack.items() if items
    }

    return stack


# =========================================================
# GUARDAR EL STACK EN LA BD (por detras)
# =========================================================

def asignar_suplementacion_automatica(
    alumno_id: str,
    solo_si_vacio: bool = True
):

    """
    Punto de entrada. Lee el perfil del alumno y:
    - Si requiere revision manual -> marca y NO asigna.
    - Si es sano -> asigna el stack automatico.

    Devuelve (estado, detalle):
      estado: 'asignado' | 'revision_manual' | 'ya_tenia' | 'error'
    """

    try:

        res = (
            supabase
            .table("perfiles_atletas")
            .select("*")
            .eq("id", alumno_id)
            .execute()
        )

        if not res.data:
            return "error", "Alumno no encontrado"

        atleta = res.data[0]

        # No pisar lo que el entrenador ya cargo
        if solo_si_vacio:

            existentes = (
                supabase
                .table("suplementos_alumno")
                .select("id")
                .eq("alumno_id", alumno_id)
                .limit(1)
                .execute()
            )

            if existentes.data:
                return "ya_tenia", "Ya tiene suplementación cargada"

        # -------------------------------------------------
        # FILTRO DE SEGURIDAD
        # -------------------------------------------------

        revisar, motivo = requiere_revision_manual(atleta)

        if revisar:

            logger.info(
                f"⚠️ {atleta.get('nombre_completo')}: "
                f"requiere revisión manual ({motivo}). "
                f"No se asigna stack automático."
            )

            return "revision_manual", motivo

        # -------------------------------------------------
        # GENERAR Y GUARDAR STACK
        # -------------------------------------------------

        stack = generar_stack_automatico(atleta)

        if not stack:
            return "error", "No se pudo generar stack"

        filas = []

        for momento, items in stack.items():

            for sup in items:

                filas.append({
                    "alumno_id": alumno_id,
                    "momento": momento,
                    "nombre": sup.get("nombre"),
                    "dosis": sup.get("dosis"),
                    "nota": sup.get("nota"),
                    "activo": True
                })

        if filas:

            supabase.table(
                "suplementos_alumno"
            ).insert(filas).execute()

        logger.info(
            f"✅ Suplementación automática asignada a "
            f"{atleta.get('nombre_completo')}: "
            f"{len(filas)} suplementos."
        )

        return "asignado", f"{len(filas)} suplementos"

    except Exception as e:

        logger.error(
            f"❌ Error asignando suplementación: {str(e)}"
        )

        return "error", str(e)