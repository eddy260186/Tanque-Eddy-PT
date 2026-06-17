# automation/reporte_semanal.py
"""
REPORTE SEMANAL PARA EL ENTRENADOR
Cada domingo a las 20:00 le llega al WhatsApp comercial de cada
entrenador un resumen DETALLADO de todos sus alumnos:
  - Quiénes cumplen (checkin + entrenos recientes)
  - Quiénes están flojos
  - Quiénes están por abandonar (sin actividad hace días)
  - Progreso de peso de cada uno

La BD es la fuente de verdad. Si la IA está caída, el reporte
igual sale, porque se arma con datos puros.
"""

from datetime import datetime, timedelta
from database.conexion import supabase
from backend.services.whatsapp_service import enviar_mensaje_texto_evolution
from utils.logger import obtener_logger

logger = obtener_logger("ReporteSemanal")


def _dias_desde(fecha_str):
    """Cuántos días pasaron desde una fecha ISO. Si no hay fecha, devuelve None."""
    if not fecha_str:
        return None
    try:
        fecha = datetime.fromisoformat(str(fecha_str).replace("Z", "+00:00"))
        # quitar tzinfo para comparar
        fecha = fecha.replace(tzinfo=None)
        return (datetime.now() - fecha).days
    except Exception:
        try:
            fecha = datetime.strptime(str(fecha_str)[:10], "%Y-%m-%d")
            return (datetime.now() - fecha).days
        except Exception:
            return None


def _clasificar_alumno(dias_checkin, dias_entreno):
    """
    Devuelve (categoria, emoji) según la actividad reciente.
    - cumpliendo: actividad en los últimos 3 días
    - flojo: actividad entre 4 y 7 días
    - abandonando: sin actividad hace más de 7 días (o nunca)
    """
    # Tomamos el dato más reciente de los dos (checkin o entreno)
    dias_validos = [d for d in [dias_checkin, dias_entreno] if d is not None]

    if not dias_validos:
        return "abandonando", "🔴"

    dias_min = min(dias_validos)

    if dias_min <= 3:
        return "cumpliendo", "✅"
    elif dias_min <= 7:
        return "flojo", "⚠️"
    else:
        return "abandonando", "🔴"


def _linea_alumno(atleta):
    """Arma la línea detallada de un alumno para el reporte."""
    nombre = str(atleta.get("nombre_completo", "Sin nombre")).strip()
    primer_nombre = nombre.split()[0] if nombre else "Alumno"

    dias_checkin = _dias_desde(atleta.get("ultimo_checkin"))
    dias_entreno = _dias_desde(atleta.get("ultimo_entrenamiento"))

    categoria, emoji = _clasificar_alumno(dias_checkin, dias_entreno)

    # Texto de actividad
    if dias_entreno is None:
        act_entreno = "sin entrenos"
    elif dias_entreno == 0:
        act_entreno = "entrenó hoy"
    elif dias_entreno == 1:
        act_entreno = "entrenó ayer"
    else:
        act_entreno = f"entrenó hace {dias_entreno}d"

    # Progreso de peso
    peso_actual = atleta.get("peso_actual")
    peso_objetivo = atleta.get("peso_objetivo")
    progreso_txt = ""
    try:
        if peso_actual and peso_objetivo:
            pa = float(peso_actual)
            po = float(peso_objetivo)
            falta = round(abs(pa - po), 1)
            progreso_txt = f" · {pa}kg→{po}kg (faltan {falta})"
    except Exception:
        progreso_txt = ""

    return categoria, f"{emoji} {primer_nombre} — {act_entreno}{progreso_txt}"


