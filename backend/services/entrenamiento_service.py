import json
import re

import google.generativeai as genai

from config.settings import settings
from database.conexion import supabase
from utils.logger import obtener_logger

logger = obtener_logger("EntrenamientoService")

# =========================================================
# CONFIGURAR GEMINI
# =========================================================

modelo_extractor = None

if settings.GEMINI_API_KEY:

    try:

        genai.configure(
            api_key=settings.GEMINI_API_KEY
        )

        modelo_extractor = genai.GenerativeModel(
            "gemini-2.5-flash"
        )

        logger.info("✅ Extractor Gemini configurado.")

    except Exception as e:

        logger.error(
            f"❌ Error configurando extractor: {str(e)}"
        )

else:

    logger.warning("⚠️ GEMINI_API_KEY no encontrada.")

# =========================================================
# EXTRAER EJERCICIOS DEL MENSAJE
# =========================================================

def extraer_ejercicios_con_ia(
    mensaje_alumno: str
):

    """
    Convierte un mensaje libre del alumno en
    datos estructurados de entrenamiento.

    Entrada:
        "Hice sentadilla 60kg 4x10 y prensa 100kg 3x12"

    Salida:
        [
            {
                "ejercicio": "Sentadilla",
                "grupo_muscular": "Piernas",
                "peso": 60,
                "series": 4,
                "repeticiones": 10,
                "observaciones": null
            },
            ...
        ]
    """

    try:

        if modelo_extractor is None:

            logger.warning(
                "⚠️ Extractor no disponible."
            )

            return []

        prompt = f"""
Sos un extractor de datos de entrenamiento.

Analizá el siguiente mensaje de un alumno de gimnasio
y extraé TODOS los ejercicios que menciona.

REGLAS:

- Respondé SOLAMENTE con un array JSON válido.
- Sin explicaciones, sin markdown, sin ```json.
- Si no hay ejercicios concretos, respondé: []
- Campos por ejercicio:
  - ejercicio (string, nombre normalizado)
  - grupo_muscular (string o null:
    Piernas, Pecho, Espalda, Hombros,
    Brazos, Core, Cardio)
  - peso (number o null, en kg)
  - series (number o null)
  - repeticiones (number o null)
  - observaciones (string o null,
    cómo se sintió o detalles extra)

EJEMPLO:

Mensaje: "hice sentadilla 60kg 4x10, me sentí fuerte"

Respuesta:
[{{"ejercicio": "Sentadilla", "grupo_muscular": "Piernas", "peso": 60, "series": 4, "repeticiones": 10, "observaciones": "se sintió fuerte"}}]

MENSAJE DEL ALUMNO:
{mensaje_alumno}
"""

        response = modelo_extractor.generate_content(
            prompt
        )

        texto = (response.text or "").strip()

        # Limpiar posibles fences de markdown
        texto = re.sub(
            r"^```(?:json)?|```$",
            "",
            texto,
            flags=re.MULTILINE
        ).strip()

        ejercicios = json.loads(texto)

        if not isinstance(ejercicios, list):

            return []

        logger.info(
            f"🏋️ Ejercicios extraídos: {len(ejercicios)}"
        )

        return ejercicios

    except json.JSONDecodeError:

        logger.warning(
            "⚠️ La IA no devolvió JSON válido."
        )

        return []

    except Exception as e:

        logger.error(
            f"❌ Error extrayendo ejercicios: {str(e)}"
        )

        return []

# =========================================================
# GUARDAR ENTRENAMIENTO ESTRUCTURADO
# =========================================================

def guardar_entrenamiento_estructurado(
    alumno_id: str,
    mensaje_alumno: str
):

    """
    Extrae los ejercicios del mensaje con IA
    y los guarda en ejercicios_realizados
    (tu tabla existente).

    Devuelve la cantidad de ejercicios guardados.
    """

    try:

        ejercicios = extraer_ejercicios_con_ia(
            mensaje_alumno
        )

        if not ejercicios:

            return 0

        filas = []

        for ej in ejercicios:

            filas.append({
                "alumno_id": alumno_id,
                "ejercicio": ej.get("ejercicio") or "Desconocido",
                "grupo_muscular": ej.get("grupo_muscular"),
                "peso": ej.get("peso"),
                "series": ej.get("series"),
                "repeticiones": ej.get("repeticiones"),
                "observaciones": ej.get("observaciones"),
                "mensaje_original": mensaje_alumno
            })

        supabase.table(
            "ejercicios_realizados"
        ).insert(
            filas
        ).execute()

        # Actualizar fecha de último entrenamiento
        # en el perfil del alumno
        supabase.table(
            "perfiles_atletas"
        ).update({
            "ultimo_entrenamiento": "now()"
        }).eq(
            "id",
            alumno_id
        ).execute()

        logger.info(
            f"✅ {len(filas)} ejercicios guardados "
            f"para alumno {alumno_id}"
        )

        return len(filas)

    except Exception as e:

        logger.error(
            f"❌ Error guardando entrenamiento: {str(e)}"
        )

        return 0

# =========================================================
# OBTENER HISTORIAL DE ENTRENAMIENTOS
# =========================================================

def obtener_historial_entrenamientos(
    alumno_id: str,
    limite: int = 15
):

    """
    Devuelve los últimos ejercicios registrados
    como texto, listo para inyectar al prompt
    de la IA conversacional.
    """

    try:

        res = (
            supabase
            .table("ejercicios_realizados")
            .select(
                "fecha, ejercicio, grupo_muscular, "
                "peso, series, repeticiones, observaciones"
            )
            .eq("alumno_id", alumno_id)
            .order("fecha", desc=True)
            .limit(limite)
            .execute()
        )

        if not res.data:

            return "Sin entrenamientos registrados todavía."

        lineas = []

        for r in res.data:

            fecha = str(
                r.get("fecha") or ""
            )[:10]

            partes = [
                fecha,
                r.get("ejercicio", "")
            ]

            if r.get("peso") is not None:
                partes.append(f"{r['peso']}kg")

            if r.get("series") and r.get("repeticiones"):
                partes.append(
                    f"{r['series']}x{r['repeticiones']}"
                )

            if r.get("observaciones"):
                partes.append(
                    f"({r['observaciones']})"
                )

            lineas.append(" - ".join(partes))

        return "\n".join(lineas)

    except Exception as e:

        logger.error(
            f"❌ Error obteniendo historial: {str(e)}"
        )

        return "Sin datos de entrenamiento."