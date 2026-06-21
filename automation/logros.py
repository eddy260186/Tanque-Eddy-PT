"""
SISTEMA DE LOGROS / MEDALLAS POR ENTRENOS
Cuando el alumno completa cierta cantidad de entrenos,
desbloquea una medalla (bronce, plata, oro, platino, leyenda)
y le llega un mensaje motivador por WhatsApp.

Un "entreno" = un DÍA en que el alumno reportó ejercicios
(no cuenta ejercicios sueltos, sino días entrenados).

La medalla se entrega UNA sola vez (se recuerda en logros_alumno).
"""

from database.conexion import supabase
from utils.logger import obtener_logger

logger = obtener_logger("Logros")


# =========================================================
# DEFINICIÓN DE MEDALLAS
# =========================================================
# Cada medalla: cantidad de entrenos, código, nivel, emoji,
# y el emoji de la próxima meta para motivar.
MEDALLAS = [
    {"entrenos": 10,  "codigo": "entrenos_10",  "nivel": "Bronce",  "emoji": "🥉", "siguiente": "🥈 Plata en 25 entrenos"},
    {"entrenos": 25,  "codigo": "entrenos_25",  "nivel": "Plata",   "emoji": "🥈", "siguiente": "🥇 Oro en 50 entrenos"},
    {"entrenos": 50,  "codigo": "entrenos_50",  "nivel": "Oro",     "emoji": "🥇", "siguiente": "💎 Platino en 100 entrenos"},
    {"entrenos": 100, "codigo": "entrenos_100", "nivel": "Platino", "emoji": "💎", "siguiente": "👑 Leyenda en 200 entrenos"},
    {"entrenos": 200, "codigo": "entrenos_200", "nivel": "Leyenda", "emoji": "👑", "siguiente": "¡Sos una LEYENDA! 🔥"},
]


# =========================================================
# CONTAR ENTRENOS (días distintos entrenados)
# =========================================================

def contar_entrenos(alumno_id: str) -> int:
    """
    Cuenta cuántos DÍAS distintos entrenó el alumno,
    leyendo de ejercicios_realizados.

    Un entreno = un día con ejercicios reportados.
    """
    try:
        res = (
            supabase
            .table("ejercicios_realizados")
            .select("created_at")
            .eq("alumno_id", alumno_id)
            .execute()
        )

        if not res.data:
            return 0

        # Contar días únicos (no ejercicios sueltos)
        dias = set()
        for fila in res.data:
            fecha = str(fila.get("created_at") or "")[:10]  # YYYY-MM-DD
            if fecha:
                dias.add(fecha)

        return len(dias)

    except Exception as e:
        logger.error(f"❌ Error contando entrenos: {str(e)}")
        return 0


# =========================================================
# OBTENER LOGROS YA GANADOS
# =========================================================

def logros_ya_ganados(alumno_id: str) -> set:
    """Devuelve el set de códigos de logros que el alumno ya tiene."""
    try:
        res = (
            supabase
            .table("logros_alumno")
            .select("codigo_logro")
            .eq("alumno_id", alumno_id)
            .execute()
        )
        return {l.get("codigo_logro") for l in (res.data or [])}
    except Exception as e:
        logger.error(f"❌ Error leyendo logros ganados: {str(e)}")
        return set()


# =========================================================
# COMPONER EL MENSAJE DE MEDALLA
# =========================================================

def componer_mensaje_medalla(nombre: str, medalla: dict) -> str:
    """Arma el mensaje de WhatsApp para una medalla ganada (estilo niveles)."""
    primer_nombre = (nombre or "Atleta").split()[0]

    msg = "━━━━━━━━━━━━━━━\n"
    msg += f"{medalla['emoji']} *NIVEL {medalla['nivel'].upper()} ALCANZADO*\n"
    msg += "━━━━━━━━━━━━━━━\n\n"
    msg += f"🏋️ *{medalla['entrenos']} entrenamientos completados*\n\n"
    msg += f"{primer_nombre}, desbloqueaste una nueva insignia. "
    msg += "¡Tu constancia está dando frutos! 💪\n\n"
    msg += f"🎯 Próxima meta: {medalla['siguiente']}\n\n"
    msg += "_Team Eddy — Software Elite_"

    return msg


# =========================================================
# REGISTRAR EL LOGRO GANADO
# =========================================================

def _guardar_logro(alumno_id: str, medalla: dict, total_entrenos: int):
    """Guarda en la BD que el alumno ganó esta medalla."""
    try:
        supabase.table("logros_alumno").insert({
            "alumno_id": alumno_id,
            "codigo_logro": medalla["codigo"],
            "nivel": medalla["nivel"],
            "entrenos_al_ganar": total_entrenos,
        }).execute()
        return True
    except Exception as e:
        # Si ya existía (constraint único), no es error grave
        logger.warning(f"No se guardó el logro {medalla['codigo']}: {str(e)}")
        return False


# =========================================================
# FUNCIÓN PRINCIPAL: CHEQUEAR Y ENTREGAR MEDALLAS
# =========================================================

def revisar_logros(alumno_id: str, nombre: str = ""):
    """
    Revisa si el alumno desbloqueó una o más medallas nuevas.
    Devuelve una LISTA de mensajes (uno por medalla nueva)
    para que el llamador los envíe por WhatsApp.

    Si no ganó nada nuevo, devuelve lista vacía.

    Se llama JUSTO DESPUÉS de que el alumno reporta un entreno.
    """
    mensajes = []

    try:
        total = contar_entrenos(alumno_id)

        if total <= 0:
            return mensajes

        ya_tiene = logros_ya_ganados(alumno_id)

        for medalla in MEDALLAS:

            # ¿Llegó a la cantidad y todavía no tiene esta medalla?
            if total >= medalla["entrenos"] and medalla["codigo"] not in ya_tiene:

                # Guardar el logro
                guardado = _guardar_logro(alumno_id, medalla, total)

                if guardado:
                    mensaje = componer_mensaje_medalla(nombre, medalla)
                    mensajes.append(mensaje)
                    logger.info(
                        f"🏅 {nombre} ganó {medalla['nivel']} "
                        f"({medalla['entrenos']} entrenos)."
                    )

        return mensajes

    except Exception as e:
        logger.error(f"❌ Error revisando logros: {str(e)}")
        return mensajes