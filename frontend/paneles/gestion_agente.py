"""
GESTION DEL AGENTE DIARIO (panel del entrenador)

Pestanias para administrar, por alumno:
- Rutina semanal     → tabla rutinas_programadas
- Plan de comidas    → tabla comidas_programadas
- Actividad          → ejercicios_realizados + checkins_diarios

Estas tablas alimentan los mensajes automaticos
de WhatsApp del agente diario.
"""

import streamlit as st
import pandas as pd
from datetime import time, datetime

from database.conexion import supabase
from utils.logger import obtener_logger
from automation.generador_automatizaciones import generar_automatizaciones_alumno

logger = obtener_logger("GestionAgente")

DIAS = [
    "lunes", "martes", "miercoles",
    "jueves", "viernes", "sabado", "domingo"
]

TIPOS_COMIDA = [
    "desayuno", "colacion", "almuerzo",
    "merienda", "cena", "post_entreno"
]


# =========================================================
# PESTANIA: RUTINA SEMANAL
# =========================================================

def tab_rutina_semanal(alumno_id: str):

    st.markdown(
        "<div class='seccion-titulo-vip'>"
        "📅 Rutina Semanal del Atleta</div>",
        unsafe_allow_html=True
    )

    st.caption(
        "Lo que cargues acá es lo que el agente le "
        "manda por WhatsApp el día que corresponde, "
        "con cada ejercicio, series y repeticiones."
    )

    # Cargar rutinas existentes
    try:

        res = (
            supabase
            .table("rutinas_programadas")
            .select("*")
            .eq("alumno_id", alumno_id)
            .execute()
        )

        rutinas = {
            str(r.get("dia_semana", "")).lower()
            .replace("é", "e").replace("á", "a"): r
            for r in (res.data or [])
        }

    except Exception as e:

        st.error(f"No pude cargar las rutinas: {e}")

        return

    # Vista resumen de la semana
    resumen = []

    for dia in DIAS:

        r = rutinas.get(dia)

        resumen.append({
            "Día": dia.capitalize(),
            "Grupo Muscular": (
                r.get("grupo_muscular") if r else "— Descanso —"
            ),
            "Ejercicios": (
                len(r.get("ejercicios") or []) if r else 0
            ),
            "Activa": "✅" if (r and r.get("activa")) else "—"
        })

    st.dataframe(
        resumen,
        use_container_width=True,
        hide_index=True
    )

    st.write("---")

    # Editor por dia
    dia_sel = st.selectbox(
        "✏️ Editar día:",
        DIAS,
        format_func=str.capitalize,
        key=f"dia_rutina_{alumno_id}"
    )

    rutina_actual = rutinas.get(dia_sel)

    col1, col2, col3 = st.columns(3)

    with col1:

        grupo = st.text_input(
            "Grupo muscular:",
            value=(
                rutina_actual.get("grupo_muscular")
                if rutina_actual else ""
            ),
            placeholder="Ej: Espalda y Bíceps",
            key=f"grupo_{alumno_id}_{dia_sel}"
        )

    with col2:

        objetivo = st.text_input(
            "Objetivo del día:",
            value=(
                rutina_actual.get("objetivo")
                if rutina_actual else ""
            ) or "",
            placeholder="Ej: Hipertrofia",
            key=f"obj_{alumno_id}_{dia_sel}"
        )

    with col3:

        duracion = st.number_input(
            "Duración (min):",
            min_value=0,
            max_value=240,
            value=int(
                rutina_actual.get("duracion_minutos") or 60
            ) if rutina_actual else 60,
            key=f"dur_{alumno_id}_{dia_sel}"
        )

    # Editor de ejercicios (tabla dinamica)
    st.markdown("**Ejercicios del día:**")

    ejercicios_existentes = (
        rutina_actual.get("ejercicios")
        if rutina_actual else []
    ) or []

    filas = []

    for ej in ejercicios_existentes:

        if isinstance(ej, dict):

            filas.append({
                "Ejercicio": ej.get("nombre")
                or ej.get("ejercicio") or "",
                "Series": int(ej.get("series") or 4),
                "Repeticiones": int(
                    ej.get("repeticiones")
                    or ej.get("reps") or 10
                )
            })

        elif isinstance(ej, str):

            filas.append({
                "Ejercicio": ej,
                "Series": 4,
                "Repeticiones": 10
            })

    if not filas:

        filas = [{
            "Ejercicio": "",
            "Series": 4,
            "Repeticiones": 12
        }]

    df_editado = st.data_editor(
        pd.DataFrame(filas),
        num_rows="dynamic",
        use_container_width=True,
        key=f"editor_{alumno_id}_{dia_sel}",
        column_config={
            "Ejercicio": st.column_config.TextColumn(
                "Ejercicio",
                width="large"
            ),
            "Series": st.column_config.NumberColumn(
                "Series",
                min_value=1,
                max_value=20
            ),
            "Repeticiones": st.column_config.NumberColumn(
                "Repeticiones",
                min_value=1,
                max_value=100
            )
        }
    )

    col_g1, col_g2 = st.columns(2)

    with col_g1:

        if st.button(
            f"💾 Guardar rutina del {dia_sel.capitalize()}",
            type="primary",
            use_container_width=True,
            key=f"save_rut_{alumno_id}_{dia_sel}"
        ):

            if not grupo.strip():

                st.error(
                    "Poné el grupo muscular antes de guardar."
                )

            else:

                ejercicios_json = []

                for _, fila in df_editado.iterrows():

                    nombre_ej = str(
                        fila.get("Ejercicio") or ""
                    ).strip()

                    if not nombre_ej:
                        continue

                    ejercicios_json.append({
                        "nombre": nombre_ej,
                        "series": int(fila.get("Series") or 4),
                        "repeticiones": int(
                            fila.get("Repeticiones") or 10
                        )
                    })

                datos = {
                    "alumno_id": alumno_id,
                    "dia_semana": dia_sel,
                    "grupo_muscular": grupo.strip(),
                    "objetivo": objetivo.strip() or None,
                    "duracion_minutos": int(duracion),
                    "ejercicios": ejercicios_json,
                    "activa": True
                }

                try:

                    if rutina_actual:

                        supabase.table(
                            "rutinas_programadas"
                        ).update(datos).eq(
                            "id",
                            rutina_actual["id"]
                        ).execute()

                    else:

                        supabase.table(
                            "rutinas_programadas"
                        ).insert(datos).execute()

                    st.success(
                        f"✅ Rutina del "
                        f"{dia_sel.capitalize()} guardada "
                        f"({len(ejercicios_json)} ejercicios)."
                    )

                    st.rerun()

                except Exception as e:

                    st.error(f"Error guardando: {e}")

    with col_g2:

        if rutina_actual and st.button(
            f"🗑️ Borrar rutina del {dia_sel.capitalize()}",
            use_container_width=True,
            key=f"del_rut_{alumno_id}_{dia_sel}"
        ):

            try:

                supabase.table(
                    "rutinas_programadas"
                ).delete().eq(
                    "id",
                    rutina_actual["id"]
                ).execute()

                st.success("Rutina eliminada.")

                st.rerun()

            except Exception as e:

                st.error(f"Error eliminando: {e}")


