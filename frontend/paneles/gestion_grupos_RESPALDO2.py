"""
GESTOR DE GRUPOS / CLASES (CrossFit y funcional)
Pantalla para que el entrenador:
  - Cree grupos (nombre, horario, nivel)
  - Vea sus grupos
  - Agregue / quite alumnos de cada grupo

Se usa en el panel del entrenador como una pestaña nueva.
"""

import streamlit as st
from datetime import datetime
from database.conexion import supabase

# Envío por WhatsApp (para mandar el WOD a los alumnos del grupo)
try:
    from backend.services.whatsapp_service import enviar_mensaje_texto_evolution
except Exception:
    enviar_mensaje_texto_evolution = None

DIAS_SEMANA = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]


# =========================================================
# LECTURA DE DATOS
# =========================================================

def _obtener_grupos(entrenador_id: str):
    """Devuelve los grupos activos de este entrenador."""
    try:
        res = (
            supabase
            .table("grupos")
            .select("*")
            .eq("entrenador_id", entrenador_id)
            .eq("activo", True)
            .order("fecha_creado", desc=True)
            .execute()
        )
        return res.data or []
    except Exception as e:
        st.error(f"No se pudieron cargar los grupos: {e}")
        return []


def _obtener_alumnos_del_entrenador(entrenador_id: str):
    """Devuelve los alumnos vinculados a este entrenador."""
    try:
        res = (
            supabase
            .table("perfiles_atletas")
            .select("id, nombre_completo, email, telefono")
            .eq("entrenador_id", entrenador_id)
            .execute()
        )
        return res.data or []
    except Exception:
        return []


def _obtener_miembros(grupo_id: str):
    """Devuelve los alumno_id que están en un grupo."""
    try:
        res = (
            supabase
            .table("grupos_miembros")
            .select("alumno_id")
            .eq("grupo_id", grupo_id)
            .execute()
        )
        return [m["alumno_id"] for m in (res.data or [])]
    except Exception:
        return []


# =========================================================
# PANTALLA PRINCIPAL
# =========================================================


# =========================================================
# CARGAR WOD Y ENVIARLO A TODO EL GRUPO
# =========================================================

def _enviar_wod_al_grupo(entrenador_id, grupo, miembros_ids, dict_alumnos_full, dia_sel, nombre_wod, texto_wod):
    """
    Guarda el WOD como rutina de cada alumno del grupo y se lo
    manda por WhatsApp. Devuelve (guardados, enviados).
    """
    # Convertir el texto en lista de bloques (una línea por bloque)
    ejercicios_json = [linea.strip() for linea in texto_wod.split("\n") if linea.strip()]

    guardados = 0
    enviados = 0

    instancia_nombre = f"coach_{str(entrenador_id)[:8]}"

    # Armar el mensaje de WhatsApp (con iconos)
    mensaje_wa = "━━━━━━━━━━━━━━━\n"
    mensaje_wa += f"🏋️ *{nombre_wod.upper()}*\n"
    mensaje_wa += f"📅 {dia_sel.capitalize()}\n"
    mensaje_wa += "━━━━━━━━━━━━━━━\n\n"
    mensaje_wa += texto_wod.strip()
    mensaje_wa += "\n\n👊 _Dale con todo, equipo!_"

    for aid in miembros_ids:

        alumno = dict_alumnos_full.get(aid, {})

        # 1. Guardar el WOD como rutina del alumno para ese día
        try:
            datos = {
                "alumno_id": aid,
                "dia_semana": dia_sel,
                "grupo_muscular": nombre_wod.strip(),
                "ejercicios": ejercicios_json,
                "activa": True
            }
            # Buscar si ya tiene rutina ese día
            existente = (
                supabase.table("rutinas_programadas")
                .select("id")
                .eq("alumno_id", aid)
                .eq("dia_semana", dia_sel)
                .execute()
            )
            if existente.data:
                supabase.table("rutinas_programadas").update(datos)\
                    .eq("id", existente.data[0]["id"]).execute()
            else:
                supabase.table("rutinas_programadas").insert(datos).execute()
            guardados += 1
        except Exception:
            pass

        # 2. Enviar por WhatsApp
        telefono = str(alumno.get("telefono", "")).strip()
        if telefono and enviar_mensaje_texto_evolution is not None:
            try:
                enviar_mensaje_texto_evolution(
                    nombre_instancia=instancia_nombre,
                    alumno_id=aid,
                    entrenador_id=entrenador_id,
                    telefono=telefono,
                    mensaje=mensaje_wa
                )
                enviados += 1
            except Exception:
                pass

    return guardados, enviados


