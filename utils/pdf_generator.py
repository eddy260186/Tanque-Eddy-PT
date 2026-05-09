import os
import base64
from weasyprint import HTML

def build_pdf_v60_7(d, grafico_b64, ruta_img, gen):
    # ==========================================\
    # 1. LÓGICA DE EDICIONES LUXURY Y LOGOS FÍSICOS
    # ==========================================\
    is_f = (gen == "f")
    
    # Colores Base (Ébano absoluto y Blanco)
    c_bg = "#050505"         
    c_card = "#0B0B0B"       
    c_txt = "#F5F5F5"        
    c_titanio = "#878681"    
    
    if is_f:
        # RUBY BLACK ELITE (Femenino)
        c_accent = "#E0115F"     
        nombre_edicion = "RUBY BLACK ELITE"
        # BUSCAMOS EL LOGO FÍSICO ROSA
        ruta_logo_exacta = "logo_rosa.png" 
    else:
        # BLACK GOLD ALPHA (Masculino)
        c_accent = "#FFD700"     
        nombre_edicion = "BLACK GOLD ALPHA"
        # BUSCAMOS EL LOGO FÍSICO DORADO
        ruta_logo_exacta = "logo_dorado.png"

    # ==========================================\
    # PROCESAMIENTO DEL LOGO CORRECTO
    # ==========================================\
    logo_img_html_gigante = ""
    logo_img_html_chico = ""
    
    # Verificamos si el logo específico existe, si no, usa el general de ruta_img
    ruta_final = ruta_logo_exacta if os.path.exists(ruta_logo_exacta) else ruta_img

    if ruta_final and os.path.exists(ruta_final):
        with open(ruta_final, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
            # Logo gigante para portada
            logo_img_html_gigante = f'<img src="data:image/png;base64,{b64}" style="height: 350px; display: block; margin: 0 auto;">'
            # Logo chico para cabeceras
            logo_img_html_chico = f'<img src="data:image/png;base64,{b64}" style="height: 60px;">'

    # ==========================================\
    # MAQUETADO CSS 100% COMPATIBLE CON WEASYPRINT
    # ==========================================\
    html = f"""
    <html>
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Montserrat:wght@300;400;700&display=swap" rel="stylesheet">
        <style>
            @page {{ size: A4; margin: 0; background-color: {c_bg}; }}
            body {{ font-family: 'Montserrat', sans-serif; color: {c_txt}; background-color: {c_bg}; margin: 0; padding: 0; font-size: 11px; }}
            
            /* --- PORTADA --- */
            .page-cover {{ text-align: center; padding-top: 120px; height: 100vh; box-sizing: border-box; border-bottom: 5px solid {c_accent}; }}
            .cover-title {{ font-family: 'Bebas Neue', cursive; font-size: 70px; letter-spacing: 5px; color: {c_accent}; margin: 20px 0 0 0; }}
            .badge-edicion {{ border: 2px solid {c_accent}; color: {c_txt}; padding: 10px 30px; border-radius: 50px; font-weight: bold; font-size: 16px; letter-spacing: 3px; display: inline-block; margin-top: 20px; margin-bottom: 40px; }}
            
            /* --- INTERIORES --- */
            .page-content {{ padding: 35px; page-break-before: always; }}
            
            /* Tablas Base WeasyPrint */
            .header-table {{ width: 100%; border-bottom: 2px solid {c_accent}; padding-bottom: 10px; margin-bottom: 20px; }}
            .header-table h1 {{ font-family: 'Bebas Neue'; font-size: 38px; color: {c_accent}; margin: 0; }}
            
            /* Tarjetas de Cristal Oscuro */
            .card-glass {{ background-color: {c_card}; border: 1px solid #222; border-top: 3px solid {c_accent}; padding: 15px; margin-bottom: 15px; border-radius: 8px; }}
            
            /* Grillas 100% Seguras */
            .grid-table {{ width: 100%; border-collapse: separate; border-spacing: 10px; margin-left: -10px; }}
            .grid-td {{ background-color: {c_card}; border: 1px solid #222; padding: 15px; border-radius: 8px; border-top: 2px solid {c_accent}; width: 33%; }}
            
            .metric-title {{ color: {c_titanio}; font-size: 10px; text-transform: uppercase; display: block; margin-bottom: 5px; }}
            .metric-value {{ font-family: 'Bebas Neue'; font-size: 30px; color: {c_txt}; display: block; }}
            
            .data-table {{ width: 100%; border-collapse: collapse; }}
            .data-table td {{ padding: 10px; border-bottom: 1px solid #1A1A1A; }}
        </style>
    </head>
    <body>
        
        <div class="page-cover">
            {logo_img_html_gigante}
            <h1 class="cover-title">PLAN INTEGRAL ELITE</h1>
            <p style="letter-spacing: 4px; color: {c_titanio};">INGENIERÍA CORPORAL DE ALTO VALOR</p>
            <div class="badge-edicion">{nombre_edicion}</div>
            
            <h2 style="font-family: 'Bebas Neue'; font-size: 55px; color: {c_txt}; margin: 0;">{d['n'].upper()}</h2>
            <p style="color: {c_accent}; font-weight: bold; letter-spacing: 2px; margin-top: 5px;">ATLETA DE ÉLITE</p>
            <p style="color: {c_titanio};">NIVEL: {d['nivel'].upper()}</p>
        </div>

        <div class="page-content">
            <table class="header-table">
                <tr>
                    <td style="width: 80%;"><h1>📈 ANALÍTICA FÍSICA Y OBJETIVOS</h1></td>
                    <td style="width: 20%; text-align: right;">{logo_img_html_chico}</td>
                </tr>
            </table>

            <table class="grid-table">
                <tr>
                    <td class="grid-td">
                        <span class="metric-title">ESTATURA</span>
                        <span class="metric-value" style="color: {c_accent};">{d['estatura']} CM</span>
                    </td>
                    <td class="grid-td">
                        <span class="metric-title">PESO ACTUAL</span>
                        <span class="metric-value" style="color: {c_accent};">{d['peso']} KG</span>
                    </td>
                    <td class="grid-td">
                        <span class="metric-title">GRASA ESTIMADA</span>
                        <span class="metric-value" style="color: {c_accent};">{d['rfm']}%</span>
                    </td>
                </tr>
            </table>

            <div class="card-glass" style="text-align: center; padding: 25px;">
                <span class="metric-title" style="margin-bottom: 10px;">OBJETIVO ESTRATÉGICO</span>
                <span style="font-family: 'Bebas Neue'; font-size: 45px; color: {c_txt}; display: block; margin-bottom: 20px;">{d['meta'].upper()}</span>
                
                <table style="width: 100%;">
                    <tr>
                        <td>
                            <span class="metric-title">KCAL DIARIAS</span>
                            <span class="metric-value">{d['k']:.0f}</span>
                        </td>
                        <td>
                            <span class="metric-title">HIDRATACIÓN</span>
                            <span class="metric-value" style="color: #00BFFF;">{d['w']} LTS</span>
                        </td>
                        <td>
                            <span class="metric-title">PROTEÍNA</span>
                            <span class="metric-value">{d['p']:.0f}g</span>
                        </td>
                        <td>
                            <span class="metric-title">CARBOS</span>
                            <span class="metric-value">{d['c']:.0f}g</span>
                        </td>
                        <td>
                            <span class="metric-title">GRASAS</span>
                            <span class="metric-value">{d['g']:.0f}g</span>
                        </td>
                    </tr>
                </table>
            </div>

            <div class="card-glass" style="text-align: center;">
                <span class="metric-title">PROYECCIÓN DE EVOLUCIÓN</span>
                <img src="data:image/png;base64,{grafico_b64}" style="width: 100%; border-radius: 8px; margin-top: 10px; border: 1px solid #222;">
            </div>
        </div>

        <div class="page-content">
            <table class="header-table">
                <tr>
                    <td style="width: 80%;"><h1>🥗 ESTRATEGIA NUTRICIONAL</h1></td>
                    <td style="width: 20%; text-align: right;">{logo_img_html_chico}</td>
                </tr>
            </table>
    """

    for comida, opciones in d['m'].items():
        html += f"""
            <div class="card-glass">
                <h3 style="font-family: 'Bebas Neue'; color: {c_accent}; font-size: 22px; margin: 0 0 10px 0;">🍴 {comida}</h3>
                <table class="data-table">
        """
        for op in opciones:
            html += f"<tr><td>• {op}</td></tr>"
        html += "</table></div>"

    html += f"""
            <div class="card-glass" style="border-top-color: #00BFFF;">
                <h3 style="font-family: 'Bebas Neue'; color: #00BFFF; font-size: 22px; margin: 0 0 10px 0;">💊 SUPLEMENTACIÓN</h3>
                <ul style="margin: 0; color: {c_txt};">
    """
    for suplemento in d['s']:
        html += f'<li style="margin-bottom: 8px;">{suplemento}</li>'
    html += """
                </ul>
            </div>
        </div>
    """

    # PÁGINA 4: ENTRENAMIENTO
    html += f"""
        <div class="page-content">
            <table class="header-table">
                <tr>
                    <td style="width: 80%;"><h1>🏋️‍♂️ PLAN DE ENTRENAMIENTO</h1></td>
                    <td style="width: 20%; text-align: right;">{logo_img_html_chico}</td>
                </tr>
            </table>
    """

    for dia, ejercicios in d['rutina'].items():
        html += f"""
            <div class="card-glass">
                <h3 style="font-family: 'Bebas Neue'; color: {c_accent}; font-size: 22px; margin: 0 0 10px 0;">📅 {dia}</h3>
                <table class="data-table">
        """
        for ej in ejercicios:
            html += f"<tr><td>• {ej}</td></tr>"
        html += "</table></div>"

    # PÁGINA 5: COMPRAS
    html += f"""
        </div>
        <div class="page-content">
            <table class="header-table">
                <tr>
                    <td style="width: 80%;"><h1>🛒 TICKET DE COMPRA MENSUAL</h1></td>
                    <td style="width: 20%; text-align: right;">{logo_img_html_chico}</td>
                </tr>
            </table>
            
            <div class="card-glass">
                <table class="data-table">
    """
    
    for item, cant in d['compras'].items():
        if "Huevo" in item or "Claras" in item:
            unidades = int(cant / 50)
            res = f"<span style='color:{c_accent}; font-weight:bold;'>{unidades} Uni.</span> (~{round(unidades/12, 1)} Doc.)"
        elif any(x in item for x in ["Café", "Mate", "Té", "Infusión"]):
            res = f"<span style='color:{c_accent}; font-weight:bold;'>{int(cant)} Tazas</span>"
        else:
            if cant >= 1000:
                res = f"<span style='color:{c_accent}; font-weight:bold;'>{round(cant/1000, 2)} KG</span>"
            else:
                res = f"<span style='color:{c_accent}; font-weight:bold;'>{int(cant)} g</span>"
                
        html += f"<tr><td style='width: 70%;'><b>{item}</b></td><td style='width: 30%; text-align: right;'>{res}</td></tr>"
    
    html += f"""
                </table>
            </div>
            
            <div style="margin-top: 50px; text-align: center; border-top: 1px solid #333; padding-top: 20px;">
                <p style="font-family: 'Bebas Neue'; font-size: 24px; letter-spacing: 5px; color: {c_accent}; margin: 0;">EDDY PERSONAL TRAINER ELITE</p>
                <p style="font-size: 11px; color: {c_titanio}; margin-top: 5px;">SOFTWARE DE INGENIERÍA CORPORAL • {nombre_edicion}</p>
            </div>
        </div>
    </body></html>
    """
    
    return HTML(string=html).write_pdf()