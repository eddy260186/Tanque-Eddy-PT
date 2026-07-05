"""
GESTOR DE GRUPOS / CLASES (CrossFit y funcional)
Pantalla para que el entrenador:
  - Cree grupos (nombre, horario, nivel)
  - Vea sus grupos
  - Agregue / quite alumnos de cada grupo

Se usa en el panel del entrenador como una pestaña nueva.
"""

import streamlit as st
from database.conexion import supabase


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
            .select("id, nombre_completo, email")
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

            # --- Eliminar el grupo ---
            if st.button("🗑️ Eliminar este grupo", key=f"del_grupo_{grupo_id}"):
                try:
                    supabase.table("grupos").update({"activo": False})\
                        .eq("id", grupo_id).execute()
                    st.success("Grupo eliminado.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")