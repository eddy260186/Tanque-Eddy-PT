import streamlit as st
from weasyprint import HTML
import base64

def build_pdf_v60_7(d, grafico_b64, ruta_img, gen):
    # ==========================================\
    # LÓGICA DE EDICIONES LUXURY: ALPHA vs RUBY
    # ==========================================\
    is_f = (gen == "f")
    
    # --- PALETA BASE PREMIUM ---
    c_bg = "#050505"         
    c_card = "#0B0B0B"       
    c_txt = "#F5F5F5"        
    c_titanio = "#878681"    
    
    if is_f:
        # --- EDICIÓN RUBY BLACK ELITE ---
        c_accent = "#C0104A"     
        c_bright = "#E0115F"     
        nombre_edicion = "RUBY BLACK ELITE"
    else:
        # --- EDICIÓN BLACK GOLD ALPHA ---
        c_accent = "#D4AF37"     
        c_bright = "#FFD700"     
        nombre_edicion = "BLACK GOLD ALPHA"
    
    # --- LOGO DINÁMICO ---
    logo_img_html = ""
    if ruta_img:
        with open(ruta_img, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
            logo_img_html = f'<img src="data:image/png;base64,{b64}" style="height: 80px; filter: drop-shadow(0 0 10px {c_accent});">'

    # ==========================================\
    # MAQUETADO HTML Y CSS LUXURY
    # ==========================================\
    html = f"""
    <html>
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Montserrat:wght@300;400;700&display=swap" rel="stylesheet">
        <style>
            @page {{ size: A4; margin: 10mm; background-color: {c_bg}; }}
            body {{ font-family: 'Montserrat', sans-serif; color: {c_txt}; background-color: {c_bg}; margin: 0; padding: 0; font-size: 12px; }}
            
            /* PORTADA Y CABECERAS */
            .cover {{ height: 90vh; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; background: radial-gradient(circle at center, #111 0%, {c_bg} 100%); }}
            .cover h1 {{ font-family: 'Bebas Neue', cursive; font-size: 60px; letter-spacing: 8px; color: {c_accent}; margin: 20px 0; text-shadow: 0px 4px 10px rgba(0,0,0,0.8); }}
            .badge {{ border: 1px solid {c_accent}; color: {c_txt}; padding: 8px 20px; border-radius: 30px; font-weight: 700; letter-spacing: 2px; box-shadow: 0 0 10px {c_accent}40; }}
            
            .header-table {{ width: 100%; border-bottom: 2px solid {c_accent}; padding-bottom: 15px; margin-bottom: 20px; }}
            .header-table h1 {{ font-family: 'Bebas Neue'; font-size: 30px; color: {c_txt}; margin: 0; letter-spacing: 2px; }}
            
            /* CARDS PREMIUM */
            .card-elite {{ background: {c_card}; border: 1px solid #1A1A1A; border-left: 4px solid {c_accent}; border-radius: 8px; padding: 20px; margin-bottom: 20px; box-shadow: 0 5px 15px rgba(0,0,0,0.5); }}
            
            /* TABLAS E INTERIORES */
            table {{ width: 100%; border-collapse: collapse; }}
            .data-table td {{ padding: 12px; border-bottom: 1px solid #1a1a1a; font-size: 11px; }}
            .grid-table td {{ padding: 10px; vertical-align: top; }}
            
            .accent-text {{ color: {c_accent}; font-weight: bold; }}
            .bright-text {{ color: {c_bright}; font-family: 'Bebas Neue'; font-size: 20px; letter-spacing: 1px; }}
            .label-sm {{ color: {c_titanio}; font-size: 10px; display: block; margin-bottom: 2px; text-transform: uppercase; }}
            
            h2 {{ font-family: 'Bebas Neue'; font-size: 26px; color: {c_accent}; letter-spacing: 1px; margin-top: 0; border-bottom: 1px solid #222; padding-bottom: 10px; }}
            h3 {{ font-family: 'Bebas Neue'; font-size: 20px; color: {c_bright}; margin: 15px 0 5px 0; }}
            ul {{ padding-left: 20px; }}
            li {{ margin-bottom: 8px; color: {c_txt}; }}
        </style>
    </head>
    <body>
        
        <div class="cover">
            {logo_img_html}
            <h1>PLAN INTEGRAL ELITE</h1>
            <div class="badge">{nombre_edicion}</div>
            <p style="letter-spacing: 4px; font-weight: 300; color: {c_titanio}; margin-top: 30px;">INGENIERÍA CORPORAL DE ALTO VALOR</p>
            <div style="margin-top: 50px; border-top: 1px solid {c_titanio}; padding-top: 20px;">
                <span class="label-sm">ATLETA DE ÉLITE</span>
                <span class="accent-text" style="font-size: 24px;">{d['n'].upper()}</span>
                <span class="label-sm" style="margin-top: 15px;">NIVEL DE ENTRENAMIENTO: {d['nivel'].upper()}</span>
            </div>
        </div>

        <div style="page-break-before: always;"></div>

        <table class="header-table">
            <tr>
                <td><h1>👤 PERFIL FÍSICO Y BIOMÉTRICO</h1><span class="accent-text">ANÁLISIS DE PARTIDA</span></td>
                <td style="text-align: right;">{logo_img_html}</td>
            </tr>
        </table>

        <div class="card-elite">
            <table class="grid-table">
                <tr>
                    <td><span class="label-sm">EDAD</span><span class="accent-text">{d['edad']} AÑOS</span></td>
                    <td><span class="label-sm">ESTATURA</span><span class="accent-text">{d['estatura']} CM</span></td>
                    <td><span class="label-sm">PESO ACTUAL</span><span class="accent-text">{d['peso']} KG</span></td>
                </tr>
                <tr>
                    <td><span class="label-sm">CINTURA</span><span class="accent-text">{d['cintura']} CM</span></td>
                    <td><span class="label-sm">CADERA</span><span class="accent-text">{d['cadera']} CM</span></td>
                    <td><span class="label-sm">ÍNDICE RCC</span><span class="accent-text">{d['rcc']}</span></td>
                </tr>
                <tr>
                    <td><span class="label-sm">GRASA ESTIMADA</span><span class="accent-text">{d['rfm']}%</span></td>
                    <td><span class="label-sm">META PRINCIPAL</span><span class="accent-text">{d['meta']}</span></td>
                    <td><span class="label-sm">ESTILO DE DIETA</span><span class="accent-text">{d['dt']}</span></td>
                </tr>
                <tr>
                    <td colspan="3"><span class="label-sm">ESTRUCTURA DE ENTRENAMIENTO</span><span class="accent-text">{d['entreno']} ({d['dias']} DÍAS/SEM)</span></td>
                </tr>
            </table>
        </div>

        <div class="card-elite">
            <h2>📊 BALANCE NUTRICIONAL (KATCH-MCARDLE)</h2>
            <table class="grid-table">
                <tr>
                    <td><span class="label-sm">CALORÍAS OBJETIVO</span><span class="bright-text">{d['k']:.0f} KCAL</span></td>
                    <td><span class="label-sm">SUMATORIA DEL MENÚ</span><span class="bright-text" style="color: #00FF00;">{d['k']:.0f} KCAL ✅</span></td>
                    <td><span class="label-sm">HIDRATACIÓN DIARIA</span><span class="bright-text" style="color: #00BFFF;">💧 {d['w']} LTS</span></td>
                </tr>
            </table>
            <div style="margin-top: 15px; border-top: 1px dashed #333; padding-top: 15px;">
                <span class="label-sm">MACROS DIARIOS ESTRATÉGICOS</span>
                <span class="accent-text">PROTEÍNA: {d['p']:.0f}g &nbsp;|&nbsp; CARBOHIDRATOS: {d['c']:.0f}g &nbsp;|&nbsp; GRASAS: {d['g']:.0f}g</span>
            </div>
        </div>

        <div class="card-elite" style="text-align: center;">
            <span class="label-sm" style="margin-bottom: 10px;">📈 PROYECCIÓN DE PESO ESTIMADA</span>
            <img src="data:image/png;base64,{grafico_b64}" style="width: 100%; border-radius: 5px; border: 1px solid #222;">
        </div>

        <div style="page-break-before: always;"></div>

        <table class="header-table">
            <tr>
                <td><h1>🥗 ESTRATEGIA NUTRICIONAL</h1><span class="accent-text">MENÚ Y SUPLEMENTACIÓN</span></td>
                <td style="text-align: right;">{logo_img_html}</td>
            </tr>
        </table>
    """
    
    # BUCLE EXACTO DE COMIDAS
    for c, ops in d['m'].items():
        html += f"""
        <div class="card-elite">
            <h3 style="margin-top: 0;">🍴 {c}</h3>
            <table class='data-table'>"""
        for o in ops:
            html += f"<tr><td>{o}</td></tr>"
        html += "</table></div>"
    
    # BUCLE EXACTO DE SUPLEMENTACIÓN
    html += f"""
        <div class="card-elite" style="border-left-color: #00BFFF;">
            <h2 style="color: #00BFFF; margin-bottom: 15px;">💊 SUPLEMENTACIÓN Y MICRONUTRIENTES</h2>
            <ul>"""
    for s in d['s']:
        html += f"<li>{s}</li>"
    html += f"""</ul>
        </div>
        
        <div style="page-break-before: always;"></div>

        <table class="header-table">
            <tr>
                <td><h1>🏋️‍♂️ PLAN DE ENTRENAMIENTO</h1><span class="accent-text">DISTRIBUCIÓN {d['nivel'].upper()}</span></td>
                <td style="text-align: right;">{logo_img_html}</td>
            </tr>
        </table>
    """
    
    # BUCLE EXACTO DE RUTINAS
    for dia, ejercicios in d['rutina'].items():
        html += f"""
        <div class="card-elite">
            <h3 style="margin-top: 0;">📅 {dia}</h3>
            <table class='data-table'>"""
        for e in ejercicios:
            html += f"<tr><td>{e}</td></tr>"
        html += "</table></div>"
        
    html += f"""
        <div style="page-break-before: always;"></div>

        <table class="header-table">
            <tr>
                <td><h1>🛒 TICKET DE COMPRA MENSUAL</h1><span class="accent-text">LISTA AUTOMATIZADA PARA 30 DÍAS</span></td>
                <td style="text-align: right;">{logo_img_html}</td>
            </tr>
        </table>
        
        <div class="card-elite">
            <table class='data-table'>"""
    
    # BUCLE EXACTO DE COMPRAS CON TU FÓRMULA MATEMÁTICA
    for item, cant in d['compras'].items():
        if "Huevo" in item or "Claras" in item:
            unidades = int(cant / 50)
            res = f"<span class='accent-text'>{unidades} Unidades</span> (~{round(unidades/12, 1)} Docenas)"
        elif any(x in item for x in ["Café", "Mate", "Té", "Infusión"]):
            res = f"<span class='accent-text'>{int(cant)} Porciones/Tazas</span>"
        else:
            if cant >= 1000:
                res = f"<span class='accent-text'>{round(cant/1000, 2)} KG</span>"
            else:
                res = f"<span class='accent-text'>{int(cant)} g</span>"
        html += f"<tr><td><b>{item}</b></td><td style='text-align: right;'>{res}</td></tr>"
    
    html += f"""
            </table>
        </div>
        
        <div style="margin-top: 40px; text-align: center; border-top: 1px solid {c_titanio}; padding-top: 20px;">
            <p style="font-family: 'Bebas Neue'; font-size: 20px; letter-spacing: 3px; margin: 0;">EDDY PERSONAL TRAINER ELITE</p>
            <p style="font-size: 10px; color: {c_titanio}; margin-top: 5px;">INSTAGRAM: @EDDY_PERSONAL_TRAINER | MORENO, BUENOS AIRES</p>
        </div>
    </body></html>"""
    
    return HTML(string=html).write_pdf()