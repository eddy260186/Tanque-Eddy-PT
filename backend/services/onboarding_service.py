"""
ONBOARDING SERVICE
Cuando el alumno completa sus datos por primera vez,
genera automaticamente su plan inicial desde LA BASE
DE DATOS PROPIA (data/alimentos.py + data/ejercicios.py)
y lo persiste en:

- rutinas_programadas   (rutina semanal dia por dia)
- comidas_programadas   (dieta con horarios)

Asi el agente diario funciona desde el dia 1, con o
sin IA. La IA es solo el mensajero: la fuente de
verdad es la base de datos.

Por defecto NO pisa lo que el entrenador ya cargo
(solo genera si el alumno no tiene nada).
"""

import re
from datetime import datetime, timedelta

from database.conexion import supabase
from utils.logger import obtener_logger
from backend.services.plan_service import (
    generar_menu_dinamico,
    generar_rutina_entrenamiento
)

logger = obtener_logger("OnboardingService")

# Distribucion de dias de entreno en la semana
MAPA_DIAS = {
    1: ["lunes"],
    2: ["lunes", "jueves"],
    3: ["lunes", "miercoles", "viernes"],
    4: ["lunes", "martes", "jueves", "viernes"],
    5: ["lunes", "martes", "miercoles", "jueves", "viernes"],
    6: ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado"],
    7: ["lunes", "martes", "miercoles", "jueves",
        "viernes", "sabado", "domingo"]
}

# Mapa: nombre de comida del generador → tipo + hora por defecto
MAPA_COMIDAS = {
    "COMIDA ÚNICA": ("almuerzo", "13:00"),
    "COMIDA UNICA": ("almuerzo", "13:00"),
    "DESAYUNO": ("desayuno", None),       # despertar + 1h
    "MEDIA MAÑANA": ("colacion", None),   # despertar + 3.5h
    "ALMUERZO": ("almuerzo", "13:00"),
    "MERIENDA": ("merienda", "16:30"),
    "PRE-CENA": ("pre_cena", "19:30"),
    "CENA": ("cena", "21:00")
}


def _parsear_ejercicio(texto: str):

    """
    Convierte un string de la BD de ejercicios en
    un dict estructurado.

    "Press banca 4x12"  → {nombre, series: 4, repeticiones: 12}
    "Plancha 3 series"  → {nombre: "Plancha 3 series"}
    """

    texto = str(texto).strip().lstrip("•-– ").strip()

    match = re.search(
        r"(\d+)\s*[xX]\s*(\d+)",
        texto
    )

    if match:

        nombre = texto[:match.start()].strip(" :·-")

        return {
            "nombre": nombre or texto,
            "series": int(match.group(1)),
            "repeticiones": int(match.group(2))
        }

    return {"nombre": texto}


def _sumar_horas(hora_base: str, horas: float):

    try:

        base = datetime.strptime(
            str(hora_base)[:5],
            "%H:%M"
        )

        return (
            base + timedelta(hours=horas)
        ).strftime("%H:%M")

    except Exception:

        return "08:00"


# =========================================================
# GENERAR Y GUARDAR RUTINA SEMANAL
# =========================================================

def generar_rutina_inicial(
    alumno_id: str,
    tipo_entreno: str,
    nivel_experiencia: str,
    dias_entreno: int,
    solo_si_vacio: bool = True
):

    """
    Genera la rutina semanal desde data/ejercicios.py
    y la guarda en rutinas_programadas.

    Devuelve cantidad de dias creados.
    """

    try:

        # No pisar trabajo del entrenador
        if solo_si_vacio:

            existentes = (
                supabase
                .table("rutinas_programadas")
                .select("id")
                .eq("alumno_id", alumno_id)
                .limit(1)
                .execute()
            )

            if existentes.data:

                logger.info(
                    "⏭️ El alumno ya tiene rutinas, "
                    "no se genera plan inicial."
                )

                return 0

        bloques = generar_rutina_entrenamiento(
            tipo_entreno,
            nivel_experiencia,
            dias_entreno
        )

        if not bloques or "Aviso" in bloques:

            logger.warning(
                "⚠️ Sin rutina en la BD para esa "
                "disciplina/nivel."
            )

            return 0

        dias = MAPA_DIAS.get(
            max(1, min(7, int(dias_entreno or 3)))
        )

        filas = []

        for i, (titulo, ejercicios) in enumerate(
            bloques.items()
        ):

            if i >= len(dias):
                break

            ejercicios_json = [
                _parsear_ejercicio(e)
                for e in ejercicios
                if str(e).strip()
            ]

            filas.append({
                "alumno_id": alumno_id,
                "dia_semana": dias[i],
                "grupo_muscular": str(titulo).strip(),
                "objetivo": nivel_experiencia,
                "duracion_minutos": 60,
                "ejercicios": ejercicios_json,
                "activa": True
            })

        if filas:

            supabase.table(
                "rutinas_programadas"
            ).insert(filas).execute()

        logger.info(
            f"✅ Rutina inicial generada: "
            f"{len(filas)} días."
        )

        return len(filas)

    except Exception as e:

        logger.error(
            f"❌ Error generando rutina inicial: {str(e)}"
        )

        return 0


# =========================================================
# GENERAR Y GUARDAR PLAN DE COMIDAS
# =========================================================

