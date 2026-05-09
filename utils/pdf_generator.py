import streamlit as st
from weasyprint import HTML
import base64

def build_pdf_v60_7(d, grafico_b64, ruta_img, gen):
    # ==========================================\
    # 1. LÓGICA DE EDICIONES LUXURY
    # ==========================================\
    is_f = (gen == "f")
    
    # Colores Base (Ébano y Blanco Suave)
    c_bg = "#050505"         
    c_card = "#0B0B0B"       
    c_txt = "#F5F5F5"        
    c_titanio = "#878681"    
    
    if is_f:
        # RUBY PINK EDITION (Femenino)
        c_accent = "#9B111E"     # Rubí Metálico
        c_bright = "#D10022"     # Rubí Brillante
        nombre_edicion = "RUBY PINK EDITION"
    else:
        # BLACK GOLD ALPHA (Masculino)
        c_accent = "#D4AF37"     # Dorado Metálico
        c_bright = "#FFD700"     # Dorado Brillante
        nombre_edicion = "BLACK GOLD ALPHA"
    
    # Procesar Logo con Glow dinámico
    logo_img_html = ""
    if ruta_img:
        with open(ruta_img, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
            logo_img_html = f'<img src="data:image/png;base64,{b64}" style="height: 80px; filter: drop-shadow(0 0 10px {c_accent});">'

    # ==========================================\
    # 2. MAQUETADO CSS DE ALTA GAMA
    # ==========================================\
    html = f"""
    <html>
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Montserrat:wght@300;400;700&display=swap" rel="stylesheet">
        <style>
            @page {{ size: A4; margin: 10mm; background-color: {c_bg}; }}
            body {{ font-family: 'Montserrat', sans-serif; color: {c_txt}; background-color: {c_bg}; margin: 0; padding: 0; font-size: 11pt; }}
            .cover {{ height: 92vh; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; background: radial-gradient(circle at center, #111 0%, {c_bg} 100%); border-bottom: 3px solid {c_accent}; }}
            .cover h1 {{ font-family: 'Bebas Neue', cursive; font-size: 65px; letter-spacing: 10px; color: {c_accent}; margin: 20px 0; text-shadow: 0px 4px 15px rgba(0,0,0,0.8); }}
            .badge {{ border: 1px solid {c_accent}; color: {c_txt}; padding: 10px 25px; border-radius: 40px; font-weight: 700; letter-spacing: 3px; box-shadow: 0 0 15px {c_accent}30; }}
            .section {{ padding: 30px 40px; page-break-before: always; }}
            .header-table {{ width: 100%; border-bottom: 2px solid {c_accent}; padding-bottom: 15px; margin-bottom: 25px; }}
            .header-table h1 {{ font-family: 'Bebas Neue'; font-size: 32px; color: {c_txt}; margin: 0; letter-spacing: 3px; }}
            .card-elite {{ background: {c_card}; border: 1px solid #1A1A1A; border-left: 5px solid {c_accent}; border-radius: 12px; padding: 25px; margin-bottom: 25px; box-shadow: 0 10px 25px rgba(0,0,0,0.6); }}
            table {{ width: 100%; border-collapse: collapse; }}
            .data-table td {{ padding: 14px; border-bottom: 1px solid #1a1a1a; font-size: 10.5pt; }}
            .grid-table td {{ padding: 10px; vertical-align: top; }}
            .accent-text {{ color: {c_accent}; font-weight: bold; }}
            .bright-text {{ color: {c_bright}; font-family: 'Bebas Neue'; font-size: 24px; letter-spacing: 1px; }}
            .label-sm {{ color: {c_titanio}; font-size: 9px; display: block; margin-bottom: 3px; text-transform: uppercase; letter-spacing: 1px; }}
            h2 {{ font-family: 'Bebas Neue'; font-size: 28px; color: {c_accent}; letter-spacing: 2px; margin: 0 0 15px 0; }}
            h3 {{ font-family: 'Bebas Neue'; font-size: 22px; color: {c_bright}; margin: 20px 0 10px 0; border-bottom: 1px solid #333; padding-bottom: 5px; }}
        </style>
    </head>
    <body>
        
        <div class="cover">
            {logo_img_html}
            <h1>PLAN INTEGRAL ELITE</h1>
            <div class="badge">{nombre_edicion}</div>
            <p style="letter-spacing: 5px; font-weight: 300; color: {c_titanio}; margin-top: 40px; font-size: 14px;">TRANSFORMACIÓN FÍSICA PROFESIONAL</p>
            <div style="margin-top: 60px; border-top: 1px solid #333; padding-top: 25px; width: 350px;">
                <span class="label-sm">ATLETA SELECCIONADO</span>
                <span class="accent-text" style="font-size: 28px;">{d['n'].upper()}</span>
                <p style="color: {c_titanio}; font-size: 11px; margin-top: 20px;">NIVEL DE ENTRENAMIENTO: {d['nivel'].upper()}</p>
            </div>
        </div>

        <div class="section">
            <table class="header-table">
                <tr>
                    <td><h1>📈 ANALÍTICA CORPORAL</h1><span class="accent-text">ESTADO INICIAL Y MÉTRICAS</span></td>
                    <td style="text-align: right;">{logo_img_html}</td>
                </tr>
            </table>

            <div class="card-elite">
                <table class="grid-table">
                    <tr>
                        <td><span class="label-sm">EDAD</span><span class="accent-text" style="font-size: 18px;">{d['edad']} AÑOS</span></td>
                        <td><span class="label-sm">ESTATURA</span><span class="accent-text" style="font-size: 18px;">{d['estatura']} CM</span></td>
                        <td><span class="label-sm">PESO</span><span class="accent-text" style="font-size: 18px;">{d['peso']} KG</span></td>
                    </tr>
                    <tr>
                        <td style="padding-top: 20px;"><span class="label-sm">CINTURA</span><span class="accent-text">{d['cintura']} CM</span></td>
                        <td style="padding-top: 20px;"><span class="label-sm">CADERA</span><span class="accent-text">{d['cadera']} CM</span></td>
                        <td style="padding-top: 20px;"><span class="label-sm">ÍNDICE RCC</span><span class="accent-text">{d['rcc']}</span></td>
                    </tr>
                    <tr>
                        <td style="padding-top: 20px;"><span class="label-sm">ESTILO DE DIETA</span><span class="accent-text">{d['dt']}</span></td>
                        <td style="padding-top: 20px;"><span class="label-sm">ESTRUCTURA DE ENTRENO</span><span class="accent-text">{d['entreno']}</span></td>
                        <td style="padding-top: 20px;"><span class="label-sm">FRECUENCIA</span><span class="accent-text">{d['dias']} DÍAS/SEM</span></td>
                    </tr>
                </table>
            </div>

            <div class="card-elite" style="border-color: {c_bright};">
                <h2 style="color: {c_bright};">🎯 OBJETIVO: {d['meta'].upper()}</h2>
                <table class="grid-table">
                    <tr>
                        <td><span class="label-sm">CALORÍAS DIARIAS</span><span class="bright-text">{d['k']:.0f} KCAL</span></td>
                        <td><span class="label-sm">HIDRATACIÓN DIARIA</span><span class="bright-text">💧 {d['w']} LTS</span></td>
                        <td><span class="label-sm">GRASA RFM ESTIMADA</span><span class="bright-text">{d['rfm']}%</span></td>
                    </tr>
                </table>
                <div style="margin-top: 20px; border-top: 1px solid #222; padding-top: 15px;">
                    <span class="label-sm">DISTRIBUCIÓN DE MACROS EXACTA</span>
                    <span style="font-weight: bold; letter-spacing: 1px;">PROTEÍNA: {d['p']:.0f}g | CARBOS: {d['c']:.0f}g | GRASAS: {d['g']:.0f}g</span>
                </div>
            </div>

            <div class="card-elite" style="text-align: center;">
                <span class="label-sm" style="margin-bottom: 10px;">PROYECCIÓN DE PESO ESTIMADA</span>
                <img src="data:image/png;base64,{grafico_b64}" style="width: 100%; border-radius: 8px; border: 1px solid #222;">
            </div>
        </div>

        <div class="section">
            <table class="header-table">
                <tr>
                    <td><h1>🥗 ESTRATEGIA NUTRICIONAL</h1><span class="accent-text">ALIMENTACIÓN Y SUPLEMENTOS</span></td>
                    <td style="text-align: right;">{logo_img_html}</td>
                </tr>
            </table>
    """

    # --- BUCLE DE COMIDAS (100% Seguro) ---
    for comida, opciones in d['m'].items():
        html += f"""
            <div class="card-elite">
                <h3>🍴 {comida}</h3>
                <table class="data-table">
        """
        for op in opciones:
            html += f"<tr><td>{op}</td></tr>"
            
        html += """
                </table>
            </div>
        """

    # --- BUCLE DE SUPLEMENTACIÓN (100% Seguro) ---
    html += f"""
            <div class="card-elite" style="border-left-color: {c_bright};">
                <h2 style="color: {c_bright};">💊 PROTOCOLO DE SUPLEMENTACIÓN</h2>
                <ul style="margin: 10px 0 0 0; color: {c_txt};">
    """
    
    for suplemento in d['s']:
        html += f'<li style="margin-bottom: 10px;">{suplemento}</li>'
        
    html += """
                </ul>
            </div>
        </div>
    """

    # ==========================================\
    # PÁGINA 4: ENTRENAMIENTO
    # ==========================================\
    html += f"""
        <div class="section">
            <table class="header-table">
                <tr>
                    <td><h1>🏋️‍♂️ PLAN DE ENTRENAMIENTO</h1><span class="accent-text">ESTRUCTURA DE {d['dias']} DÍAS</span></td>
                    <td style="text-align: right;">{logo_img_html}</td>
                </tr>
            </table>
    """

    # --- BUCLE DE RUTINAS (100% Seguro) ---
    for dia, ejercicios in d['rutina'].items():
        html += f"""
            <div class="card-elite">
                <h3>📅 {dia}</h3>
                <table class="data-table">
        """
        for ej in ejercicios:
            html += f"<tr><td>{ej}</td></tr>"
            
        html += """
                </table>
            </div>
        """

    # ==========================================\
    # PÁGINA 5: COMPRAS AUTOMATIZADAS
    # ==========================================\
    html += f"""
        </div>
        <div class="section">
            <table class="header-table">
                <tr>
                    <td><h1>🛒 TICKET DE COMPRA MENSUAL</h1><span class="accent-text">LISTA AUTOMATIZADA - 30 DÍAS</span></td>
                    <td style="text-align: right;">{logo_img_html}</td>
                </tr>
            </table>
            
            <div class="card-elite">
                <table class="data-table">
    """
    
    # --- BUCLE DE LISTA DE COMPRAS (Con cálculo de Huevos, infusiones y kilos) ---
    for item, cant in d['compras'].items():
        if "Huevo" in item or "Claras" in item:
            unidades = int(cant / 50)
            res = f"<span class='accent-text'>{unidades} Uni.</span> (~{round(unidades/12, 1)} Doc.)"
        elif any(x in item for x in ["Café", "Mate", "Té", "Infusión"]):
            res = f"<span class='accent-text'>{int(cant)} Tazas</span>"
        else:
            if cant >= 1000:
                res = f"<span class='accent-text'>{round(cant/1000, 2)} KG</span>"
            else:
                res = f"<span class='accent-text'>{int(cant)} g</span>"
                
        html += f"<tr><td><b>{item}</b></td><td style='text-align: right;'>{res}</td></tr>"
    
    # --- CIERRE FINAL DEL PDF Y FIRMA ---
    html += f"""
                </table>
            </div>
            
            <div style="margin-top: 60px; text-align: center; border-top: 1px solid #333; padding-top: 30px;">
                <p style="font-family: 'Bebas Neue'; font-size: 24px; letter-spacing: 5px; color: {c_accent};">EDDY PERSONAL TRAINER ELITE</p>
                <p style="font-size: 11px; color: {c_titanio}; margin-top: 8px;">MORENO • BUENOS AIRES • {nombre_edicion}</p>
            </div>
        </div>
    </body></html>
    """
    
    return HTML(string=html).write_pdf()