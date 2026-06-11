"""
AGENTE DIARIO
Compone mensajes dinamicos leyendo la base de datos:
rutina del dia, dieta, macros, suplementos, checkin.

La IA no espera mensajes: dirige al alumno todo el dia.
"""

from datetime import datetime

from database.conexion import supabase
from utils.logger import obtener_logger

logger = obtener_logger("AgenteDiario")

DIAS_SEMANA = [
    "lunes", "martes", "miercoles",
    "jueves", "viernes", "sabado", "domingo"
]


def dia_semana_hoy():

    return DIAS_SEMANA[datetime.now().weekday()]


# =========================================================
# RUTINA DEL DIA (desde rutinas_programadas)
# =========================================================

def obtener_rutina_del_dia(alumno_id: str):

    """
    Devuelve la rutina de hoy:
    {grupo_muscular, objetivo, duracion, ejercicios[]}
    o None si hoy no entrena.
    """

    try:

        hoy = dia_semana_hoy()

        res = (
            supabase
            .table("rutinas_programadas")
            .select("*")
            .eq("alumno_id", alumno_id)
            .eq("activa", True)
            .execute()
        )

        if not res.data:
            return None

        for rutina in res.data:

            dia = str(
                rutina.get("dia_semana") or ""
            ).lower().strip()

            # tolerar acentos: miércoles / sábado
            dia = (
                dia
                .replace("é", "e")
                .replace("á", "a")
            )

            if dia == hoy:
                return rutina

        return None

    except Exception as e:

        logger.error(
            f"❌ Error leyendo rutina del dia: {str(e)}"
        )

        return None


def formatear_ejercicios(rutina: dict):

    """
    Convierte el jsonb de ejercicios en texto:
    Jalon al pecho - 4 x 12
    """

    ejercicios = rutina.get("ejercicios") or []

    if not isinstance(ejercicios, list):
        return ""

    lineas = []

    for ej in ejercicios:

        if isinstance(ej, str):

            lineas.append(f"• {ej}")

            continue

        nombre = (
            ej.get("nombre")
            or ej.get("ejercicio")
            or "Ejercicio"
        )

        series = (
            ej.get("series")
            or ej.get("sets")
        )

        reps = (
            ej.get("repeticiones")
            or ej.get("reps")
        )

        if series and reps:

            lineas.append(
                f"• {nombre} — {series} x {reps}"
            )

        else:

            lineas.append(f"• {nombre}")

    return "\n".join(lineas)


# =========================================================
# MACROS DEL ALUMNO (desde historial_planes)
# =========================================================

def obtener_macros(alumno_id: str):

    """
    Devuelve texto con kcal y macros del plan vigente.
    """

    try:

        res = (
            supabase
            .table("historial_planes")
            .select("detalle_macros, tipo_plan")
            .eq("perfil_id", alumno_id)
            .order("fecha", desc=True)
            .limit(1)
            .execute()
        )

        if not res.data:
            return None

        macros = res.data[0].get("detalle_macros")

        if not isinstance(macros, dict):
            return None

        partes = []

        kcal = (
            macros.get("kcal")
            or macros.get("calorias")
        )

        if kcal:
            partes.append(f"• {kcal} kcal")

        proteina = (
            macros.get("proteina")
            or macros.get("proteinas")
        )

        if proteina:
            partes.append(f"• {proteina} g proteína")

        grasa = (
            macros.get("grasa")
            or macros.get("grasas")
        )

        if grasa:
            partes.append(f"• {grasa} g grasa")

        carbos = (
            macros.get("carbohidratos")
            or macros.get("carbos")
        )

        if carbos:
            partes.append(f"• {carbos} g carbohidratos")

        return "\n".join(partes) if partes else None

    except Exception as e:

        logger.error(
            f"❌ Error leyendo macros: {str(e)}"
        )

        return None


# =========================================================
# COMIDA PROGRAMADA (desde comidas_programadas)
# =========================================================