def tab_gestion_grupos(entrenador_id: str):
    """
    Pestaña de gestión de grupos para el panel del entrenador.
    """

    st.subheader("👥 Mis Grupos / Clases")
    st.caption(
        "Armá grupos (por clase y nivel) para mandar un WOD a todos "
        "de una vez. Ideal para CrossFit y funcional."
    )

    # =====================================================
    # CREAR UN GRUPO NUEVO
    # =====================================================
    with st.expander("➕ Crear un grupo nuevo"):

        col_n, col_h = st.columns(2)
        with col_n:
            nombre_grupo = st.text_input(
                "Nombre del grupo",
                placeholder="Ej: CrossFit Tarde",
                key="nuevo_grupo_nombre"
            )
        with col_h:
            horario_grupo = st.text_input(
                "Horario",
                placeholder="Ej: Lun y Mié 18:00",
                key="nuevo_grupo_horario"
            )

        nivel_grupo = st.selectbox(
            "Nivel",
            ["Mixto", "Principiante", "Intermedio", "Avanzado"],
            key="nuevo_grupo_nivel"
        )

        if st.button("✅ Crear grupo", type="primary", use_container_width=True,
                     key="btn_crear_grupo"):
            if not nombre_grupo.strip():
                st.error("Poné un nombre al grupo.")
            else:
                try:
                    supabase.table("grupos").insert({
                        "entrenador_id": entrenador_id,
                        "nombre": nombre_grupo.strip(),
                        "horario": horario_grupo.strip() or None,
                        "nivel": nivel_grupo,
                    }).execute()
                    st.success(f"✅ Grupo '{nombre_grupo}' creado.")
                    st.rerun()
                except Exception as e:
                    st.error(f"No se pudo crear el grupo: {e}")

    st.divider()

    # =====================================================
    # LISTA DE GRUPOS EXISTENTES
    # =====================================================
    grupos = _obtener_grupos(entrenador_id)

    if not grupos:
        st.info("Todavía no tenés grupos. Creá el primero arriba ☝️")
        return

    alumnos = _obtener_alumnos_del_entrenador(entrenador_id)
    dict_alumnos = {a["id"]: a.get("nombre_completo", "Sin nombre") for a in alumnos}
    dict_alumnos_full = {a["id"]: a for a in alumnos}

    for grupo in grupos:

        grupo_id = grupo["id"]
        miembros_ids = _obtener_miembros(grupo_id)

        titulo = grupo.get("nombre", "Grupo")
        if grupo.get("horario"):
            titulo += f" · {grupo['horario']}"
        if grupo.get("nivel"):
            titulo += f" · {grupo['nivel']}"

        with st.expander(f"🏋️ {titulo}  ({len(miembros_ids)} alumnos)"):

            # --- Alumnos actuales del grupo ---
            st.markdown("**Alumnos en este grupo:**")
            if miembros_ids:
                for aid in miembros_ids:
                    nombre = dict_alumnos.get(aid, "Alumno")
                    col_nom, col_quitar = st.columns([4, 1])
                    with col_nom:
                        st.write(f"• {nombre}")
                    with col_quitar:
                        if st.button("Quitar", key=f"quitar_{grupo_id}_{aid}"):
                            try:
                                supabase.table("grupos_miembros").delete()\
                                    .eq("grupo_id", grupo_id)\
                                    .eq("alumno_id", aid).execute()
                                st.success("Alumno quitado.")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error: {e}")
            else:
                st.caption("Este grupo todavía no tiene alumnos.")

            st.divider()

            # --- Agregar alumnos al grupo ---
            st.markdown("**Agregar alumnos:**")
            disponibles = {
                a["id"]: dict_alumnos[a["id"]]
                for a in alumnos
                if a["id"] not in miembros_ids
            }

            if disponibles:
                seleccionados = st.multiselect(
                    "Elegí alumnos para sumar al grupo",
                    options=list(disponibles.keys()),
                    format_func=lambda x: disponibles.get(x, "Alumno"),
                    key=f"multiselect_{grupo_id}"
                )

                if st.button("➕ Agregar al grupo", key=f"agregar_{grupo_id}",
                             use_container_width=True):
                    if seleccionados:
                        try:
                            filas = [
                                {"grupo_id": grupo_id, "alumno_id": aid}
                                for aid in seleccionados
                            ]
                            supabase.table("grupos_miembros").insert(filas).execute()
                            st.success(f"✅ {len(seleccionados)} alumno(s) agregado(s).")
                            st.rerun()
                        except Exception as e:
                            st.error(f"No se pudieron agregar: {e}")
                    else:
                        st.warning("Elegí al menos un alumno.")
            else:
                st.caption("Todos tus alumnos ya están en este grupo.")

            st.divider()

            # --- CARGAR WOD Y ENVIAR A TODO EL GRUPO ---
            st.markdown("**🏋️ Cargar entrenamiento (WOD) para todo el grupo:**")

            if not miembros_ids:
                st.caption("Agregá alumnos al grupo antes de mandar un WOD.")
            else:
                col_dia, col_nom = st.columns(2)
                with col_dia:
                    dia_wod = st.selectbox(
                        "Día",
                        DIAS_SEMANA,
                        format_func=lambda x: x.capitalize(),
                        key=f"dia_wod_{grupo_id}"
                    )
                with col_nom:
                    nombre_wod = st.text_input(
                        "Nombre del WOD",
                        value="WOD del día",
                        key=f"nombre_wod_{grupo_id}"
                    )

                texto_wod = st.text_area(
                    "Entrenamiento (escribí libre, como CrossFit):",
                    height=200,
                    placeholder=(
                        "Ej:\n"
                        "🔥 Calentamiento\n"
                        "Remo 500m suave\n\n"
                        "💪 Fuerza\n"
                        "Back Squat 5x5\n\n"
                        "⏱️ WOD 'For Time' (15 min)\n"
                        "40 cal Remo\n"
                        "30 Toes to Bar\n"
                        "20 Clean & Jerks (80/55kg)"
                    ),
                    key=f"texto_wod_{grupo_id}"
                )

                if st.button(
                    f"📤 Enviar WOD a los {len(miembros_ids)} alumnos del grupo",
                    type="primary",
                    use_container_width=True,
                    key=f"enviar_wod_{grupo_id}"
                ):
                    if not texto_wod.strip():
                        st.error("Escribí el entrenamiento antes de enviar.")
                    else:
                        with st.spinner("Guardando y enviando el WOD al grupo..."):
                            guardados, enviados = _enviar_wod_al_grupo(
                                entrenador_id, grupo, miembros_ids,
                                dict_alumnos_full, dia_wod, nombre_wod, texto_wod
                            )
                        st.success(
                            f"✅ WOD cargado a {guardados} alumnos "
                            f"y enviado por WhatsApp a {enviados}."
                        )

            st.divider()

            # --- Eliminar el grupo ---
            if st.button("🗑️ Eliminar este grupo", key=f"del_grupo_{grupo_id}"):
                try:
                    supabase.table("grupos").update({"activo": False})\
                        .eq("id", grupo_id).execute()
                    st.success("Grupo eliminado.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")