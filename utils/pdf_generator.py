import streamlit as st
from weasyprint import HTML
import base64

def build_pdf_v60_7(d, grafico_b64, ruta_img, gen):
    # ==========================================\
    # 1. LÓGICA DE EDICIONES LUXURY
    # ==========================================\
    is_f = (gen == "f")
    
    # Colores Base (Ébano absoluto y Blanco)
    c_bg = "#050505"         
    c_card = "#0B0B0B"       
    c_txt = "#F5F5F5"        
    c_titanio = "#878681"    
    
    if is_f:
        # RUBY BLACK ELITE (Femenino)
        c_accent = "#E0115F"     # Rubí Metálico Brillante
        c_dark_accent = "#7A0026" # Sombra rubí
        nombre_edicion = "RUBY BLACK ELITE"
    else:
        # BLACK GOLD ALPHA (Masculino)
        c_accent = "#FFD700"     # Dorado Brillante
        c_dark_accent = "#8B6508" # Sombra dorada
        nombre_edicion = "BLACK GOLD ALPHA"
    
    # Procesar Logo (Glow dinámico)
    logo_img_html_gigante = ""
    logo_img_html_chico = ""
    if ruta_img:
        try:
            with open(ruta_img, "rb") as f:
                b64 = base64.b64encode(f.read()).decode("utf-8")
                # Logo para la portada (GIGANTE Y CENTRADO)
                logo_img_html_gigante = f'<img src="data:image/png;base64,{b64}" style="height: 350px; object-fit: contain; filter: drop-shadow(0 0 25px {c_accent});">'
                # Logo para las páginas interiores (CHICO ARRIBA A LA DERECHA)
                logo_img_html_chico = f'<img src="data:image/png;base64,{b64}" style="height: 60px; filter: drop-shadow(0 0 8px {c_accent});">'
        except:
            pass

    # ==========================================\
    # 2. MAQUETADO CSS TIPO "DASHBOARD" DE AUTO
    # ==========================================\
    html = f"""
    <html>
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Montserrat:wght@300;400;600;800&display=swap" rel="stylesheet">
        <style>
            @page {{ 
                size: A4; 
                margin: 0; /* Sin margen para fondos completos */
                background-color: {c_bg}; 
            }}
            body {{ font-family: 'Montserrat', sans-serif; color: {c_txt}; background-color: {c_bg}; margin: 0; padding: 0; font-size: 10pt; }}
            
            /* --- PORTADA --- */
            .page-cover {{ height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; background: radial-gradient(circle at center, #151515 0%, {c_bg} 100%); padding: 40px; box-sizing: border-box; border-bottom: 4px solid {c_accent}; }}
            .logo-container {{ margin-bottom: 20px; }}
            .cover-title {{ font-family: 'Bebas Neue', cursive; font-size: 75px; letter-spacing: 6px; color: {c_accent}; margin: 10px 0 0 0; text-shadow: 0px 5px 20px {c_dark_accent}; }}
            .cover-subtitle {{ font-family: 'Montserrat', sans-serif; font-size: 12px; letter-spacing: 4px; color: {c_titanio}; margin-bottom: 25px; text-transform: uppercase; }}
            .badge-edicion {{ border: 1px solid {c_accent}; color: {c_txt}; padding: 8px 30px; border-radius: 50px; font-weight: 800; font-size: 14px; letter-spacing: 3px; box-shadow: 0 0 15px {c_dark_accent}; margin-bottom: 40px; background-color: #000; }}
            .cover-name {{ font-family: 'Bebas Neue', cursive; font-size: 55px; color: {c_txt}; letter-spacing: 4px; margin: 0; }}
            .cover-footer {{ margin-top: auto; border-top: 1px solid #333; padding-top: 20px; width: 100%; display: flex; justify-content: space-between; align-items: center; font-size: 10px; color: {c_titanio}; }}

            /* --- PÁGINAS INTERIORES --- */
            .page-content {{ padding: 40px; page-break-before: always; }}
            
            /* Cabecera Interior (Título Izq, Logo Der) */
            .header-interior {{ width: 100%; border-bottom: 1px solid {c_accent}; padding-bottom: 10px; margin-bottom: 20px; display: table; }}
            .header-left {{ display: table-cell; vertical-align: bottom; width: 80%; }}
            .header-right {{ display: table-cell; vertical-align: bottom; text-align: right; width: 20%; }}
            .header-interior h1 {{ font-family: 'Bebas Neue'; font-size: 38px; color: {c_accent}; margin: 0; letter-spacing: 2px; text-shadow: 0 0 10px {c_dark_accent}; }}
            
            /* Tarjetas tipo Dashboard (Cristal oscuro) */
            .dashboard-grid {{ width: 100%; border-collapse: separate; border-spacing: 12px; margin-left: -12px; }}
            .card-glass {{ background: linear-gradient(145deg, #121212, #050505); border: 1px solid #222; border-top: 2px solid {c_accent}; border-radius: 10px; padding: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.8); }}
            
            .metric-title {{ color: {c_txt}; font-size: 11px; font-weight: 600; text-transform: uppercase; margin-bottom: 5px; display: block; }}
            .metric-value {{ font-family: 'Bebas Neue'; font-size: 32px; color: {c_accent}; display: block; text-shadow: 0 0 8px {c_dark_accent}; }}
            
            /* Barras de progreso futuristas */
            .progress-bg {{ width: 100%; background-color: #1a1a1a; height: 6px; border-radius: 3px; margin-top: 8px; overflow: hidden; }}
            .progress-fill {{ background: linear-gradient(90deg, {c_dark_accent}, {c_accent}); height: 100%; }}
            
            /* Tablas de dietas y rutinas */
            .list-card {{ background: {c_card}; border: 1px solid #1a1a1a; border-left: 3px solid {c_accent}; padding: 15px; margin-bottom: 15px; border-radius: 6px; }}
            .list-card h3 {{ font-family: 'Bebas Neue'; color: {c_accent}; font-size: 24px; margin: 0 0 10px 0; letter-spacing: 1px; }}
            .data-table {{ width: 100%; border-collapse: collapse; }}
            .data-table td {{ padding: 10px 5px; border-bottom: 1px solid #151515; font-size: 11px; color: #ddd; }}
        </style>
    </head>
    <body>
        
        <div class="page-cover">
            <div class="logo-container">
                {logo_img_html_gigante}
            </div>
            <h1 class="cover-title">PLAN INTEGRAL ELITE</h1>
            <div class="cover-subtitle">INGENIERÍA CORPORAL DE ALTO VALOR</div>
            
            <div class="badge-edicion">{nombre_edicion}</div>
            
            <h2 class="cover-name">{d['n'].upper()}</h2>
            <p style="color: {c_accent}; font-weight: 600; letter-spacing: 2px; font-size: 12px; margin-top: 5px;">ATLETA DE ÉLITE</p>
            <p style="color: {c_titanio}; font-size: 10px; margin-top: 0;">NIVEL DE ENTRENAMIENTO: {d['nivel'].upper()}</p>
            
            <div class="cover-footer">
                <div>FECHA: {d.get('fecha', 'ACTUAL')}</div>
                <div>POWERED BY EDDY PERSONAL TRAINER ELITE</div>
                <div>FIRMA DIGITAL AUTORIZADA</div>
            </div>
        </div>

        <div class="page-content">
            <div class="header-interior">
                <div class="header-left">
                    <h1>📈 ANALÍTICA FÍSICA Y OBJETIVOS</h1>
                </div>
                <div class="header-right">
                    {logo_img_html_chico}
                </div>
            </div>

            <table class="dashboard-grid">
                <tr>
                    <td class="card-glass" style="width: 25%;">
                        <span class="metric-title">ESTATURA</span>
                        <span class="metric-value">{d['estatura']} CM</span>
                        <div class="progress-bg"><div class="progress-fill" style="width: 70%;"></div></div>
                    </td>
                    <td class="card-glass" style="width: 25%;">
                        <span class="metric-title">PESO ACTUAL</span>
                        <span class="metric-value">{d['peso']} KG</span>
                        <div class="progress-bg"><div class="progress-fill" style="width: 80%;"></div></div>
                    </td>
                    <td class="card-glass" style="width: 25%;">
                        <span class="metric-title">ÍNDICE RCC</span>
                        <span class="metric-value">{d['rcc']}</span>
                        <div class="progress-bg"><div class="progress-fill" style="width: 60%;"></div></div>
                    </td>
                    <td class="card-glass" style="width: 25%;">
                        <span class="metric-title">GRASA EST.</span>
                        <span class="metric-value">{d['rfm']}%</span>
                        <div class="progress-bg"><div class="progress-fill" style="width: 40%;"></div></div>
                    </td>
                </tr>
            </table>

            <table class="dashboard-grid">
                <tr>
                    <td class="card-glass" style="width: 50%;">
                        <span class="metric-title" style="color: {c_titanio};">OBJETIVO ESTRATÉGICO</span>
                        <span class="metric-value" style="font-size: 40px; color: #fff;">{d['meta'].upper()}</span>
                        <p style="color: {c_titanio}; font-size: 10px; margin: 5px 0 0 0;">CINTURA: {d['cintura']} CM | CADERA: {d['cadera']} CM</p>
                    </td>
                    <td class="card-glass" style="width: 25%;">
                        <span class="metric-title">KCAL DIARIAS</span>
                        <span class="metric-value">{d['k']:.0f}</span>
                        <div class="progress-bg"><div class="progress-fill" style="width: 100%;"></div></div>
                    </td>
                    <td class="card-glass" style="width: 25%;">
                        <span class="metric-title">HIDRATACIÓN</span>
                        <span class="metric-value">{d['w']} LTS</span>
                        <div class="progress-bg"><div class="progress-fill" style="width: 100%; background: linear-gradient(90deg, #0055ff, #00bfff);"></div></div>
                    </td>
                </tr>
            </table>

            <div class="card-glass" style="margin-top: 15px; text-align: center;">
                <span class="metric-title" style="margin-bottom: 15px;">DISTRIBUCIÓN DE MACRONUTRIENTES</span>
                <div style="display: flex; width: 100%; gap: 10px;">
                    <div style="flex: 1; background: #111; padding: 10px; border-radius: 5px;">
                        <span style="color: #fff; font-size: 10px;">PROTEÍNA</span><br>
                        <span class="metric-value" style="font-size: 24px;">{d['p']:.0f}g</span>
                    </div>
                    <div style="flex: 1; background: #111; padding: 10px; border-radius: 5px;">
                        <span style="color: #fff; font-size: 10px;">CARBOHIDRATOS</span><br>
                        <span class="metric-value" style="font-size: 24px;">{d['c']:.0f}g</span>
                    </div>
                    <div style="flex: 1; background: #111; padding: 10px; border-radius: 5px;">
                        <span style="color: #fff; font-size: 10px;">GRASAS</span><br>
                        <span class="metric-value" style="font-size: 24px;">{d['g']:.0f}g</span>
                    </div>
                </div>
            </div>

            <div class="card-glass" style="margin-top: 25px; text-align: center;">
                <span class="metric-title">PROYECCIÓN GRÁFICA DE EVOLUCIÓN</span>
                <img src="data:image/png;base64,{grafico_b64}" style="width: 100%; border-radius: 8px; margin-top: 10px; border: 1px solid #222;">
            </div>
        </div>

        <div class="page-content">
            <div class="header-interior">
                <div class="header-left">
                    <h1>🥗 ESTRATEGIA NUTRICIONAL</h1>
                </div>
                <div class="header-right">
                    {logo_img_html_chico}
                </div>
            </div>
    """

    # --- BUCLE DE COMIDAS (Diseño Cajas separadas) ---
    for comida, opciones in d['m'].items():
        html += f"""
            <div class="list-card">
                <h3>🍴 {comida}</h3>
                <table class="data-table">
        """
        for op in opciones:
            html += f"<tr><td>• {op}</td></tr>"
            
        html += """
                </table>
            </div>
        """

    # --- BUCLE DE SUPLEMENTACIÓN ---
    html += f"""
            <div class="list-card" style="border-left-color: #00bfff;">
                <h3 style="color: #00bfff;">💊 SUPLEMENTACIÓN Y MICRONUTRIENTES</h3>
                <ul style="margin: 10px 0 0 0; color: #ddd; font-size: 11px;">
    """
    for suplemento in d['s']:
        html += f'<li style="margin-bottom: 8px;">{suplemento}</li>'
        
    html += """
                </ul>
            </div>
        </div>
    """

    # ==========================================\
    # PÁGINA 4: ENTRENAMIENTO
    # ==========================================\
    html += f"""
        <div class="page-content">
            <div class="header-interior">
                <div class="header-left">
                    <h1>🏋️‍♂️ PLAN DE ENTRENAMIENTO</h1>
                </div>
                <div class="header-right">
                    {logo_img_html_chico}
                </div>
            </div>
            <p style="color: {c_titanio}; font-size: 12px; margin-top: -10px; margin-bottom: 20px;">ESTRUCTURA DE {d['dias']} DÍAS | TIPO: {d['entreno'].upper()}</p>
    """

    # BUCLE DE RUTINAS
    for dia, ejercicios in d['rutina'].items():
        html += f"""
            <div class="list-card">
                <h3>📅 {dia}</h3>
                <table class="data-table">
        """
        for ej in ejercicios:
            html += f"<tr><td>• {ej}</td></tr>"
            
        html += """
                </table>
            </div>
        """

    # ==========================================\
    # PÁGINA 5: TICKET DE COMPRAS
    # ==========================================\
    html += f"""
        </div>
        <div class="page-content">
            <div class="header-interior">
                <div class="header-left">
                    <h1>🛒 TICKET DE COMPRA MENSUAL</h1>
                </div>
                <div class="header-right">
                    {logo_img_html_chico}
                </div>
            </div>
            
            <div class="list-card">
                <table class="data-table">
    """
    
    # BUCLE DE COMPRAS
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
            
            <div style="margin-top: 60px; text-align: center; border-top: 1px solid #333; padding-top: 30px;">
                <p style="font-family: 'Bebas Neue'; font-size: 26px; letter-spacing: 5px; color: {c_accent}; margin: 0;">EDDY PERSONAL TRAINER ELITE</p>
                <p style="font-size: 11px; color: {c_titanio}; margin-top: 5px;">SOFTWARE DE INGENIERÍA CORPORAL • {nombre_edicion}</p>
            </div>
        </div>
    </body></html>
    """
    
    return HTML(string=html).write_pdf()