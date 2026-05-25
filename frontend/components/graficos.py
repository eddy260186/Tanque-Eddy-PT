import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, date
from database.conexion import supabase

def renderizar_grafico_macros_sidebar(p_g_total: float, c_g_total: float, g_g_total: float):
    """
    Renderiza el gráfico de dona VIP tricolor en el sidebar con efecto de brillo.
    """
    st.sidebar.markdown("""
    <style>
    @keyframes eliteGlow {
        0% { filter: drop-shadow(0 0 5px rgba(255,215,0,0.4)); }
        100% { filter: drop-shadow(0 0 15px rgba(0,255,150,0.8)); }
    }
    </style>
    <h2 style="text-align:center; background:linear-gradient(90deg, #ffd700, #ffffff, #00ff95); -webkit-background-clip:text; -webkit-text-fill-color:transparent; font-weight:900; font-size:28px; margin-top:10px; margin-bottom:-10px; letter-spacing:1px; animation: eliteGlow 2s infinite alternate;">
    ⚡ AI Elite Macros
    </h2>
    <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,215,0,0.18); padding:10px; border-radius:24px; backdrop-filter:blur(14px); box-shadow:0 0 35px rgba(0,0,0,0.35); margin-bottom: 15px;">
    """, unsafe_allow_html=True)

    labels = ['Proteínas', 'Carbohidratos', 'Grasas']
    valores = [int(round(p_g_total)), int(round(c_g_total)), int(round(g_g_total))]
    colores_vip = ['#00d9ff', '#00ff95', '#ffd700']

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=valores,
        hole=0.52,
        sort=False,
        direction='clockwise',
        marker=dict(colors=colores_vip, line=dict(color='rgba(255,255,255,0.18)', width=3)),
        texttemplate="<b>%{value} g</b><br>%%{label}",
        textposition='inside',
        insidetextorientation='horizontal',
        textfont=dict(family='Poppins, Arial', size=13, color='black'),
        hovertemplate="<b>%{label}</b><br>%{value} g<br>%{percent}",
        pull=[0.02, 0.02, 0.02]
    )])

    fig.update_layout(
        height=380, margin=dict(t=20, b=20, l=10, r=10),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        annotations=[dict(text="<b style='font-size:30px'>AI</b><br><span style='font-size:16px;color:#d4af37'>MACROS</span>", x=0.5, y=0.5, showarrow=False, font=dict(family='Poppins, Arial', color='#ffffff'))]
    )
    fig.update_traces(rotation=90, hoverlabel=dict(bgcolor="#111111", bordercolor="#d4af37", font_size=15, font_family="Poppins, Arial"))
    
    st.sidebar.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.sidebar.markdown("</div>", unsafe_allow_html=True)


def renderizar_grafico_proyeccion(fechas_reales: list, pesos_prog: list, accent_color: str):
    """
    Dibuja el gráfico interactivo de barras con la proyección de kilos a lo largo de los meses.
    """
    fig_plotly = go.Figure()
    fig_plotly.add_trace(go.Bar(
        x=fechas_reales, y=pesos_prog, 
        marker_color=accent_color, 
        text=[f"{round(v,1)} kg" for v in pesos_prog], 
        textposition='auto', 
        hoverinfo='x+y', 
        hovertemplate='<b>Fecha:</b> %{x}<br><b>Peso Proyectado:</b> %{y} kg<extra></extra>'
    ))
    
    fig_plotly.update_layout(
        title=dict(text="Proyección de Evolución Corporal", font=dict(color=accent_color, size=18)), 
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', 
        font=dict(color='#ffffff'), 
        xaxis=dict(showgrid=False, linecolor=accent_color), 
        yaxis=dict(showgrid=True, gridcolor='#333333', linecolor=accent_color, zeroline=False), 
        margin=dict(l=20, r=20, t=50, b=20)
    )
    st.plotly_chart(fig_plotly, use_container_width=True, key="grafico_evolucion_corporal_elite")


