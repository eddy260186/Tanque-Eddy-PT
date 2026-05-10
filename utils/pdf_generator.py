import os
import base64
from weasyprint import HTML

# ==========================================================
# EDDY PERSONAL TRAINER ELITE - PDF GENERATOR ULTRA PREMIUM
# ==========================================================

def build_pdf_v60_7(d, grafico_b64, ruta_img, gen):

    # ======================================================
    # 1. DETECCIÓN DE GÉNERO / EDICIÓN
    # ======================================================

    is_f = (gen == "f")

    # ======================================================
    # 2. PALETA ULTRA PREMIUM
    # ======================================================

    c_bg = "#030303"
    c_bg2 = "#090909"

    c_card = "#111111"
    c_card2 = "#191919"

    c_txt = "#F5F5F5"

    c_soft = "#8C8C8C"

    if is_f:
        c_accent = "#C2185B"
        c_bright = "#FF4D8D"
        c_dark = "rgba(194,24,91,0.35)"
        edition = "RUBY BLACK ELITE"
        ruta_logo = "logo_rosa.png"
    else:
        c_accent = "#D4AF37"
        c_bright = "#FFD700"
        c_dark = "rgba(212,175,55,0.35)"
        edition = "BLACK GOLD ALPHA"
        ruta_logo = "logo_dorado.png"

    # ======================================================
    # 3. LOGO PRINCIPAL
    # ======================================================

    logo_html = ""
    logo_chico_html = ""

    ruta_final = ruta_logo if os.path.exists(ruta_logo) else ruta_img

    if ruta_final and os.path.exists(ruta_final):
        with open(ruta_final, "rb") as f:
            logo_b64 = base64.b64encode(f.read()).decode("utf-8")

        logo_html = f"""
        <img src="data:image/png;base64,{logo_b64}" class="logo-main">
        """
        
        logo_chico_html = f"""
        <img src="data:image/png;base64,{logo_b64}" class="logo-small">
        """

    # ======================================================
    # 4. QR REAL
    # ======================================================

    qr_html = ""

    if os.path.exists("qr_code.png"):
        with open("qr_code.png", "rb") as f:
            qr_b64 = base64.b64encode(f.read()).decode("utf-8")
        qr_html = f"""
        <img src="data:image/png;base64,{qr_b64}" class="qr">
        """
    else:
        qr_html = f"""
        <div class="qr" style="background:#111; color:{c_accent}; font-size:8px; display:flex; align-items:center; justify-content:center;">QR</div>
        """

    # ======================================================
    # 5. HTML Y CSS PRINCIPAL (TU DISEÑO EXACTO)
    # ======================================================

    html = f"""
    <html>
    <head>
    <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Montserrat:wght@300;400;500;700;900&family=Great+Vibes&display=swap" rel="stylesheet">
    <style>

    @page {{
        size:A4;
        margin:0;
        background:{c_bg};
    }}

    *{{
        box-sizing:border-box;
    }}

    body{{
        margin:0;
        padding:0;
        background: radial-gradient(rgba(255,255,255,0.02) 1px, transparent 1px), linear-gradient(180deg, {c_bg2}, {c_bg});
        background-size:30px 30px;
        font-family:'Montserrat',sans-serif;
        color:{c_txt};
    }}

    body:before{{
        content:'';
        position:fixed;
        width:800px;
        height:800px;
        top:-300px;
        left:-200px;
        background: radial-gradient(circle, {c_dark}, transparent 70%);
        filter:blur(90px);
        z-index:-1;
    }}

    /* ================================================== */
    /* PORTADA */
    /* ================================================== */

    .cover{{
        height:100vh;
        display:flex;
        flex-direction:column;
        justify-content:center;
        align-items:center;
        text-align:center;
        padding:40px;
        position:relative;
        overflow:hidden;
        background: radial-gradient(circle at top, {c_dark}, transparent 40%);
    }}

    .logo-main{{
        height:360px;
        filter: drop-shadow(0 0 15px {c_accent}) drop-shadow(0 0 35px {c_dark}) brightness(1.08) contrast(1.08);
    }}

    .cover-title{{
        font-family:'Bebas Neue';
        font-size:74px;
        letter-spacing:8px;
        margin-top:-15px;
        background: linear-gradient(180deg, #FFF3B0 0%, {c_bright} 25%, {c_accent} 55%, #6B4E00 100%);
        -webkit-background-clip:text;
        -webkit-text-fill-color:transparent;
        text-shadow: 0 2px 0 #000, 0 10px 25px rgba(0,0,0,0.8), 0 0 18px {c_dark};
    }}

    .cover-sub{{
        color:{c_soft};
        letter-spacing:4px;
        font-size:11px;
        margin-top:-10px;
    }}

    .badge{{
        margin-top:30px;
        padding:12px 35px;
        border-radius:50px;
        background: linear-gradient(145deg, rgba(255,255,255,0.05), rgba(255,255,255,0.01));
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 0 20px {c_dark};
        font-weight:700;
        letter-spacing:4px;
    }}

    .athlete{{
        margin-top:40px;
        width:70%;
        border-top: 1px solid rgba(255,255,255,0.08);
        border-bottom: 1px solid rgba(255,255,255,0.08);
        padding:25px 0;
    }}

    .athlete-name{{
        font-family:'Bebas Neue';
        font-size:52px;
        letter-spacing:3px;
        margin:0;
        background: linear-gradient(180deg, #FFF3B0, {c_bright}, {c_accent});
        -webkit-background-clip:text;
        -webkit-text-fill-color:transparent;
    }}

    /* ================================================== */
    /* INTERIORES */
    /* ================================================== */

    .page{{
        padding:40px;
        page-break-before:always;
    }}

    .header{{
        display:flex;
        justify-content:space-between;
        align-items:end;
        border-bottom: 1px solid rgba(255,255,255,0.08);
        padding-bottom:15px;
        margin-bottom:25px;
    }}

    .header-title{{
        font-family:'Bebas Neue';
        font-size:34px;
        letter-spacing:3px;
        background: linear-gradient(180deg, #FFF3B0, {c_bright}, {c_accent});
        -webkit-background-clip:text;
        -webkit-text-fill-color:transparent;
    }}

    .logo-small{{
        height:60px;
        filter: drop-shadow(0 0 10px {c_dark});
    }}

    /* ================================================== */
    /* SISTEMA DE GRILLAS PARA WEASYPRINT (LA SOLUCIÓN) */
    /* ================================================== */

    /* Grilla de 4 columnas */
    .grid-4 {{
        width: 100%;
        margin-bottom: 20px;
    }}
    .grid-4::after {{ content: ""; display: table; clear: both; }}
    .grid-4 .card {{ float: left; width: 22.5%; margin-right: 3.33%; }}
    .grid-4 .card.last {{ margin-right: 0; }}

    /* Grilla de 3 columnas */
    .grid-3 {{
        width: 100%;
        margin-bottom: 20px;
    }}
    .grid-3::after {{ content: ""; display: table; clear: both; }}
    .grid-3 .card {{ float: left; width: 31%; margin-right: 3.5%; }}
    .grid-3 .card.last {{ margin-right: 0; }}

    /* ================================================== */
    /* CARDS */
    /* ================================================== */

    .card{{
        background: linear-gradient(145deg, rgba(255,255,255,0.04), rgba(255,255,255,0.01));
        border: 1px solid rgba(255,255,255,0.06);
        border-top: 3px solid {c_accent};
        border-radius:18px;
        padding:22px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.8), 0 0 18px {c_dark};
        position:relative;
        overflow:hidden;
    }}

    .card:before{{
        content:'';
        position:absolute;
        width:200px;
        height:200px;
        background: radial-gradient(circle, rgba(255,255,255,0.05), transparent 70%);
        top:-120px;
        right:-100px;
    }}

    .label{{
        font-size:10px;
        letter-spacing:2px;
        color:{c_soft};
        margin-bottom:8px;
        text-transform:uppercase;
    }}

    .value{{
        font-family:'Bebas Neue';
        font-size:34px;
        letter-spacing:2px;
        background: linear-gradient(180deg, #FFF3B0, {c_bright}, {c_accent}, #7A5A00);
        -webkit-background-clip:text;
        -webkit-text-fill-color:transparent;
        text-shadow: 0 4px 12px rgba(0,0,0,0.7);
    }}

    .bar-bg{{
        width:100%;
        height:6px;
        background:#1A1A1A;
        border-radius:20px;
        margin-top:15px;
        overflow:hidden;
    }}

    .bar-fill{{
        height:100%;
        border-radius:20px;
        background: linear-gradient(90deg, #FFF6CC, {c_bright}, {c_accent}, #7A5A00);
        box-shadow: 0 0 15px {c_dark};
    }}

    /* ================================================== */
    /* LISTAS Y TABLAS */
    /* ================================================== */

    .list-card{{
        background: linear-gradient(145deg, rgba(255,255,255,0.03), rgba(255,255,255,0.01));
        border-left: 4px solid {c_accent};
        border-radius:16px;
        padding:22px;
        margin-bottom:18px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.8);
    }}

    .list-title{{
        font-family:'Bebas Neue';
        font-size:24px;
        letter-spacing:2px;
        margin-bottom:12px;
        color:{c_bright};
    }}

    .item{{
        padding:10px 0;
        border-bottom: 1px solid rgba(255,255,255,0.04);
        font-size:11px;
        color: #E0E0E0;
    }}
    
    .data-table {{
        width: 100%;
        border-collapse: collapse;
    }}
    
    .data-table td {{
        padding: 10px 0;
        border-bottom: 1px solid rgba(255,255,255,0.04);
        font-size: 11px;
        color: #E0E0E0;
    }}

    /* ================================================== */
    /* GRAFICO */
    /* ================================================== */

    .graph{{
        width:100%;
        border-radius:16px;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 0 25px rgba(0,0,0,0.8);
    }}

    /* ================================================== */
    /* FOOTER */
    /* ================================================== */

    .footer{{
        margin-top:40px;
        display:flex;
        justify-content:space-between;
        align-items:end;
        border-top: 1px solid rgba(255,255,255,0.08);
        padding-top:18px;
    }}

    .signature{{
        font-family:'Great Vibes';
        font-size:34px;
        color:{c_soft};
    }}

    .qr{{
        width:60px;
        height:60px;
        background:white;
        padding:3px;
        border-radius:6px;
        border: 1px solid {c_accent};
        box-shadow: 0 0 18px rgba(0,0,0,0.7);
    }}

    </style>
    </head>
    <body>

    <div class="cover">
        {logo_html}
        <div class="cover-title">PLAN INTEGRAL ELITE</div>
        <div class="cover-sub">INGENIERÍA CORPORAL DE ALTO VALOR</div>
        <div class="badge">{edition}</div>

        <div class="athlete">
            <div class="label">ATLETA DE ÉLITE</div>
            <div class="athlete-name">{d['n'].upper()}</div>
            <div class="label" style="margin-top:15px; margin-bottom:0;">NIVEL: {d['nivel'].upper()}</div>
        </div>
        
        <div style="position: absolute; bottom: 40px; width: 100%; display: flex; justify-content: space-between; padding: 0 40px; align-items: end;">
            {qr_html}
            <div style="font-size: 9px; color: {c_soft}; letter-spacing: 2px;">POWERED BY EDDY PT ELITE</div>
            <div class="signature">Eddy Personal Trainer</div>
        </div>
    </div>

    <div class="page">
        <div class="header">
            <div class="header-title">ANALÍTICA FÍSICA</div>
            {logo_chico_html}
        </div>

        <div class="grid-4">
            <div class="card">
                <div class="label">EDAD</div>
                <div class="value">{d['edad']}</div>
                <div class="bar-bg"><div class="bar-fill" style="width:100%;"></div></div>
            </div>
            <div class="card">
                <div class="label">ESTATURA</div>
                <div class="value">{d['estatura']}CM</div>
                <div class="bar-bg"><div class="bar-fill" style="width:80%;"></div></div>
            </div>
            <div class="card">
                <div class="label">PESO</div>
                <div class="value">{d['peso']}KG</div>
                <div class="bar-bg"><div class="bar-fill" style="width:70%;"></div></div>
            </div>
            <div class="card last">
                <div class="label">GRASA</div>
                <div class="value">{d['rfm']}%</div>
                <div class="bar-bg"><div class="bar-fill" style="width:65%;"></div></div>
            </div>
        </div>
        
        <div class="grid-4">
            <div class="card">
                <div class="label">CINTURA</div>
                <div class="value">{d['cintura']}CM</div>
                <div class="bar-bg"><div class="bar-fill" style="width:60%;"></div></div>
            </div>
            <div class="card">
                <div class="label">CADERA</div>
                <div class="value">{d['cadera']}CM</div>
                <div class="bar-bg"><div class="bar-fill" style="width:60%;"></div></div>
            </div>
            <div class="card">
                <div class="label">ÍNDICE RCC</div>
                <div class="value">{d['rcc']}</div>
                <div class="bar-bg"><div class="bar-fill" style="width:50%;"></div></div>
            </div>
            <div class="card last" style="border-top-color: #00BFFF;">
                <div class="label" style="color: #00BFFF;">HIDRATACIÓN</div>
                <div class="value" style="background: none; -webkit-text-fill-color: #00BFFF; text-shadow: none;">{d['w']}L</div>
                <div class="bar-bg"><div class="bar-fill" style="width:100%; background: #00BFFF; box-shadow: 0 0 15px #00BFFF;"></div></div>
            </div>
        </div>

        <div class="card" style="margin-bottom: 20px; width: 100%; display: block;">
            <div class="label">OBJETIVO ESTRATÉGICO</div>
            <div class="value" style="font-size: 40px;">{d['meta'].upper()}</div>
            <div class="label" style="margin-top: 5px;">DIETA ASIGNADA: {d['dt'].upper()}</div>
        </div>

        <div class="card" style="width: 100%; display: block;">
            <div class="label">PROYECCIÓN CORPORAL</div>
            <img src="data:image/png;base64,{grafico_b64}" class="graph">
        </div>
    </div>

    <div class="page">
        <div class="header">
            <div class="header-title">ESTRATEGIA NUTRICIONAL</div>
            {logo_chico_html}
        </div>
        
        <div class="grid-3">
            <div class="card">
                <div class="label">KCAL DIARIAS</div>
                <div class="value">{d['k']:.0f}</div>
            </div>
            <div class="card">
                <div class="label">PROTEÍNAS</div>
                <div class="value">{d['p']:.0f}g</div>
            </div>
            <div class="card last">
                <div class="label">CARBOS / GRASAS</div>
                <div class="value" style="font-size: 26px;">{d['c']:.0f}g / {d['g']:.0f}g</div>
            </div>
        </div>
    """

    # BUCLE DE COMIDAS (Con limpieza de saltos de línea para que no se rompan las tablas)
    for comida, opciones in d['m'].items():
        html += f"""
        <div class="list-card">
            <div class="list-title">{comida}</div>
        """
        for op in opciones:
            # LIMPIEZA CLAVE AQUÍ:
            op_limpia = str(op).replace('\n', ' ').strip()
            html += f'<div class="item"><span style="color:{c_accent}; margin-right:8px;">&rsaquo;</span>{op_limpia}</div>'
        html += "</div>"

    # BUCLE DE SUPLEMENTACIÓN
    html += f"""
        <div class="list-card" style="border-left-color: #00BFFF;">
            <div class="list-title" style="color: #00BFFF;">SUPLEMENTACIÓN</div>
    """
    for suplemento in d['s']:
        # LIMPIEZA CLAVE AQUÍ:
        sup_limpio = str(suplemento).replace('\n', ' ').strip()
        html += f'<div class="item"><span style="color:#00BFFF; margin-right:8px;">&rsaquo;</span>{sup_limpio}</div>'
    
    html += f"""
        </div>
        
        <div class="footer">
            {qr_html}
            <div class="signature">Eddy Personal Trainer</div>
        </div>
    </div>
    """

    # =================================================
    # ENTRENAMIENTO
    # =================================================
    html += f"""
    <div class="page">
        <div class="header">
            <div class="header-title">PLAN DE ENTRENAMIENTO</div>
            {logo_chico_html}
        </div>
        
        <div class="card" style="margin-bottom: 20px; text-align: center; width: 100%; display: block;">
            <span class="label" style="display:inline-block; margin-right:20px;">TIPO DE RUTINA: <span style="color:{c_txt}; font-size:12px;">{d['entreno'].upper()}</span></span>
            <span class="label" style="display:inline-block;">FRECUENCIA: <span style="color:{c_txt}; font-size:12px;">{d['dias']} DÍAS/SEM</span></span>
        </div>
    """

    # BUCLE DE RUTINAS
    for dia, ejercicios in d['rutina'].items():
        html += f"""
        <div class="list-card">
            <div class="list-title">{dia}</div>
        """
        for ej in ejercicios:
            # LIMPIEZA CLAVE AQUÍ:
            ej_limpio = str(ej).replace('\n', ' ').strip()
            html += f'<div class="item"><span style="color:{c_accent}; margin-right:8px;">&rsaquo;</span>{ej_limpio}</div>'
        html += "</div>"

    html += f"""
        <div class="footer">
            {qr_html}
            <div class="signature">Eddy Personal Trainer</div>
        </div>
    </div>
    """

    # =================================================
    # COMPRAS
    # =================================================
    html += f"""
    <div class="page">
        <div class="header">
            <div class="header-title">TICKET DE COMPRA MENSUAL</div>
            {logo_chico_html}
        </div>
        
        <div class="list-card">
            <table class="data-table">
    """
    
    # BUCLE DE COMPRAS (Con fórmula de huevos e infusiones intocable)
    for item, cant in d['compras'].items():
        # LIMPIEZA CLAVE AQUÍ PARA QUE LA TABLA NO SE ROMPA:
        item_limpio = str(item).replace('\n', '').strip()
        
        if "Huevo" in item_limpio or "Claras" in item_limpio:
            unidades = int(cant / 50)
            res = f"<span style='color:{c_accent}; font-weight:bold;'>{unidades} Uni.</span> <span style='color:{c_soft};'>(~{round(unidades/12, 1)} Doc.)</span>"
        elif any(x in item_limpio for x in ["Café", "Mate", "Té", "Infusión"]):
            res = f"<span style='color:{c_accent}; font-weight:bold;'>{int(cant)} Tazas</span>"
        else:
            if cant >= 1000:
                res = f"<span style='color:{c_accent}; font-weight:bold;'>{round(cant/1000, 2)} KG</span>"
            else:
                res = f"<span style='color:{c_accent}; font-weight:bold;'>{int(cant)} g</span>"
                
        html += f"<tr><td style='width:70%; font-weight:600;'>{item_limpio}</td><td style='width:30%; text-align:right;'>{res}</td></tr>"

    html += f"""
            </table>
        </div>
        
        <div class="footer">
            {qr_html}
            <div class="signature">Eddy Personal Trainer</div>
        </div>
    </div>
    
    </body>
    </html>
    """

    return HTML(
        string=html
    ).write_pdf()