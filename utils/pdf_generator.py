import os
import base64
from weasyprint import HTML

def build_pdf_v60_7(d, grafico_b64, ruta_img, gen):
    # ==========================================\
    # 1. LÓGICA DE EDICIONES LUXURY Y LOGOS
    # ==========================================\
    is_f = (gen == "f")
    
    # Colores Base (Ébano absoluto y Blanco)
    c_bg = "#070707"         
    c_card = "#111111"       
    c_txt = "#F5F5F5"        
    c_titanio = "#A0A0A0"    
    
    if is_f:
        # RUBY BLACK ELITE (Femenino)
        c_accent = "#FF0055"     # Rosa Neón/Rubí de la foto
        c_dark = "#4A0018"
        nombre_edicion = "RUBY BLACK ELITE"
        ruta_logo_exacta = "logo_rosa.png" 
    else:
        # BLACK GOLD ALPHA (Masculino)
        c_accent = "#FFD700"     # Dorado Metálico de la foto
        c_dark = "#5A4A00"
        nombre_edicion = "BLACK GOLD ALPHA"
        ruta_logo_exacta = "logo_dorado.png"

    # ==========================================\
    # 2. PROCESAMIENTO DE IMÁGENES
    # ==========================================\
    logo_portada = ""
    logo_chico = ""
    ruta_final = ruta_logo_exacta if os.path.exists(ruta_logo_exacta) else ruta_img

    if ruta_final and os.path.exists(ruta_final):
        with open(ruta_final, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
            logo_portada = f'<img src="data:image/png;base64,{b64}" class="img-portada">'
            logo_chico = f'<img src="data:image/png;base64,{b64}" class="img-chica">'

    # Simulador de Código QR para el pie de página
    qr_placeholder = """<div style="border: 2px solid #fff; padding: 2px; width: 40px; height: 40px; display: inline-block; background: url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==');"></div>"""

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
            .page-cover {{ text-align: center; height: 100vh; box-sizing: border-box; padding: 50px 30px; position: relative; }}
            .img-portada {{ height: 380px; filter: drop-shadow(0 0 30px {c_dark}); margin-bottom: 20px; }}
            .cover-title {{ font-family: 'Bebas Neue', cursive; font-size: 60px; letter-spacing: 6px; color: {c_accent}; margin: 0; text-shadow: 0 5px 15px #000; }}
            .cover-subtitle {{ font-family: 'Montserrat', sans-serif; font-size: 11px; letter-spacing: 5px; color: {c_titanio}; margin-top: 5px; text-transform: uppercase; }}
            
            .badge-edicion {{ border: 1px solid {c_accent}; color: {c_txt}; padding: 6px 25px; border-radius: 30px; font-weight: bold; font-size: 12px; letter-spacing: 3px; display: inline-block; margin: 25px 0; background: linear-gradient(180deg, #111, #000); box-shadow: 0 0 15px {c_dark}; }}
            
            .atleta-box {{ margin-top: 10px; border-top: 1px solid #333; padding-top: 20px; width: 60%; margin-left: auto; margin-right: auto; }}
            .atleta-name {{ font-family: 'Bebas Neue', cursive; font-size: 45px; color: {c_accent}; margin: 0; letter-spacing: 2px; }}
            
            .footer-portada {{ position: absolute; bottom: 40px; width: calc(100% - 60px); display: flex; justify-content: space-between; align-items: flex-end; border-top: 1px solid #333; padding-top: 15px; }}
            .signature {{ font-family: 'Great Vibes', cursive; font-size: 28px; color: {c_titanio}; }}
            
            /* --- INTERIORES (EL DASHBOARD) --- */
            .page-content {{ padding: 30px 40px; page-break-before: always; }}
            .header-interior {{ border-bottom: 1px solid #333; padding-bottom: 10px; margin-bottom: 20px; display: table; width: 100%; }}
            .header-left {{ display: table-cell; vertical-align: bottom; width: 80%; }}
            .header-right {{ display: table-cell; vertical-align: bottom; text-align: right; width: 20%; }}
            .header-left h1 {{ font-family: 'Bebas Neue'; font-size: 32px; color: {c_accent}; margin: 0; letter-spacing: 2px; display: inline-block; }}
            .img-chica {{ height: 50px; filter: drop-shadow(0 0 5px {c_accent}); }}
            
            /* TARJETAS DE CRISTAL (Gauges simulados) */
            .grid-container {{ width: 100%; border-collapse: separate; border-spacing: 12px; margin-left: -12px; }}
            .glass-card {{ background: linear-gradient(145deg, #151515, #080808); border: 1px solid #222; border-top: 2px solid {c_accent}; border-radius: 8px; padding: 15px; box-shadow: 0 8px 15px rgba(0,0,0,0.8); text-align: center; }}
            
            .metric-label {{ color: {c_titanio}; font-size: 9px; text-transform: uppercase; letter-spacing: 1px; display: block; margin-bottom: 8px; }}
            .metric-value {{ font-family: 'Bebas Neue'; font-size: 28px; color: {c_txt}; display: block; }}
            .metric-highlight {{ color: {c_accent}; font-family: 'Bebas Neue'; font-size: 34px; display: block; }}
            
            /* BARRAS DE PROGRESO NEÓN */
            .bar-bg {{ width: 100%; background: #222; height: 6px; border-radius: 3px; margin-top: 10px; overflow: hidden; }}
            .bar-fill {{ background: linear-gradient(90deg, {c_dark}, {c_accent}); height: 100%; box-shadow: 0 0 10px {c_accent}; }}
            
            /* LISTAS Y TABLAS (Para que no se corte nada) */
            .list-card {{ background: {c_card}; border: 1px solid #1a1a1a; border-left: 3px solid {c_accent}; padding: 15px; margin-bottom: 12px; border-radius: 6px; }}
            .list-card h3 {{ font-family: 'Bebas Neue'; color: {c_accent}; font-size: 20px; margin: 0 0 8px 0; letter-spacing: 1px; }}
            .data-table {{ width: 100%; border-collapse: collapse; }}
            .data-table td {{ padding: 8px 5px; border-bottom: 1px solid #151515; font-size: 10px; color: #ddd; vertical-align: top; }}
            
            /* FIRMA PIE DE PÁGINA INTERIOR */
            .footer-interior {{ margin-top: 40px; border-top: 1px solid #222; padding-top: 15px; display: table; width: 100%; }}
            .footer-interior td {{ vertical-align: middle; }}
        </style>
    </head>
    <body>
        
        <div class="page-cover">
            {logo_portada}
            <h1 class="cover-title">PLAN INTEGRAL ELITE</h1>
            <div class="cover-subtitle">INGENIERÍA CORPORAL DE ALTO VALOR</div>
            
            <div class="badge-edicion">{nombre_edicion}</div>
            
            <div class="atleta-box">
                <div style="font-size: 10px; color: {c_titanio}; letter-spacing: 2px; margin-bottom: 5px;">ATLETA DE ÉLITE</div>
                <h2 class="atleta-name">{d['n'].upper()}</h2>
                <div style="font-size: 9px; color: {c_titanio}; letter-spacing: 1px; margin-top: 5px;">NIVEL DE ENTRENAMIENTO: {d['nivel'].upper()}</div>
            </div>
            
            <table class="footer-portada">
                <tr>
                    <td style="text-align: left; width: 33%;">{qr_placeholder}</td>
                    <td style="text-align: center; width: 33%; font-size: 8px; color: #666; letter-spacing: 1px;">POWERED BY EDDY PERSONAL PT ELITE</td>
                    <td style="text-align: right; width: 33%;"><div class="signature">Eddy Signature</div></td>
                </tr>
            </table>
        </div>

        <div class="page-content">
            <div class="header-interior">
                <div class="header-left"><h1>📈 ANALÍTICA FÍSICA</h1></div>
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
                        <span class="metric-highlight" style="font-size: 38px;">{d['meta'].upper()}</span>
                        <span style="font-size: 9px; color: {c_titanio};">DIETA: {d['dt'].upper()} | RCC: {d['rcc']}</span>
                    </td>
                    <td class="glass-card" style="width: 25%;">
                        <span class="metric-label">KCal Diarias</span>
                        <span class="metric-value">{d['k']:.0f}</span>
                        <div class="bar-bg"><div class="bar-fill" style="width: 100%;"></div></div>
                    </td>
                    <td class="glass-card" style="width: 25%; border-top-color: #00BFFF;">
                        <span class="metric-label" style="color: #00BFFF;">Hidratación</span>
                        <span class="metric-value" style="color: #00BFFF;">{d['w']} LTS</span>
                        <div class="bar-bg"><div class="bar-fill" style="width: 100%; background: #00BFFF; box-shadow: 0 0 10px #00BFFF;"></div></div>
                    </td>
                </tr>
            </table>

            <div class="glass-card" style="margin-top: 10px; padding: 10px;">
                <span class="metric-label" style="text-align: left;">PROYECCIÓN DE EVOLUCIÓN</span>
                <img src="data:image/png;base64,{grafico_b64}" style="width: 100%; border-radius: 5px; border: 1px solid #222;">
            </div>
        </div>

        <div class="page-content">
            <div class="header-interior">
                <div class="header-left"><h1>🥗 ESTRATEGIA NUTRICIONAL</h1></div>
                <div class="header-right">{logo_chico}</div>
            </div>

            <table class="grid-container" style="margin-bottom: 10px;">
                <tr>
                    <td class="glass-card" style="padding: 10px;">
                        <span class="metric-label">Proteína</span>
                        <span class="metric-value" style="font-size: 20px;">p {d['p']:.0f}g</span>
                    </td>
                    <td class="glass-card" style="padding: 10px;">
                        <span class="metric-label">Carbohidratos</span>
                        <span class="metric-value" style="font-size: 20px;">c {d['c']:.0f}g</span>
                    </td>
                    <td class="glass-card" style="padding: 10px;">
                        <span class="metric-label">Grasas</span>
                        <span class="metric-value" style="font-size: 20px;">g {d['g']:.0f}g</span>
                    </td>
                </tr>
            </table>
    """

    # --- BUCLE INTACTO DE COMIDAS (Para que NO falte nada) ---
    for comida, opciones in d['m'].items():
        html += f"""
            <div class="list-card">
                <h3>🍴 {comida}</h3>
                <table class="data-table">
        """
        for op in opciones:
            html += f"<tr><td style="width: 10px; color: {c_accent};">•</td><td>{op}</td></tr>"
        html += "</table></div>"

    # --- BUCLE INTACTO DE SUPLEMENTACIÓN ---
    html += f"""
            <div class="list-card" style="border-left-color: #00BFFF;">
                <h3 style="color: #00BFFF;">💊 SUPLEMENTACIÓN Y MICRONUTRIENTES</h3>
                <table class="data-table">
    """
    for suplemento in d['s']:
        html += f'<tr><td style="width: 10px; color: #00BFFF;">•</td><td>{suplemento}</td></tr>'
        
    html += """
                </table>
            </div>
            
            <table class="footer-interior">
                <tr>
                    <td style="text-align: right;"><div class="signature">Eddy Signature</div><div style="font-size: 8px; color: #666;">Firma digital cromada</div></td>
                    <td style="width: 50px; text-align: right;">{qr_placeholder}</td>
                </tr>
            </table>
        </div>
    """

    # ==========================================\
    # PÁGINA 4: ENTRENAMIENTO (Bucle Completo)
    # ==========================================\
    html += f"""
        <div class="page-content">
            <div class="header-interior">
                <div class="header-left"><h1>🏋️‍♂️ PLAN DE ENTRENAMIENTO</h1></div>
                <div class="header-right">{logo_chico}</div>
            </div>
            <div style="font-size: 10px; color: {c_titanio}; margin-bottom: 15px;">TIPO: {d['entreno'].upper()} | {d['dias']} DÍAS/SEM</div>
    """

    # --- BUCLE INTACTO DE RUTINAS ---
    for dia, ejercicios in d['rutina'].items():
        html += f"""
            <div class="list-card">
                <h3>📅 {dia}</h3>
                <table class="data-table">
        """
        for ej in ejercicios:
            html += f"<tr><td style="width: 10px; color: {c_accent};">•</td><td>{ej}</td></tr>"
        html += "</table></div>"

    html += f"""
            <table class="footer-interior">
                <tr>
                    <td style="text-align: right;"><div class="signature">Eddy Signature</div><div style="font-size: 8px; color: #666;">Firma digital cromada</div></td>
                    <td style="width: 50px; text-align: right;">{qr_placeholder}</td>
                </tr>
            </table>
        </div>
    """

    # ==========================================\
    # PÁGINA 5: TICKET DE COMPRAS (Bucle Completo)
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
    
    # --- BUCLE INTACTO DE COMPRAS ---
    for item, cant in d['compras'].items():
        if "Huevo" in item or "Claras" in item:
            unidades = int(cant / 50)
            res = f"<b style='color:{c_accent};'>{unidades} Uni.</b> (~{round(unidades/12, 1)} Doc.)"
        elif any(x in item for x in ["Café", "Mate", "Té", "Infusión"]):
            res = f"<b style='color:{c_accent};'>{int(cant)} Tazas</b>"
        else:
            if cant >= 1000:
                res = f"<b style='color:{c_accent};'>{round(cant/1000, 2)} KG</b>"
            else:
                res = f"<b style='color:{c_accent};'>{int(cant)} g</b>"
                
        html += f"<tr><td style='width: 75%; font-weight: bold;'>{item}</td><td style='width: 25%; text-align: right;'>{res}</td></tr>"
    
    html += f"""
                </table>
            </div>
            
            <table class="footer-interior" style="margin-top: 60px;">
                <tr>
                    <td style="text-align: left; font-family: 'Bebas Neue'; font-size: 20px; color: {c_accent}; letter-spacing: 3px;">EDDY PERSONAL TRAINER ELITE</td>
                    <td style="text-align: right;"><div class="signature">Eddy Signature</div></td>
                    <td style="width: 50px; text-align: right;">{qr_placeholder}</td>
                </tr>
            </table>
        </div>
    </body></html>
    """
    
    return HTML(string=html).write_pdf()