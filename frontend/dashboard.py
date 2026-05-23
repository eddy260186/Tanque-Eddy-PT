import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date
from database.conexion import supabase

def renderizar_dashboard(perfil_id, peso_actual, rfm, brazos, piernas, tipo_objetivo):
    # ==========================================
    # 📈 DASHBOARD DE EVOLUCIÓN HISTÓRICA (TIEMPO REAL)
    # ==========================================
    st.divider()
    st.markdown("### 📈 Tu Evolución Histórica")

    if perfil_id:
        try:
            res_historial = supabase.table("evaluaciones_biometricas").select("*").eq("perfil_id", perfil_id).order("fecha_registro").execute()
            
            if len(res_historial.data) > 0:
                df_hist = pd.DataFrame(res_historial.data)
                df_hist = df_hist[df_hist['peso'] > 0]
                df_hist = df_hist.groupby('fecha_registro').last().reset_index()
            else:
                df_hist = pd.DataFrame(columns=['fecha_registro', 'peso', 'rfm', 'brazos', 'piernas'])
            
            fecha_hoy = str(date.today())
            datos_en_vivo = {
                'fecha_registro': fecha_hoy,
                'peso': peso_actual,
                'rfm': rfm,
                'brazos': brazos,
                'piernas': piernas
            }
            
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
            
            if len(df_hist) > 0:
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

                st.markdown("""
                <div style="background-color: rgba(212, 175, 55, 0.1); border-left: 4px solid #d4af37; padding: 15px; border-radius: 5px; margin-bottom: 20px;">
                    <h4 style="color: #d4af37; margin-top: 0; margin-bottom: 10px;">🤖 Análisis de tu progreso en vivo:</h4>
                """, unsafe_allow_html=True)
                
                mensaje = ""
                if len(df_hist) == 1:
                    mensaje += "🎯 <b>¡Bienvenido a tu Punto de Partida!</b> Moví los controles de tu izquierda para probar el sistema en vivo, y cuando estés listo tocá 'Guardar Progreso'. "
                else:
                    if dif_peso < 0:
                        mensaje += f"🔥 ¡Excelente trabajo! Has <b>bajado {abs(dif_peso):.1f} kg</b> desde que empezaste. "
                    elif dif_peso > 0:
                        mensaje += f"💪 Has <b>subido {abs(dif_peso):.1f} kg</b>. "
                    else:
                        mensaje += "⚖️ Te has mantenido en tu peso exacto. "
                        
                    if dif_grasa < 0:
                        mensaje += f"Lograste quemar un <b>{abs(dif_grasa):.1f}% de grasa</b>. "
                        
                    if dif_brazo > 0:
                        mensaje += f"¡Y tus brazos crecieron <b>{dif_brazo:.1f} cm</b>! "
                    
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
                        x=df_hist['fecha_registro_str'], y=df_hist['peso'], 
                        mode='lines+markers', name='Peso (kg)', 
                        line=dict(color='#00D9FF', width=4, shape='spline'), 
                        marker=dict(size=12, color='white', line=dict(width=2, color='#00D9FF')),
                        fill='tozeroy', fillcolor='rgba(0, 217, 255, 0.1)',
                        hovertemplate='<b>Día:</b> %{x}<br><b>Peso:</b> %{y} kg<extra></extra>'
                    ))
                    fig1.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='white',
                        hovermode="x unified", margin=dict(l=10, r=10, t=30, b=20),
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
                    )
                    st.plotly_chart(fig1, use_container_width=True)
                
                with tab_medidas:
                    fig2 = go.Figure()
                    df_graf_brazos = df_hist[df_hist['brazos'] > 0]
                    df_graf_piernas = df_hist[df_hist['piernas'] > 0]
                    
                    if not df_graf_brazos.empty:
                        fig2.add_trace(go.Scatter(
                            x=df_graf_brazos['fecha_registro_str'], y=df_graf_brazos['brazos'], 
                            mode='lines+markers', name='Brazos (cm)', 
                            line=dict(color='#D4AF37', width=4, shape='spline'), 
                            marker=dict(size=12, color='white', line=dict(width=2, color='#D4AF37')),
                            hovertemplate='<b>Día:</b> %{x}<br><b>Brazos:</b> %{y} cm<extra></extra>'
                        ))
                    if not df_graf_piernas.empty:
                        fig2.add_trace(go.Scatter(
                            x=df_graf_piernas['fecha_registro_str'], y=df_graf_piernas['piernas'], 
                            mode='lines+markers', name='Piernas (cm)', 
                            line=dict(color='#00FF00', width=4, shape='spline'), 
                            marker=dict(size=12, color='white', line=dict(width=2, color='#00FF00')),
                            hovertemplate='<b>Día:</b> %{x}<br><b>Piernas:</b> %{y} cm<extra></extra>'
                        ))
                    fig2.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='white',
                        hovermode="x unified", margin=dict(l=10, r=10, t=30, b=20),
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
                    )
                    st.plotly_chart(fig2, use_container_width=True)
        except Exception as e:
            st.error(f"❌ Error al cargar historial: {e}")