def renderizar_evolucion_historica(perfil_id: str, peso_actual: float, rfm: float, brazos: float, piernas: float, tipo_objetivo: str):
    """
    Trae los datos históricos de Supabase, calcula deltas y dibuja las curvas evolutivas en pestañas.
    """
    st.markdown("### 📈 Tu Evolución Histórica")

    if not perfil_id:
        st.info("📌 Movimientos en tiempo real: Ajustá los datos de tu izquierda y mirá cómo se proyectan aquí de inmediato.")
        return

    try:
        res_historial = supabase.table("evaluaciones_biometricas").select("*").eq("perfil_id", perfil_id).order("fecha_registro").execute()
        
        if len(res_historial.data) > 0:
            df_hist = pd.DataFrame(res_historial.data)
            df_hist = df_hist[df_hist['peso'] > 0]
            df_hist = df_hist.groupby('fecha_registro').last().reset_index()
        else:
            df_hist = pd.DataFrame(columns=['fecha_registro', 'peso', 'rfm', 'brazos', 'piernas'])
        
        fecha_hoy = str(date.today())
        datos_en_vivo = {'fecha_registro': fecha_hoy, 'peso': peso_actual, 'rfm': rfm, 'brazos': brazos, 'piernas': piernas}
        
        if not df_hist.empty and fecha_hoy in df_hist['fecha_registro'].values:
            idx = df_hist.index[df_hist['fecha_registro'] == fecha_hoy].tolist()[0]
            df_hist.at[idx, 'peso'] = peso_actual
            df_hist.at[idx, 'rfm'] = rfm
            if 'brazos' in df_hist.columns: df_hist.at[idx, 'brazos'] = brazos
            if 'piernas' in df_hist.columns: df_hist.at[idx, 'piernas'] = piernas
        else:
            df_nuevo_punto = pd.DataFrame([datos_en_vivo])
            df_hist = pd.concat([df_hist, df_nuevo_punto], ignore_index=True)
            
        df_hist['fecha_registro_str'] = pd.to_datetime(df_hist['fecha_registro']).dt.strftime('%d/%m/%Y')
        
        if len(df_hist) > 1:
            peso_ini = float(df_hist['peso'].iloc[0])
            peso_dinamico = float(df_hist['peso'].iloc[-1])
            dif_peso = peso_dinamico - peso_ini
            
            grasa_ini = float(df_hist['rfm'].iloc[0])
            grasa_dinamica = float(df_hist['rfm'].iloc[-1])
            dif_grasa = grasa_dinamica - grasa_ini
            
            if 'brazos' in df_hist.columns:
                df_brazos = df_hist[df_hist['brazos'] > 0]
                if not df_brazos.empty:
                    brazo_ini = float(df_brazos['brazos'].iloc[0])
                    brazo_dinamico = float(df_brazos['brazos'].iloc[-1])
                    dif_brazo = brazo_dinamico - brazo_ini
                else:
                    brazo_dinamico = brazos
                    dif_brazo = 0
            else:
                brazo_dinamico = brazos
                dif_brazo = 0

            # Bloque motivacional personalizado del Team Eddy
            st.markdown("""
            <div style="background-color: rgba(212, 175, 55, 0.1); border-left: 4px solid #d4af37; padding: 15px; border-radius: 5px; margin-bottom: 20px;">
                <h4 style="color: #d4af37; margin-top: 0; margin-bottom: 10px;">🤖 Análisis de tu progreso en vivo:</h4>
            """, unsafe_allow_html=True)
            
            mensaje = ""
            if dif_peso < 0: mensaje += f"🔥 ¡Excelente trabajo! Has <b>bajado {abs(dif_peso):.1f} kg</b> desde que empezaste. "
            elif dif_peso > 0: mensaje += f"💪 Has <b>subido {abs(dif_peso):.1f} kg</b>. "
            else: mensaje += "⚖️ Te has mantenido en tu peso exacto. "
                
            if dif_grasa < 0: mensaje += f"Lograste quemar un <b>{abs(dif_grasa):.1f}% de grasa</b>. "
            if dif_brazo > 0: mensaje += f"¡Y tus brazos crecieron <b>{dif_brazo:.1f} cm</b>! "
                
            st.markdown(f"<p style='color: #ffffff; font-size: 16px; margin-bottom: 0; line-height: 1.5;'>{mensaje}</p></div>", unsafe_allow_html=True)

            c1, c2, c3 = st.columns(3)
            c1.metric("⚖️ Peso", f"{peso_dinamico} kg", f"{dif_peso:+.1f} kg", delta_color="inverse" if "Pérdida" in tipo_objetivo else "normal")
            c2.metric("🔥 Grasa Corporal", f"{grasa_dinamica}%", f"{dif_grasa:+.1f}%", delta_color="inverse")
            c3.metric("💪 Brazos", f"{brazo_dinamico} cm", f"{dif_brazo:+.1f} cm")
            
            st.markdown("<br>", unsafe_allow_html=True)
            tab_peso, tab_medidas = st.tabs(["⚖️ Curva de Peso y Grasa", "💪 Evolución Muscular"])
            
            with tab_peso:
                fig1 = go.Figure()
                fig1.add_trace(go.Scatter(
                    x=df_hist['fecha_registro_str'], y=df_hist['peso'], mode='lines+markers', name='Peso (kg)', 
                    line=dict(color='#00D9FF', width=4, shape='spline'), marker=dict(size=10, color='white', line=dict(width=2, color='#00D9FF')),
                    fill='tozeroy', fillcolor='rgba(0, 217, 255, 0.1)', hovertemplate='<b>Día:</b> %{x}<br><b>Peso:</b> %{y} kg<extra></extra>'
                ))
                fig1.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='white', hovermode="x unified", margin=dict(l=10, r=10, t=30, b=20), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5))
                st.plotly_chart(fig1, use_container_width=True)
            
            with tab_medidas:
                fig2 = go.Figure()
                df_graf_brazos = df_hist[df_hist['brazos'] > 0]
                df_graf_piernas = df_hist[df_hist['piernas'] > 0]
                
                if not df_graf_brazos.empty:
                    fig2.add_trace(go.Scatter(
                        x=df_graf_brazos['fecha_registro_str'], y=df_graf_brazos['brazos'], mode='lines+markers', name='Brazos (cm)', 
                        line=dict(color='#D4AF37', width=4, shape='spline'), marker=dict(size=10, color='white', line=dict(width=2, color='#D4AF37')), hovertemplate='<b>Día:</b> %{x}<br><b>Brazos:</b> %{y} cm<extra></extra>'
                    ))
                if not df_graf_piernas.empty:
                    fig2.add_trace(go.Scatter(
                        x=df_graf_piernas['fecha_registro_str'], y=df_graf_piernas['piernas'], mode='lines+markers', name='Piernas (cm)', 
                        line=dict(color='#00FF00', width=4, shape='spline'), marker=dict(size=10, color='white', line=dict(width=2, color='#00FF00')), hovertemplate='<b>Día:</b> %{x}<br><b>Piernas:</b> %{y} cm<extra></extra>'
                    ))
                fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='white', hovermode="x unified", margin=dict(l=10, r=10, t=30, b=20), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5))
                st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("📌 Movimientos en tiempo real: Ajustá los datos de tu izquierda y mirá cómo se proyectan aquí de inmediato.")
            
    except Exception as e:
        st.error(f"❌ Error al procesar componente de evolución histórica: {e}")