def generar_comidas_iniciales(
    alumno_id: str,
    p_g_total: float,
    c_g_total: float,
    g_g_total: float,
    num_comidas: int,
    dieta_tipo: str,
    pais: str,
    cal_objetivo: float,
    hora_despertar: str = "06:30",
    num_opciones: int = 3,
    solo_si_vacio: bool = True
):

    """
    Genera el plan de comidas desde data/alimentos.py
    (segun tipo de dieta) y lo guarda en
    comidas_programadas con horarios reales.

    Devuelve cantidad de comidas creadas.
    """

    try:

        if solo_si_vacio:

            existentes = (
                supabase
                .table("comidas_programadas")
                .select("id")
                .eq("alumno_id", alumno_id)
                .limit(1)
                .execute()
            )

            if existentes.data:

                logger.info(
                    "⏭️ El alumno ya tiene comidas, "
                    "no se genera plan inicial."
                )

                return 0

        num_opciones = max(1, min(10, int(num_opciones or 3)))

        menus, lista_compras = generar_menu_dinamico(
            p_g_total,
            c_g_total,
            g_g_total,
            num_comidas,
            num_opciones,
            dieta_tipo,
            pais
        )

        if not menus:
            return 0

        # Guardar la lista de compras mensual del alumno
        try:
            _guardar_lista_compras(alumno_id, lista_compras)
        except Exception as e:
            logger.warning(
                f"⚠️ No pude guardar lista de compras: {str(e)}"
            )

        kcal_por_comida = int(
            (cal_objetivo or 0) / max(1, num_comidas)
        ) or None

        filas = []

        for nombre_comida, opciones in menus.items():

            tipo, hora = MAPA_COMIDAS.get(
                nombre_comida.upper().strip(),
                ("colacion", "11:00")
            )

            # Horas relativas al despertar
            if hora is None:

                if tipo == "desayuno":
                    hora = _sumar_horas(hora_despertar, 1)
                else:
                    hora = _sumar_horas(hora_despertar, 3.5)

            import re as _re

            opciones_limpias = [
                _re.sub(r"^Opcion \d+: ", "", str(op)).strip()
                for op in (opciones or [])
                if str(op).strip()
            ]

            if not opciones_limpias:
                continue

            filas.append({
                "alumno_id": alumno_id,
                "tipo_comida": tipo,
                "hora": hora,
                "dia_semana": None,   # todos los dias
                "detalle": opciones_limpias[0],
                "opciones": opciones_limpias,
                "kcal": kcal_por_comida,
                "activa": True
            })

        if filas:

            supabase.table(
                "comidas_programadas"
            ).insert(filas).execute()

        logger.info(
            f"✅ Plan de comidas inicial generado: "
            f"{len(filas)} comidas."
        )

        return len(filas)

    except Exception as e:

        logger.error(
            f"❌ Error generando comidas: {str(e)}"
        )

        return 0


# =========================================================
# LISTA DE COMPRAS MENSUAL
# =========================================================

def _guardar_lista_compras(
    alumno_id: str,
    lista_compras: dict
):

    """
    Convierte el dict {alimento: gramos/30 dias} en
    texto legible y lo guarda en listas_compras.
    """

    if not lista_compras:
        return

    lineas = []

    for alimento, cantidad in sorted(
        lista_compras.items()
    ):

        try:
            cantidad = float(cantidad)
        except Exception:
            continue

        if cantidad >= 1000:
            lineas.append(
                f"• {alimento}: {round(cantidad / 1000, 1)} kg"
            )
        elif cantidad >= 50:
            lineas.append(
                f"• {alimento}: {int(round(cantidad))} g"
            )
        else:
            lineas.append(
                f"• {alimento}: {int(round(cantidad))} unidades/porciones"
            )

    if not lineas:
        return

    detalle = "\n".join(lineas)

    # Desactivar listas anteriores
    supabase.table(
        "listas_compras"
    ).update({
        "activa": False
    }).eq(
        "alumno_id", alumno_id
    ).execute()

    supabase.table(
        "listas_compras"
    ).insert({
        "alumno_id": alumno_id,
        "detalle": detalle,
        "activa": True
    }).execute()

    logger.info(
        f"🛒 Lista de compras guardada "
        f"({len(lineas)} items)."
    )


# =========================================================
# ORQUESTADOR COMPLETO
# =========================================================

def generar_plan_inicial_completo(
    alumno_id: str,
    tipo_entreno: str,
    nivel_experiencia: str,
    dias_entreno: int,
    p_g_total: float,
    c_g_total: float,
    g_g_total: float,
    num_comidas: int,
    dieta_tipo: str,
    pais: str,
    cal_objetivo: float,
    hora_despertar: str = "06:30",
    num_opciones: int = 3
):

    """
    Punto de entrada unico desde el panel del alumno.
    Genera rutina + comidas desde la BD propia
    (solo si el alumno no tiene nada cargado).

    Devuelve (dias_rutina, comidas) creados.
    """

    dias_creados = generar_rutina_inicial(
        alumno_id,
        tipo_entreno,
        nivel_experiencia,
        dias_entreno
    )

    comidas_creadas = generar_comidas_iniciales(
        alumno_id,
        p_g_total,
        c_g_total,
        g_g_total,
        num_comidas,
        dieta_tipo,
        pais,
        cal_objetivo,
        hora_despertar,
        num_opciones
    )

    return dias_creados, comidas_creadas