def obtener_comida(
    alumno_id: str,
    tipo_comida: str
):

    """
    Devuelve la comida de hoy de ese tipo
    (prioriza la del dia especifico sobre la general).
    """

    try:

        hoy = dia_semana_hoy()

        res = (
            supabase
            .table("comidas_programadas")
            .select("*")
            .eq("alumno_id", alumno_id)
            .eq("tipo_comida", tipo_comida)
            .eq("activa", True)
            .execute()
        )

        if not res.data:
            return None

        especifica = None
        general = None

        for c in res.data:

            dia = str(
                c.get("dia_semana") or ""
            ).lower().strip()

            dia = (
                dia
                .replace("é", "e")
                .replace("á", "a")
            )

            if dia == hoy:
                especifica = c
            elif not dia:
                general = c

        return especifica or general

    except Exception as e:

        logger.error(
            f"❌ Error leyendo comida: {str(e)}"
        )

        return None


# =========================================================
# COMPOSITORES DE MENSAJES
# =========================================================

EMOJIS_COMIDA = {
    "desayuno": "🍳",
    "colacion": "🥤",
    "almuerzo": "🍽️",
    "merienda": "🥪",
    "cena": "🌙",
    "post_entreno": "💪"
}

NOMBRES_COMIDA = {
    "desayuno": "Desayuno",
    "colacion": "Colación",
    "almuerzo": "Almuerzo",
    "merienda": "Merienda",
    "cena": "Cena",
    "post_entreno": "Post entrenamiento"
}


def componer_resumen_matutino(
    alumno_id: str,
    nombre: str
):

    hoy = dia_semana_hoy().capitalize()

    msg = f"Buenos días, {nombre} 💪\n"
    msg += f"Hoy es {hoy}"

    rutina = obtener_rutina_del_dia(alumno_id)

    if rutina:

        grupo = rutina.get(
            "grupo_muscular",
            "Entrenamiento"
        )

        msg += f" y toca:\n\n🏋️ {grupo}"

        if rutina.get("objetivo"):
            msg += f"\nObjetivo: {rutina['objetivo']}"

    else:

        msg += ".\n\n😌 Hoy es día de descanso. " \
               "Aprovechá para recuperar."

    macros = obtener_macros(alumno_id)

    if macros:

        msg += f"\n\nObjetivo nutricional del día:\n{macros}"

    # 🛒 LISTA DE COMPRAS: el dia 1 de cada mes
    if datetime.now().day == 1:

        try:

            lista = (
                supabase
                .table("listas_compras")
                .select("detalle")
                .eq("alumno_id", alumno_id)
                .eq("activa", True)
                .order("fecha_generada", desc=True)
                .limit(1)
                .execute()
            )

            if lista.data:

                msg += (
                    "\n\n🛒 ARRANCA EL MES — "
                    "Tu lista de compras:\n"
                )

                msg += lista.data[0]["detalle"]

        except Exception:

            pass

    msg += "\n\n¡Vamos por un gran día! 🔥"

    return msg


def componer_mensaje_comida(
    alumno_id: str,
    tipo_comida: str
):

    comida = obtener_comida(
        alumno_id,
        tipo_comida
    )

    if not comida:
        return None

    emoji = EMOJIS_COMIDA.get(tipo_comida, "🍴")
    titulo = NOMBRES_COMIDA.get(
        tipo_comida,
        tipo_comida.replace("_", " ").capitalize()
    )

    # 🔄 ROTACION DE OPCIONES: cada dia toca una distinta
    opciones = comida.get("opciones") or []

    if isinstance(opciones, list) and opciones:

        indice = datetime.now().toordinal() % len(opciones)

        detalle = opciones[indice]

        extra = (
            f"\n\n(Opción {indice + 1} de {len(opciones)} "
            f"de tu plan)"
        )

    else:

        detalle = comida.get("detalle", "")
        extra = ""

    msg = f"{titulo} {emoji}\n"
    msg += "Hoy corresponde:\n\n"
    msg += detalle + extra

    if comida.get("kcal"):
        msg += f"\n\nAproximadamente {comida['kcal']} kcal."

    return msg


