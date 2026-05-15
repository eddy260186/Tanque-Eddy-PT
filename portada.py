# --- LOGO DE PORTADA (logo_tanque) ---
    col1, col_logo, col3 = st.columns([1, 1, 1]) 
    with col_logo:
        import os
        directorio_script = os.path.dirname(os.path.abspath(__file__))
        
        # Buscamos específicamente el logo de portada que me indicaste
        nombres_portada = ["logo_tanque.png", "logo_tanque(1).png", "logo_tanque"]
        foto_portada = None
        
        for nombre in nombres_portada:
            ruta_test = os.path.join(directorio_script, nombre)
            if os.path.exists(ruta_test):
                foto_portada = ruta_test
                break
        
        if foto_portada:
            try:
                st.image(foto_portada, use_container_width=True)
            except Exception:
                pass
        else:
            st.error(f"⚠️ No se encontró '{nombres_portada[0]}' en la carpeta del servidor")