# =========================================================
# PESTANIA: PLAN DE COMIDAS
# =========================================================

def tab_plan_comidas(alumno_id: str):

    st.markdown(
        "<div class='seccion-titulo-vip'>"
        "🍽️ Plan de Comidas del Atleta</div>",
        unsafe_allow_html=True
    )

    st.caption(
        "Cada comida que cargues se le envía por "
        "WhatsApp a su hora, todos los días "
        "(o el día específico que elijas)."
    )

    # Cargar comidas existentes
    try:

        res = (
            supabase
            .table("comidas_programadas")
            .select("*")
            .eq("alumno_id", alumno_id)
            .order("hora")
            .execute()
        )

        comidas = res.data or []

    except Exception as e:

        st.error(f"No pude cargar las comidas: {e}")

        return

    # Listado actual
    if comidas:

        st.markdown("**Comidas programadas:**")

        for comida in comidas:

            col_c1, col_c2 = st.columns([5, 1])

            with col_c1:

                dia_txt = (
                    comida.get("dia_semana")
                    or "todos los días"
                )

                hora_txt = str(
                    comida.get("hora") or ""
                )[:5]

                kcal_txt = (
                    f" · {comida['kcal']} kcal"
                    if comida.get("kcal") else ""
                )

                estado = (
                    "🟢" if comida.get("activa") else "🔴"
                )

                st.markdown(
                    f"{estado} **{hora_txt}** — "
                    f"{str(comida.get('tipo_comida', '')).capitalize()} "
                    f"({dia_txt}){kcal_txt}\n\n"
                    f"&nbsp;&nbsp;&nbsp;&nbsp;"
                    f"{comida.get('detalle', '')}"
                )

            with col_c2:

                if st.button(
                    "🗑️",
                    key=f"del_com_{comida['id']}",
                    help="Eliminar esta comida"
                ):

                    try:

                        supabase.table(
                            "comidas_programadas"
                        ).delete().eq(
                            "id",
                            comida["id"]
                        ).execute()

                        # Regenerar horarios del agente
                        generar_automatizaciones_alumno(
                            alumno_id
                        )

                        st.rerun()

                    except Exception as e:

                        st.error(f"Error: {e}")

    else:

        st.info(
            "Este atleta todavía no tiene comidas "
            "programadas. Agregá la primera abajo. 👇"
        )

    st.write("---")

    # Formulario de alta
    st.markdown("**➕ Agregar comida:**")

    with st.form(
        key=f"form_comida_{alumno_id}",
        clear_on_submit=True
    ):

        col_f1, col_f2, col_f3 = st.columns(3)

        with col_f1:

            tipo_comida = st.selectbox(
                "Tipo:",
                TIPOS_COMIDA,
                format_func=lambda t:
                    t.replace("_", " ").capitalize()
            )

        with col_f2:

            hora_comida = st.time_input(
                "Hora:",
                value=time(8, 0)
            )

        with col_f3:

            dia_comida = st.selectbox(
                "Día:",
                ["todos"] + DIAS,
                format_func=lambda d:
                    "Todos los días" if d == "todos"
                    else d.capitalize()
            )

        detalle = st.text_area(
            "Detalle de la comida:",
            placeholder="Ej: 4 huevos, 100g avena, 1 banana"
        )

        kcal = st.number_input(
            "Calorías aproximadas (opcional):",
            min_value=0,
            max_value=5000,
            value=0
        )

        if st.form_submit_button(
            "💾 Agregar al plan",
            type="primary",
            use_container_width=True
        ):

            if not detalle.strip():

                st.error("Escribí el detalle de la comida.")

            else:

                try:

                    supabase.table(
                        "comidas_programadas"
                    ).insert({
                        "alumno_id": alumno_id,
                        "tipo_comida": tipo_comida,
                        "hora": hora_comida.strftime("%H:%M"),
                        "dia_semana": (
                            None if dia_comida == "todos"
                            else dia_comida
                        ),
                        "detalle": detalle.strip(),
                        "kcal": int(kcal) or None,
                        "activa": True
                    }).execute()

                    # Regenerar horarios del agente
                    generar_automatizaciones_alumno(
                        alumno_id
                    )

                    st.success(
                        "✅ Comida agregada. El agente ya "
                        "la incluye en el seguimiento diario."
                    )

                    st.rerun()

                except Exception as e:

                    st.error(f"Error guardando: {e}")


