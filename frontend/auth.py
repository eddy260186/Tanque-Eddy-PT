import streamlit as st
import datetime as dt
from database.conexion import supabase

def renderizar_login():
    if "usuario_actual" in st.session_state and "rol" in st.session_state:
        c1, c2 = st.columns([4, 1])
        with c1:
            st.info(f"👤 Sesión activa: **{st.session_state['usuario_actual']}** | Rango: 👑 **{st.session_state['rol'].upper()}**")
        with c2:
            if st.button("🚪 Cerrar Sesión", use_container_width=True):
                st.session_state.clear()
                st.rerun()
        return True 

    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 20px; background-color: rgba(20,20,20,0.8); border: 1px solid #d4af37; border-radius: 10px;">
            <h2 style="color: #d4af37;">🔐 Acceso Elite</h2>
            <p style="color: #ccc;">Ingresa tu correo para acceder a tu panel de control.</p>
        </div>
        """, unsafe_allow_html=True)
        
        email_input = st.text_input("✉️ Correo Electrónico", placeholder="atleta@email.com", label_visibility="collapsed")
        
        if st.button("🚀 INGRESAR AL SISTEMA", type="primary", use_container_width=True):
            if email_input:
                email_limpio = email_input.lower().strip()
                with st.spinner("Verificando credenciales..."):
                    try:
                        res = supabase.table("perfiles_atletas").select("*").eq("email", email_limpio).execute()
                        if len(res.data) > 0:
                            usuario = res.data[0]
                            st.session_state["usuario_actual"] = usuario["email"]
                            st.session_state["perfil_id"] = usuario["id"]
                            st.session_state["rol"] = usuario.get("rol", "alumno") 
                            st.rerun()
                        else:
                            nuevo_usuario = {"email": email_limpio, "rol": "alumno"}
                            res_insert = supabase.table("perfiles_atletas").insert(nuevo_usuario).execute()
                            if len(res_insert.data) > 0:
                                usuario_nuevo = res_insert.data[0]
                                st.session_state["usuario_actual"] = usuario_nuevo["email"]
                                st.session_state["perfil_id"] = usuario_nuevo["id"]
                                st.session_state["rol"] = "alumno"
                                st.success("✅ Cuenta creada con éxito. Entrando al sistema...")
                                st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error al conectar con el servidor: {e}")
            else:
                st.warning("⚠️ Por favor, escribe un correo válido.")
                
    return False