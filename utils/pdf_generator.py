import os
import base64
from weasyprint import HTML

def build_pdf_v60_7(d, grafico_b64, ruta_img, gen):
    # ==========================================\
    # 1. LÓGICA DE EDICIONES LUXURY Y LOGOS
    # ==========================================\
    is_f = (gen == "f")
    
    # Colores Base (Ébano absoluto y Blanco)
    c_bg = "#050505"         
    c_card = "#121212"       
    c_txt = "#F5F5F5"        
    c_titanio = "#A0A0A0"    
    
    if is_f:
        # RUBY BLACK ELITE (Femenino)
        c_accent = "#FF0055"     # Rosa Neón/Rubí de la foto
        c_dark = "rgba(255, 0, 85, 0.3)" # Para el glow radial
        nombre_edicion = "RUBY BLACK ELITE"
        ruta_logo_exacta = "logo_rosa.png" 
    else:
        # BLACK GOLD ALPHA (Masculino)
        c_accent = "#FFD700"     # Dorado Metálico de la foto
        c_dark = "rgba(255, 215, 0, 0.3)" # Para el glow radial
        nombre_edicion = "BLACK GOLD ALPHA"
        ruta_logo_exacta = "logo_dorado.png"

    # ==========================================\
    # 2. PROCESAMIENTO DE IMÁGENES (CON GLOW HACK)
    # ==========================================\
    logo_portada = ""
    logo_chico = ""
    ruta_final = ruta_logo_exacta if os.path.exists(ruta_logo_exacta) else ruta_img

    if ruta_final and os.path.exists(ruta_final):
        with open(ruta_final, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
            # Logo chico normal
            logo_chico = f'<img src="data:image/png;base64,{b64}" class="img-chica">'
            # HACK WEASYPRINT: Glow radial detrás de la imagen (porque WeasyPrint no lee drop-shadow)
            logo_portada = f"""
            <div style="display: inline-block; background: radial-gradient(circle, {c_dark} 0%, transparent 65%); padding: 40px; border-radius: 50%;">
                <img src="data:image/png;base64,{b64}" class="img-portada">
            </div>
            """

    # Simulador de Código QR para el pie de página
    qr_placeholder = """<div style="border: 2px solid #fff; padding: 2px; width: 45px; height: 45px; display: inline-block; background: url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==');"></div>"""

    # ==========================================\
    # 3. MAQUETADO CSS EXTREMO (ESTILO DASHBOARD)
    # ==========================================\
    html = f"""
    <html>
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Montserrat:wght@300;400;700&family=Great+Vibes&display=swap" rel="stylesheet">
        <style>
            @page {{ size: A4; margin: 0; background-color: {c_bg}; }}
            body {{ font-family: 'Montserrat', sans-serif; color: {c_txt}; background-color: {c_bg}; margin: 0; padding: 0; font-size: 10px; }}
            
            /* --- PORTADA CALCADA A LA FOTO --- */
            .page-cover {{ text-align: center; height: 100vh; box-sizing: border-box; padding: 60px 30px; position: relative; }}
            .img-portada {{ height: 350px; position: relative; z-index: 10; }}
            .cover-title {{ font-family: 'Bebas Neue', cursive; font-size: 65px; letter-spacing: 7px; color: {c_accent}; margin: -20px 0 0 0; text-shadow: 2px 2px 5px #000; }}
            .cover-subtitle {{ font-family: 'Montserrat', sans-serif; font-size: 12px; letter-spacing: 5px; color: {c_titanio}; margin-top: 5px; text-transform: uppercase; }}
            
            .badge-edicion {{ border: 1px solid {c_accent}; color: {c_txt}; padding: 8px 30px; border-radius: 40px; font-weight: bold; font-size: 13px; letter-spacing: 4px; display: inline-block; margin: 30px 0; background-color: #000; box-shadow: 0 0 10px rgba(255,255,255,0.1); }}
            
            .atleta-box {{ margin-top: 20px; border-top: 1px solid #333; border-bottom: 1px solid #333; padding: 20px 0; width: 70%; margin-left: auto; margin-right: auto; }}
            .atleta-name {{ font-family: 'Bebas Neue', cursive; font-size: 50px; color: {c_accent}; margin: 0; letter-spacing: 2px; }}
            
            .footer-portada {{ position: absolute; bottom: 50px; left: 40px; right: 40px; display: table; width: calc(100% - 80px); border-top: 1px solid #333; padding-top: 15px; }}
            .signature {{ font-family: 'Great Vibes', cursive; font-size: 32px; color: {c_titanio}; }}
            
            /* --- INTERIORES (EL DASHBOARD) --- */
            .page-content {{ padding: 40px; page-break-before: always; }}
            .header-interior {{ border-bottom: 1px solid #333; padding-bottom: 10px; margin-bottom: 25px; display: table; width: 100%; }}
            .header-left {{ display: table-cell; vertical-align: bottom; width: 80%; }}
            .header-right {{ display: table-cell; vertical-align: bottom; text-align: right; width: 20%; }}
            .header-left h1 {{ font-family: 'Bebas Neue'; font-size: 35px; color: {c_accent}; margin: 0; letter-spacing: 2px; }}
            .img-chica {{ height: 55px; }}
            
            /* TARJETAS DE CRISTAL (Gauges simulados) */
            .grid-container {{ width: 100%; border-collapse: separate; border-spacing: 12px; margin-left: -12px; }}
            .glass-card {{ background-color: {c_card}; border: 1px solid #1a1a1a; border-top: 3px solid {c_accent}; border-radius: 8px; padding: 18px; text-align: center; }}
            
            .metric-label {{ color: {c_titanio}; font-size: 9px; text-transform: uppercase; letter-spacing: 1px; display: block; margin-bottom: 8px; }}
            .metric-value {{ font-family: 'Bebas Neue'; font-size: 30px; color: {c_txt}; display: block; }}
            .metric-highlight {{ color: {c_accent}; font-family: 'Bebas Neue'; font-size: 38px; display: block; text-shadow: 0 0 10px rgba(0,0,0,0.5); }}
            
            /* BARRAS DE PROGRESO NEÓN */
            .bar-bg {{ width: 100%; background: #222; height: 5px; border-radius: 3px; margin-top: 12px; overflow: hidden; }}
            .bar-fill {{ background-color: {c_accent}; height: 100%; }}
            
            /* LISTAS Y TABLAS (Para que no se corte nada) */
            .list-card {{ background-color: {c_card}; border: 1px solid #1a1a1a; border-left: 4px solid {c_accent}; padding: 18px; margin-bottom: 15px; border-radius: 6px; }}
            .list-card h3 {{ font-family: 'Bebas Neue'; color: {c_accent}; font-size: 22px; margin: 0 0 10px 0; letter-spacing: 1px; }}
            .data-table {{ width: 100%; border-collapse: collapse; }}
            .data-table td {{ padding: 10px 5px; border-bottom: 1px solid #1a1a1a; font-size: 11px; color: #ddd; vertical-align: top; }}
            
            /* FIRMA PIE DE PÁGINA INTERIOR */
            .footer-interior {{ margin-top: 40px; border-top: 1px solid #222; padding-top: 15px; display: table; width: 100%; }}
        </style>
    </head>
    <body>
        
        <div class="page-cover">
            {logo_portada}
            <h1 class="cover-title">PLAN INTEGRAL ELITE</h1>
            <div class="cover-subtitle">INGENIERÍA CORPORAL DE ALTO VALOR</div>
            
            <div class="badge-edicion">{nombre_edicion}</div>
            
            <div class="atleta-box">
                <div style="font-size: 11px; color: {c_titanio}; letter-spacing: 3px; margin-bottom: 5px;">ATLETA DE ÉLITE</div>
                <h2 class="atleta-name">{d['n'].upper()}</h2>
                <div style="font-size: 10px; color: {c_titanio}; letter-spacing: 2px; margin-top: 8px;">NIVEL DE ENTRENAMIENTO: {d['nivel'].upper()}</div>
            </div>
            
            <table class="footer-portada">
                <tr>
                    <td style="text-align: left; width: 33%; vertical-align: bottom;">{qr_placeholder}</td>
                    <td style="text-align: center; width: 33%; vertical-align: bottom; font-size: 9px; color: #666; letter-spacing: 2px;">POWERED BY EDDY PT ELITE<br>FECHA: {d.get('fecha', 'ACTUAL')}</td>
                    <td style="text-align: right; width: 33%; vertical-align: bottom;"><div class="signature">Eddy Signature</div></td>
                </tr>
            </table>
        </div>

        <div class="page-content">
            <div class="header-interior">
                <div class="header-left"><h1>📈 ANALÍTICA FÍSICA Y OBJETIVOS</h1></div>
                <div class="header-right">{logo_chico}</div>
            </div>

            <table class="grid-container">
                <tr>
                    <td class="glass-card" style="width: 25%;">
                        <span class="metric-label">Edad / Estatura</span>
                        <span class="metric-value">{d['edad']} A / {d['estatura']} CM</span>
                        <div class="bar-bg"><div class="bar-fill" style="width: 80%;"></div></div>
                    </td>
                    <td class="glass-card" style="width: 25%;">
                        <span class="metric-label">Peso Actual</span>
                        <span class="metric-value">{d['peso']} KG</span>
                        <div class="bar-bg"><div class="bar-fill" style="width: 75%;"></div></div>
                    </td>
                    <td class="glass-card" style="width: 25%;">
                        <span class="metric-label">Cintura / Cadera</span>
                        <span class="metric-value">{d['cintura']} / {d['cadera']} CM</span>
                        <div class="bar-bg"><div class="bar-fill" style="width: 60%;"></div></div>
                    </td>
                    <td class="glass-card" style="width: 25%;">
                        <span class="metric-label">Grasa Estimada</span>
                        <span class="metric-highlight">{d['rfm']}%</span>
                    </td>
                </tr>
            </table>

            <table class="grid-container">
                <tr>
                    <td class="glass-card" style="width: 50%; border-top-color: #fff;">
                        <span class="metric-label" style="color: #fff;">Porcentaje Objetivo (Meta)</span>
                        <span class="metric-highlight" style="font-size: 40px;">{d['meta'].upper()}</span>
                        <span style="font-size: 10px; color: {c_titanio}; margin-top: 5px; display: block;">DIETA: {d['dt'].upper()} | ÍNDICE RCC: {d['rcc']}</span>
                    </td>
                    <td class="glass-card" style="width: 25%;">
                        <span class="metric-label">KCal Diarias</span>
                        <span class="metric-value">{d['k']:.0f}</span>
                        <div class="bar-bg"><div class="bar-fill" style="width: 100%;"></div></div>
                    </td>
                    <td class="glass-card" style="width: 25%; border-top-color: #00BFFF;">
                        <span class="metric-label" style="color: #00BFFF;">Hidratación</span>
                        <span class="metric-value" style="color: #00BFFF;">{d['w']} LTS</span>
                        <div class="bar-bg"><div class="bar-fill" style="width: 100%; background-color: #00BFFF;"></div></div>
                    </td>
                </tr>
            </table>

            <div class="glass-card" style="margin-top: 10px; padding: 15px; text-align: left;">
                <span class="metric-label">PROYECCIÓN DE EVOLUCIÓN</span>
                <img src="data:image/png;base64,{grafico_b64}" style="width: 100%; border-radius: 6px; border: 1px solid #1a1a1a; margin-top: 5px;">
            </div>
        </div>

        <div class="page-content">
            <div class="header-interior">
                <div class="header-left"><h1>🥗 ESTRATEGIA NUTRICIONAL</h1></div>
                <div class="header-right">{logo_chico}</div>
            </div>

            <table class="grid-container" style="margin-bottom: 15px;">
                <tr>
                    <td class="glass-card" style="padding: 12px;">
                        <span class="metric-label">Proteína Total</span>
                        <span class="metric-value" style="font-size: 24px;">P: {d['p']:.0f}g</span>
                    </td>
                    <td class="glass-card" style="padding: 12px;">
                        <span class="metric-label">Carbohidratos</span>
                        <span class="metric-value" style="font-size: 24px;">C: {d['c']:.0f}g</span>
                    </td>
                    <td class="glass-card" style="padding: 12px;">
                        <span class="metric-label">Grasas</span>
                        <span class="metric-value" style="font-size: 24px;">G: {d['g']:.0f}g</span>
                    </td>
                </tr>
            </table>
    """

    # --- BUCLE EXACTO DE COMIDAS ---
    for comida, opciones in d['m'].items():
        html += f"""
            <div class="list-card">
                <h3>🍴 {comida}</h3>
                <table class="data-table">
        """
        for op in opciones:
            html += f"<tr><td style='width: 15px; color: {c_accent}; font-weight: bold;'>•</td><td>{op}</td></tr>"
        html += "</table></div>"

    # --- BUCLE EXACTO DE SUPLEMENTACIÓN ---
    html += f"""
            <div class="list-card" style="border-left-color: #00BFFF;">
                <h3 style="color: #00BFFF;">💊 SUPLEMENTACIÓN Y MICRONUTRIENTES</h3>
                <table class="data-table">
    """
    for suplemento in d['s']:
        html += f"<tr><td style='width: 15px; color: #00BFFF; font-weight: bold;'>•</td><td>{suplemento}</td></tr>"
        
    html += f"""
                </table>
            </div>
            
            <table class="footer-interior">
                <tr>
                    <td style="text-align: right;"><div class="signature">Eddy Signature</div><div style="font-size: 9px; color: #666; letter-spacing: 1px;">FIRMA DIGITAL AUTORIZADA</div></td>
                    <td style="width: 60px; text-align: right; vertical-align: top;">{qr_placeholder}</td>
                </tr>
            </table>
        </div>
    """

    # ==========================================\
    # PÁGINA 4: ENTRENAMIENTO (NO FALTA NINGÚN BUCLE)
    # ==========================================\
    html += f"""
        <div class="page-content">
            <div class="header-interior">
                <div class="header-left"><h1>🏋️‍♂️ PLAN DE ENTRENAMIENTO</h1></div>
                <div class="header-right">{logo_chico}</div>
            </div>
            <div style="font-size: 11px; color: {c_titanio}; margin-top: -10px; margin-bottom: 20px; letter-spacing: 2px;">
                TIPO: <span style="color: {c_txt};">{d['entreno'].upper()}</span> | FRECUENCIA: <span style="color: {c_txt};">{d['dias']} DÍAS/SEM</span>
            </div>
    """

    # --- BUCLE EXACTO DE RUTINAS ---
    for dia, ejercicios in d['rutina'].items():
        html += f"""
            <div class="list-card">
                <h3>📅 {dia}</h3>
                <table class="data-table">
        """
        for ej in ejercicios:
            html += f"<tr><td style='width: 15px; color: {c_accent}; font-weight: bold;'>•</td><td>{ej}</td></tr>"
        html += "</table></div>"

    html += f"""
            <table class="footer-interior">
                <tr>
                    <td style="text-align: right;"><div class="signature">Eddy Signature</div><div style="font-size: 9px; color: #666; letter-spacing: 1px;">FIRMA DIGITAL AUTORIZADA</div></td>
                    <td style="width: 60px; text-align: right; vertical-align: top;">{qr_placeholder}</td>
                </tr>
            </table>
        </div>
    """

    # ==========================================\
    # PÁGINA 5: TICKET DE COMPRAS (NO FALTA NADA)
    # ==========================================\
    html += f"""
        <div class="page-content">
            <div class="header-interior">
                <div class="header-left"><h1>🛒 TICKET DE COMPRA MENSUAL</h1></div>
                <div class="header-right">{logo_chico}</div>
            </div>
            
            <div class="list-card">
                <table class="data-table">
    """
    
    # --- BUCLE EXACTO DE COMPRAS (Con conversiones de huevos e infusiones) ---
    for item, cant in d['compras'].items():
        if "Huevo" in item or "Claras" in item:
            unidades = int(cant / 50)
            res = f"<span style='color:{c_accent}; font-weight: bold; font-size: 12px;'>{unidades} Uni.</span> <span style='color: #888;'>(~{round(unidades/12, 1)} Doc.)</span>"
        elif any(x in item for x in ["Café", "Mate", "Té", "Infusión"]):
            res = f"<span style='color:{c_accent}; font-weight: bold; font-size: 12px;'>{int(cant)} Tazas</span>"
        else:
            if cant >= 1000:
                res = f"<span style='color:{c_accent}; font-weight: bold; font-size: 12px;'>{round(cant/1000, 2)} KG</span>"
            else:
                res = f"<span style='color:{c_accent}; font-weight: bold; font-size: 12px;'>{int(cant)} g</span>"
                
        html += f"<tr><td style='width: 75%; font-weight: bold; font-size: 11px;'>{item}</td><td style='width: 25%; text-align: right;'>{res}</td></tr>"
    
    html += f"""
                </table>
            </div>
            
            <table class="footer-interior" style="margin-top: 50px;">
                <tr>
                    <td style="text-align: left; font-family: 'Bebas Neue'; font-size: 22px; color: {c_accent}; letter-spacing: 4px;">EDDY PERSONAL TRAINER ELITE</td>
                    <td style="text-align: right;"><div class="signature">Eddy Signature</div></td>
                    <td style="width: 60px; text-align: right; vertical-align: top;">{qr_placeholder}</td>
                </tr>
            </table>
        </div>
    </body></html>
    """
    
    return HTML(string=html).write_pdf()