# =========================================================
# PESTANIA: ACTIVIDAD DEL ALUMNO
# =========================================================

def tab_actividad_alumno(alumno_id: str):

    st.markdown(
        "<div class='seccion-titulo-vip'>"
        "🏋️ Actividad Reportada por WhatsApp</div>",
        unsafe_allow_html=True
    )

    # Entrenamientos registrados
    st.markdown("**Últimos entrenamientos registrados:**")

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
            .limit(30)
            .execute()
        )

        entrenos = res.data or []

    except Exception:

        entrenos = []

    if entrenos:

        tabla = []

        for e in entrenos:

            tabla.append({
                "Fecha": str(e.get("fecha") or "")[:10],
                "Ejercicio": e.get("ejercicio"),
                "Grupo": e.get("grupo_muscular") or "—",
                "Peso (kg)": e.get("peso") or "—",
                "Series x Reps": (
                    f"{e['series']}x{e['repeticiones']}"
                    if e.get("series") and e.get("repeticiones")
                    else "—"
                ),
                "Obs.": e.get("observaciones") or ""
            })

        st.dataframe(
            tabla,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "Todavía no reportó entrenamientos por WhatsApp."
        )

    st.write("---")

    # Checkins nocturnos
    st.markdown("**Cumplimiento diario (checkin 22:00):**")

    try:

        res_ch = (
            supabase
            .table("checkins_diarios")
            .select("fecha, respuesta")
            .eq("alumno_id", alumno_id)
            .order("fecha", desc=True)
            .limit(14)
            .execute()
        )

        checkins = res_ch.data or []

    except Exception:

        checkins = []

    if checkins:

        emoji_map = {
            "si": "✅ Cumplió todo",
            "parcial": "🟡 Parcial",
            "no": "🔴 No pudo"
        }

        tabla_ch = [
            {
                "Fecha": str(ch.get("fecha") or "")[:10],
                "Resultado": emoji_map.get(
                    ch.get("respuesta"),
                    ch.get("respuesta") or "—"
                )
            }
            for ch in checkins
        ]

        st.dataframe(
            tabla_ch,
            use_container_width=True,
            hide_index=True
        )

        # Tasa de cumplimiento
        total = len(checkins)

        cumplio = len([
            c for c in checkins
            if c.get("respuesta") == "si"
        ])

        st.metric(
            "Tasa de cumplimiento (últimos 14 días)",
            f"{round(cumplio / total * 100)}%"
        )

    else:

        st.info(
            "Todavía no respondió ningún checkin nocturno."
        )