def generar_reporte_de_entrenador(entrenador_id, alumnos):
    """Arma el texto completo del reporte para un entrenador."""
    cumpliendo = []
    flojos = []
    abandonando = []

    for atleta in alumnos:
        categoria, linea = _linea_alumno(atleta)
        if categoria == "cumpliendo":
            cumpliendo.append(linea)
        elif categoria == "flojo":
            flojos.append(linea)
        else:
            abandonando.append(linea)

    total = len(alumnos)
    hoy = datetime.now().strftime("%d/%m/%Y")

    partes = [
        f"📊 *REPORTE SEMANAL — Eddy PT*",
        f"_{hoy}_",
        f"",
        f"Tenés *{total}* alumnos activos esta semana.",
        f"",
    ]

    if cumpliendo:
        partes.append(f"✅ *CUMPLIENDO BIEN ({len(cumpliendo)})*")
        partes.extend(cumpliendo)
        partes.append("")

    if flojos:
        partes.append(f"⚠️ *FLOJOS ESTA SEMANA ({len(flojos)})*")
        partes.extend(flojos)
        partes.append("")

    if abandonando:
        partes.append(f"🔴 *POR ABANDONAR ({len(abandonando)})*")
        partes.extend(abandonando)
        partes.append("")
        partes.append("💡 _Conviene escribirles a los que están por abandonar antes de que se vayan._")

    if not (cumpliendo or flojos or abandonando):
        partes.append("Todavía no hay actividad registrada esta semana.")

    partes.append("")
    partes.append("_Team Eddy — Software Elite_")

    return "\n".join(partes)


def enviar_reportes_semanales():
    """
    Tarea principal: corre los domingos a las 20:00.
    Agrupa alumnos por entrenador y le manda a cada uno su reporte
    al WhatsApp comercial (de roles_staff).
    """
    logger.info("📊 Generando reportes semanales para entrenadores...")

    # 1. Traer todos los alumnos
    try:
        resp = supabase.table("perfiles_atletas").select("*").execute()
        atletas = resp.data if resp.data else []
    except Exception as e:
        logger.error(f"No pude leer perfiles para el reporte: {e}")
        return

    # 2. Traer el staff (entrenadores con su whatsapp comercial)
    try:
        resp_staff = supabase.table("roles_staff").select("*").execute()
        staff = resp_staff.data if resp_staff.data else []
    except Exception as e:
        logger.error(f"No pude leer roles_staff: {e}")
        return

    # Mapa: perfil_id del entrenador -> su whatsapp comercial
    wa_por_entrenador = {}
    for s in staff:
        if s.get("rol") in ("entrenador", "nutricionista"):
            wa_por_entrenador[s.get("perfil_id")] = str(s.get("whatsapp", "")).strip()

    # 3. Agrupar alumnos por entrenador
    alumnos_por_entrenador = {}
    for atleta in atletas:
        ent_id = atleta.get("entrenador_id")
        if not ent_id:
            continue
        alumnos_por_entrenador.setdefault(ent_id, []).append(atleta)

    # 4. Generar y enviar el reporte a cada entrenador
    enviados = 0
    for entrenador_id, alumnos in alumnos_por_entrenador.items():
        telefono_comercial = wa_por_entrenador.get(entrenador_id, "")

        if not telefono_comercial:
            logger.warning(f"Entrenador {str(entrenador_id)[:8]} sin WhatsApp comercial; se omite.")
            continue

        mensaje = generar_reporte_de_entrenador(entrenador_id, alumnos)

        instancia_nombre = f"coach_{str(entrenador_id)[:8]}"

        try:
            exito = enviar_mensaje_texto_evolution(
                nombre_instancia=instancia_nombre,
                alumno_id=entrenador_id,   # el destinatario es el propio entrenador
                entrenador_id=entrenador_id,
                telefono=telefono_comercial,
                mensaje=mensaje
            )
            if exito:
                enviados += 1
                logger.info(f"✅ Reporte enviado al entrenador {str(entrenador_id)[:8]} ({len(alumnos)} alumnos).")
            else:
                logger.warning(f"No se pudo enviar el reporte al entrenador {str(entrenador_id)[:8]}.")
        except Exception as e:
            logger.error(f"Error enviando reporte a {str(entrenador_id)[:8]}: {e}")

    logger.info(f"📊 Reportes semanales completados: {enviados} entrenadores notificados.")
    return enviados