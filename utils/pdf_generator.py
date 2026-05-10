import os
import base64
from weasyprint import HTML

# =========================================================
# EDDY PT ELITE - MOTOR PDF ULTRA-PREMIUM V9.5 (TABLAS)
# =========================================================

def build_pdf_v60_7(d, grafico_b64, ruta_img, gen):
    # 1. CONFIGURACIÓN DE GÉNERO Y TEMAS (ALTO CONTRASTE)
    is_f = (gen == "f")
    c_bg = "#050505"
    c_card = "#111111"
    c_txt = "#FFFFFF"
    c_soft = "#9E9E9E"
    
    if is_f:
        c_acc = "#D81B60" # Rubí Sólido
        ruta_logo = "logo_rosa.png"
        edition = "RUBY BLACK ELITE"
    else:
        c_acc = "#D4AF37" # Dorado Sólido
        ruta_logo = "logo_dorado.png"
        edition = "BLACK GOLD ALPHA"

    # 2. PROCESAMIENTO DE IMÁGENES (LOGOS Y QR)
    def get_b64(path):
        if path and os.path.exists(path):
            with open(path, "rb") as f:
                return base64.b64encode(f.read()).decode("utf-8")
        return ""

    logo_final = ruta_logo if os.path.exists(ruta_logo) else ruta_img
    logo_b64 = get_b64(logo_final)
    qr_b64 = get_b64("qr_code.png")

    img_logo_main = f'<img src="data:image/png;base64,{logo_b64}" style="height:320px;">' if logo_b64 else ""
    img_logo_sm = f'<img src="data:image/png;base64,{logo_b64}" style="height:85px;">' if logo_b64 else ""
    
    qr_html = f'<img src="data:image/png;base64,{qr_b64}" style="width:75px; border:2px solid {c_acc}; border-radius:8px;">' if qr_b64 else f'<div style="width:70px; height:70px; border:1px solid {c_acc}; color:{c_acc}; font-size:10px; line-height:70px; text-align:center;">QR</div>'
    # 3. CSS (DISEÑO ORIENTADO A TABLAS PARA EVITAR ENCIMAMIENTO)
    css_styles = f"""
    <style>
        @page {{ size: A4; margin: 0; background: {c_bg}; }}
        * {{ box-sizing: border-box; }}
        body {{ font-family: 'Montserrat', sans-serif; color: {c_txt}; margin: 0; padding: 0; line-height: 1.5; }}
        
        .page {{ padding: 45px; page-break-before: always; position: relative; }}
        .cover {{ height: 100vh; text-align: center; padding-top: 80px; position: relative; }}
        
        .title-elite {{ font-family: 'Bebas Neue'; font-size: 65px; color: {c_acc}; letter-spacing: 6px; margin: 0; }}
        .sub-title {{ color: {c_soft}; letter-spacing: 4px; font-size: 13px; font-weight: 700; text-transform: uppercase; }}
        
        .badge {{ margin: 30px auto; padding: 12px 35px; border-radius: 40px; border: 2px solid {c_acc}; color: {c_txt}; font-weight: bold; letter-spacing: 3px; display: inline-block; }}
        
        /* TABLAS DE ESTRUCTURA (LA CLAVE PARA QUE NO SE ROMPA) */
        .layout-table {{ width: 100%; border-collapse: separate; border-spacing: 15px; margin-left: -15px; margin-right: -15px; table-layout: fixed; }}
        .card-td {{ background: {c_card}; border-top: 4px solid {c_acc}; padding: 22px 10px; border-radius: 12px; text-align: center; vertical-align: middle; }}
        
        .lbl {{ font-size: 10px; color: {c_soft}; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 5px; }}
        .val {{ font-family: 'Bebas Neue'; font-size: 34px; color: {c_txt}; margin-top: 5px; }}
        
        .list-container {{ background: {c_card}; border-left: 5px solid {c_acc}; padding: 25px; margin-bottom: 22px; border-radius: 10px; }}
        .list-title {{ font-family: 'Bebas Neue'; font-size: 26px; color: {c_acc}; margin-bottom: 12px; }}
        .list-item {{ font-size: 12px; border-bottom: 1px solid #222; padding: 12px 0; color: #E0E0E0; }}
        
        .footer-table {{ width: 100%; position: absolute; bottom: 45px; left: 0; padding: 0 45px; }}
        .signature {{ font-family: 'Great Vibes'; font-size: 38px; color: {c_soft}; }}
    </style>
    """
    # 4. CONSTRUCCIÓN DE PORTADA
    html = f"""
    <html>
    <head>
    <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Montserrat:wght@400;700&family=Great+Vibes&display=swap" rel="stylesheet">
    {css_styles}
    </head>
    <body>
    <div class="cover">
        {img_logo_main}
        <h1 class="title-elite">PLAN INTEGRAL ELITE</h1>
        <div class="sub-title">INGENIERÍA CORPORAL DE ALTO VALOR</div>
        <div class="badge">{edition}</div>
        <div style="margin-top:40px; border-top:1px solid #333; border-bottom:1px solid #333; padding:25px 0; width:75%; margin-left:12.5%;">
            <div class="lbl" style="color:{c_acc}; font-size:13px;">ATLETA DE ÉLITE</div>
            <div style="font-family:'Bebas Neue'; font-size:52px; margin:10px 0;">{str(d.get('n', '')).upper()}</div>
            <div class="lbl">NIVEL DE ENTRENAMIENTO: {str(d.get('nivel', '')).upper()}</div>
        </div>
        <table class="footer-table">
            <tr>
                <td style="text-align:left;">{qr_html}</td>
                <td style="text-align:center;"><div class="lbl">POWERED BY EDDY PT ELITE</div></td>
                <td style="text-align:right;"><div class="signature">Eddy Personal Trainer</div></td>
            </tr>
        </table>
    </div>

    <div class="page">
        <table style="width:100%; border-bottom:2px solid #222; padding-bottom:15px; margin-bottom:25px;">
            <tr>
                <td style="text-align:left;"><h1 class="title-elite" style="font-size:38px;">ANALÍTICA FÍSICA</h1></td>
                <td style="text-align:right;">{img_logo_sm}</td>
            </tr>
        </table>
        <table class="layout-table">
            <tr>
                <td class="card-td"><div class="lbl">EDAD</div><div class="val">{d.get('edad','')}</div></td>
                <td class="card-td"><div class="lbl">ESTATURA</div><div class="val">{d.get('estatura','')} CM</div></td>
                <td class="card-td"><div class="lbl">PESO</div><div class="val">{d.get('peso','')} KG</div></td>
                <td class="card-td"><div class="lbl">GRASA</div><div class="val" style="color:{c_acc};">{d.get('rfm','')}%</div></td>
            </tr>
            <tr>
                <td class="card-td"><div class="lbl">CINTURA</div><div class="val">{d.get('cintura','')} CM</div></td>
                <td class="card-td"><div class="lbl">CADERA</div><div class="val">{d.get('cadera','')} CM</div></td>
                <td class="card-td"><div class="lbl">RCC</div><div class="val">{d.get('rcc','')}</div></td>
                <td class="card-td" style="border-top-color:#00BFFF;"><div class="lbl" style="color:#00BFFF;">HIDRATACIÓN</div><div class="val" style="color:#00BFFF;">{d.get('w','')} L</div></td>
            </tr>
        </table>
        <div class="list-container" style="text-align:center; border-top:4px solid {c_acc}; border-left:none;">
            <div class="lbl">OBJETIVO ESTRATÉGICO PRINCIPAL</div>
            <div class="val" style="font-size:48px;">{str(d.get('meta','')).upper()}</div>
            <div class="lbl" style="margin-top:10px;">DIETA ASIGNADA: {str(d.get('dt','')).upper()}</div>
        </div>
        <div class="list-container" style="padding:15px;">
            <div class="lbl">PROYECCIÓN DE EVOLUCIÓN</div>
            <img src="data:image/png;base64,{grafico_b64}" style="width:100%; border-radius:10px; margin-top:10px; border:1px solid #333;">
        </div>
    </div>
    """
    # 5. ESTRATEGIA NUTRICIONAL
    html += f"""
    <div class="page">
        <table style="width:100%; border-bottom:2px solid #222; padding-bottom:15px; margin-bottom:25px;">
            <tr>
                <td style="text-align:left;"><h1 class="title-elite" style="font-size:38px;">ESTRATEGIA NUTRICIONAL</h1></td>
                <td style="text-align:right;">{img_logo_sm}</td>
            </tr>
        </table>
        <table class="layout-table" style="margin-bottom:25px;">
            <tr>
                <td class="card-td" style="width:33%;"><div class="lbl">KCAL DIARIAS</div><div class="val">{d.get('k',0):.0f}</div></td>
                <td class="card-td" style="width:33%;"><div class="lbl">PROTEÍNAS</div><div class="val">{d.get('p',0):.0f} g</div></td>
                <td class="card-td" style="width:33%;"><div class="lbl">CARBOS / GRASAS</div><div class="val" style="font-size:26px;">{d.get('c',0):.0f}g / {d.get('g',0):.0f}g</div></td>
            </tr>
        </table>
    """
    
    for comida, opciones in d.get('m', {}).items():
        html += f'<div class="list-container"><div class="list-title">{comida}</div>'
        for op in opciones:
            clean_op = str(op).replace('\\n', ' ').replace('\n', ' ').strip()
            html += f'<div class="list-item"><span style="color:{c_acc}; font-weight:bold; margin-right:10px;">&rsaquo;</span>{clean_op}</div>'
        html += '</div>'

    html += f"""
        <div class="list-container" style="border-left-color:#00BFFF;">
            <div class="list-title" style="color:#00BFFF;">SUPLEMENTACIÓN Y MICRONUTRIENTES</div>
    """
    for sup in d.get('s', []):
        clean_sup = str(sup).replace('\\n', ' ').replace('\n', ' ').strip()
        html += f'<div class="list-item"><span style="color:#00BFFF; font-weight:bold; margin-right:10px;">&rsaquo;</span>{clean_sup}</div>'
    html += '</div></div>'
    # 6. PLAN DE ENTRENAMIENTO
    html += f"""
    <div class="page">
        <table style="width:100%; border-bottom:2px solid #222; padding-bottom:15px; margin-bottom:25px;">
            <tr>
                <td style="text-align:left;"><h1 class="title-elite" style="font-size:38px;">PLAN DE ENTRENAMIENTO</h1></td>
                <td style="text-align:right;">{img_logo_sm}</td>
            </tr>
        </table>
        <div class="list-container" style="text-align:center;">
            <span class="lbl" style="margin-right:25px;">MODALIDAD: <span style="color:#FFF;">{str(d.get('entreno','')).upper()}</span></span>
            <span class="lbl">FRECUENCIA: <span style="color:#FFF;">{str(d.get('dias',''))} DÍAS/SEM</span></span>
        </div>
    """
    for dia, ejercicios in d.get('rutina', {}).items():
        html += f'<div class="list-container"><div class="list-title">{dia}</div>'
        for ej in ejercicios:
            clean_ej = str(ej).replace('\\n', ' ').replace('\n', ' ').strip()
            html += f'<div class="list-item"><span style="color:{c_acc}; font-weight:bold; margin-right:10px;">&rsaquo;</span>{clean_ej}</div>'
        html += '</div>'
    
    # 7. TICKET DE COMPRA
    html += f"""
    <div class="page">
        <table style="width:100%; border-bottom:2px solid #222; padding-bottom:15px; margin-bottom:25px;">
            <tr>
                <td style="text-align:left;"><h1 class="title-elite" style="font-size:38px;">TICKET DE COMPRA MENSUAL</h1></td>
                <td style="text-align:right;">{img_logo_sm}</td>
            </tr>
        </table>
        <div class="list-container">
            <table style="width:100%; border-collapse:collapse;">
    """
    for item, cant in d.get('compras', {}).items():
        it = str(item).replace('\n', ' ').strip()
        if "Huevo" in it or "Claras" in it:
            u = int(cant/50)
            res = f"<span style='color:{c_acc}; font-weight:bold;'>{u} Uni.</span> <span style='color:{c_soft};'>(~{round(u/12,1)} Doc.)</span>"
        elif any(x in it for x in ["Café", "Mate", "Té", "Infusión"]):
            res = f"<span style='color:{c_acc}; font-weight:bold;'>{int(cant)} Tazas</span>"
        else:
            res = f"<span style='color:{c_acc}; font-weight:bold;'>{round(cant/1000,2)} KG</span>" if cant>=1000 else f"<span style='color:{c_acc}; font-weight:bold;'>{int(cant)} g</span>"
        
        html += f'<tr><td class="list-item" style="width:70%;">{it}</td><td class="list-item" style="width:30%; text-align:right;">{res}</td></tr>'

    html += f"""
            </table>
        </div>
        <div style="margin-top:60px; text-align:center;">
            {qr_html}<br><br>
            <div class="lbl">CERTIFIED BY EDDY PT ELITE</div>
            <div class="signature" style="margin-top:10px;">Eddy Personal Trainer</div>
        </div>
    </div>
    </body>
    </html>
    """
    return HTML(string=html).write_pdf()