def componer_mensaje_entrenamiento(
    alumno_id: str,
    nombre: str
):

    rutina = obtener_rutina_del_dia(alumno_id)

    if not rutina:
        return None

    grupo = rutina.get(
        "grupo_muscular",
        "Entrenamiento"
    )

    msg = f"🏋️ ENTRENAMIENTO DEL DÍA — {grupo}\n\n"

    ejercicios_txt = formatear_ejercicios(rutina)

    if ejercicios_txt:
        msg += ejercicios_txt
    else:
        msg += "Consultá tu rutina con tu entrenador."

    if rutina.get("duracion_minutos"):
        msg += f"\n\n⏱️ Duración estimada: " \
               f"{rutina['duracion_minutos']} min"

    msg += f"\n\n¡A darle con todo, {nombre}! 🔥"

    return msg


def componer_pre_entrenamiento(
    alumno_id: str,
    nombre: str
):

    rutina = obtener_rutina_del_dia(alumno_id)

    msg = f"⏰ {nombre}, en 60 minutos comienza " \
          f"tu entrenamiento.\n\nPrepará:\n" \
          f"• Agua\n• Toalla\n• Creatina"

    if rutina:

        grupo = rutina.get("grupo_muscular", "")

        if grupo:
            msg += f"\n\nHoy toca: {grupo} 💪"

    return msg


def componer_post_entrenamiento(
    alumno_id: str,
    nombre: str
):

    msg = f"💪 ¿Cómo te fue el entrenamiento, {nombre}?\n\n"

    comida = obtener_comida(
        alumno_id,
        "post_entreno"
    )

    if comida:
        msg += f"Recordá tu post entreno:\n" \
               f"{comida.get('detalle', '')}\n\n"

    msg += "Contame qué ejercicios hiciste y con " \
           "cuánto peso (ej: sentadilla 60kg 4x10) " \
           "así registro tu progreso 📈"

    return msg


def componer_checkin_nocturno(
    nombre: str
):

    return (
        f"📋 Cierre del día, {nombre}\n\n"
        f"¿Cumpliste hoy?\n"
        f"✅ Dieta\n"
        f"✅ Entrenamiento\n"
        f"✅ Agua\n\n"
        f"Respondé:\n"
        f"1 = Sí, todo\n"
        f"2 = Parcial\n"
        f"3 = No pude"
    )


# =========================================================
# DISPATCHER PRINCIPAL
# =========================================================

def componer_mensaje_dinamico(
    tipo_alerta: str,
    alumno_id: str,
    nombre: str,
    detalle: str = ""
):

    """
    Devuelve el mensaje compuesto desde la BD,
    o None para que el ciclo use la plantilla
    estatica de siempre (fallback seguro).
    """

    try:

        if tipo_alerta == "resumen_diario":

            return componer_resumen_matutino(
                alumno_id, nombre
            )

        if tipo_alerta == "comida":

            tipo_comida = (
                detalle or "almuerzo"
            ).lower().strip()

            return componer_mensaje_comida(
                alumno_id, tipo_comida
            )

        if tipo_alerta == "entrenamiento":

            return componer_mensaje_entrenamiento(
                alumno_id, nombre
            )

        if tipo_alerta == "pre_entrenamiento":

            return componer_pre_entrenamiento(
                alumno_id, nombre
            )

        if tipo_alerta == "post_entreno":

            return componer_post_entrenamiento(
                alumno_id, nombre
            )

        if tipo_alerta == "checkin_nocturno":

            return componer_checkin_nocturno(
                nombre
            )

        return None

    except Exception as e:

        logger.error(
            f"❌ Error componiendo mensaje "
            f"[{tipo_alerta}]: {str(e)}"
        )

        return None