import os
import base64
from weasyprint import HTML

# =========================================================
# EDDY PT ELITE PDF ENGINE
# CINEMATIC BLACK GOLD / RUBY BLACK
# =========================================================

# =========================================================
# THEMES
# =========================================================

THEMES = {
    "gold": {
        "bg": "#030303",
        "bg2": "#080808",
        "card": "#0E0E0E",
        "card2": "#141414",
        "txt": "#F5F5F5",
        "soft": "#8C8C8C",
        "accent": "#D4AF37",
        "bright": "#FFD700",
        "dark": "rgba(212,175,55,0.28)",
        "edition": "BLACK GOLD ALPHA",
        "logo": "logo_dorado.png"
    },
    "ruby": {
        "bg": "#030303",
        "bg2": "#080808",
        "card": "#0E0E0E",
        "card2": "#141414",
        "txt": "#F5F5F5",
        "soft": "#8C8C8C",
        "accent": "#C2185B",
        "bright": "#FF4D8D",
        "dark": "rgba(194,24,91,0.28)",
        "edition": "RUBY BLACK ELITE",
        "logo": "logo_rosa.png"
    }
}

# =========================================================
# HELPERS
# =========================================================

def img_to_b64(path):
    if not path or not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def render_logo(path, class_name):
    b64 = img_to_b64(path)
    if not b64:
        return ""
    return f"""
    <img src="data:image/png;base64,{b64}" class="{class_name}">
    """

def render_metric_card(title, value, percent="80%", extra_class=""):
    return f"""
    <div class="card {extra_class}">
        <div class="label">
        {title}
        </div>
        <div class="value">
        {value}
        </div>
        <div class="bar-bg">
            <div class="bar-fill" style="width:{percent};">
            </div>
        </div>
    </div>
    """

def render_list_card(title, items, accent):
    html = f"""
    <div class="list-card">
        <div class="list-title">
        {title}
        </div>
    """
    for item in items:
        # Limpieza de saltos de línea para que WeasyPrint no rompa los renglones
        item_limpio = str(item).replace('\n', ' ').strip()
        html += f"""
        <div class="item">
            <span class="bullet" style="color:{accent};">
            ›
            </span>
            {item_limpio}
        </div>
        """
    html += "</div>"
    return html

def render_shopping_card(compras, accent, soft):
    # Función nueva que armé respetando tu diseño de cards
    html = """<div class="list-card"><table style="width:100%; border-collapse:collapse;">"""
    for item, cant in compras.items():
        item_limpio = str(item).replace('\n', '').strip()
        if "Huevo" in item_limpio or "Claras" in item_limpio:
            unidades = int(cant / 50)
            res = f"<span style='color:{accent}; font-weight:bold; font-size:13px;'>{unidades} Uni.</span> <span style='color:{soft};'>(~{round(unidades/12, 1)} Doc.)</span>"
        elif any(x in item_limpio for x in ["Café", "Mate", "Té", "Infusión"]):
            res = f"<span style='color:{accent}; font-weight:bold; font-size:13px;'>{int(cant)} Tazas</span>"
        else:
            if cant >= 1000:
                res = f"<span style='color:{accent}; font-weight:bold; font-size:13px;'>{round(cant/1000, 2)} KG</span>"
            else:
                res = f"<span style='color:{accent}; font-weight:bold; font-size:13px;'>{int(cant)} g</span>"
        
        html += f"""
        <tr>
            <td style="padding:12px 0; border-bottom:1px solid rgba(255,255,255,0.03); font-size:11px; color:#E0E0E0; width:70%;">{item_limpio}</td>
            <td style="padding:12px 0; border-bottom:1px solid rgba(255,255,255,0.03); text-align:right; width:30%;">{res}</td>
        </tr>
        """
    html += "</table></div>"
    return html

# =========================================================
# MAIN FUNCTION
# =========================================================

def build_pdf_v70(d, grafico_b64, ruta_logo, gen="m"):

    # =====================================================
    # THEME
    # =====================================================

    theme = THEMES["ruby"] if gen == "f" else THEMES["gold"]

    c_bg = theme["bg"]
    c_bg2 = theme["bg2"]
    c_card = theme["card"]
    c_card2 = theme["card2"]
    c_txt = theme["txt"]
    c_soft = theme["soft"]
    c_accent = theme["accent"]
    c_bright = theme["bright"]
    c_dark = theme["dark"]
    edition = theme["edition"]

    # =====================================================
    # LOGOS
    # =====================================================

    final_logo = theme["logo"] if os.path.exists(theme["logo"]) else ruta_logo

    logo_main = render_logo(final_logo, "logo-main")
    logo_small = render_logo(final_logo, "logo-small")

    # =====================================================
    # QR
    # =====================================================

    qr_html = ""
    if os.path.exists("qr_code.png"):
        qr_b64 = img_to_b64("qr_code.png")
        qr_html = f'<img src="data:image/png;base64,{qr_b64}" class="qr">'
    else:
        qr_html = f'<div class="qr" style="background:#111; color:{c_accent}; font-size:10px; display:flex; align-items:center; justify-content:center;">QR</div>'

    # =====================================================
    # HTML COMPLETO
    # =====================================================

    html = f"""
    <html>
    <head>
    <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Montserrat:wght@300;400;500;700;900&family=Great+Vibes&display=swap" rel="stylesheet">
    <style>
    /* TODO TU CSS INTACTO */
    @page {{ size:A4; margin:0; background:{c_bg}; }}
    *{{ box-sizing:border-box; }}
    body{{ margin:0; padding:0; overflow-x:hidden; background: radial-gradient(rgba(255,255,255,0.015) 1px, transparent 1px), linear-gradient(180deg, {c_bg2}, {c_bg}); background-size:30px 30px; font-family:'Montserrat',sans-serif; color:{c_txt}; }}
    body:before{{ content:''; position:fixed; width:900px; height:900px; top:-350px; left:-250px; background: radial-gradient(circle, {c_dark}, transparent 70%); filter:blur(100px); z-index:-1; }}
    
    .cover{{ height:100vh; display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center; padding:50px; position:relative; overflow:hidden; }}
    .logo-main{{ height:300px; max-width:80%; object-fit:contain; filter: drop-shadow(0 0 12px {c_accent}) drop-shadow(0 0 18px {c_dark}) brightness(1.05) contrast(1.05); }}
    .cover-title{{ font-family:'Bebas Neue'; font-size:72px; letter-spacing:8px; margin-top:-10px; background: linear-gradient(180deg, #FFF3B0 0%, {c_bright} 25%, {c_accent} 55%, #6B4E00 100%); background-size:200% 200%; -webkit-background-clip:text; -webkit-text-fill-color:transparent; text-shadow: 0 2px 0 #000, 0 8px 18px rgba(0,0,0,0.8), 0 0 12px {c_dark}; }}
    .cover-sub{{ color:{c_soft}; letter-spacing:4px; font-size:11px; margin-top:-8px; }}
    .badge{{ margin-top:28px; padding:12px 32px; border-radius:50px; background: linear-gradient(145deg, rgba(255,255,255,0.03), rgba(255,255,255,0.008)); border: 1px solid rgba(255,255,255,0.05); backdrop-filter:blur(16px); box-shadow: inset 0 1px 1px rgba(255,255,255,0.04), 0 0 14px {c_dark}; font-weight:700; letter-spacing:4px; }}
    .athlete{{ margin-top:40px; width:70%; border-top: 1px solid rgba(255,255,255,0.05); border-bottom: 1px solid rgba(255,255,255,0.05); padding:25px 0; }}
    .athlete-name{{ font-family:'Bebas Neue'; font-size:50px; letter-spacing:3px; margin:0; background: linear-gradient(180deg, #FFF3B0, {c_bright}, {c_accent}); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }}
    
    .page{{ padding:45px; page-break-before:always; }}
    .header{{ display:flex; justify-content:space-between; align-items:end; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom:18px; margin-bottom:30px; }}
    .header-title{{ font-family:'Bebas Neue'; font-size:34px; letter-spacing:3px; background: linear-gradient(180deg, #FFF3B0, {c_bright}, {c_accent}); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }}
    .logo-small{{ height:55px; filter: drop-shadow(0 0 8px {c_dark}); }}
    
    .grid{{ display:flex; flex-wrap:wrap; gap:18px; margin-bottom:22px; }}
    .card{{ width:23%; background: linear-gradient(145deg, rgba(255,255,255,0.035), rgba(255,255,255,0.008)); backdrop-filter:blur(16px); border: 1px solid rgba(255,255,255,0.05); border-top: 3px solid {c_accent}; border-radius:20px; padding:28px; box-shadow: inset 0 1px 1px rgba(255,255,255,0.05), inset 0 -2px 4px rgba(0,0,0,0.4), 0 10px 25px rgba(0,0,0,0.85), 0 0 14px {c_dark}; position:relative; overflow:hidden; }}
    
    .card-medium{{ width:31%; }} /* Clase para 3 columnas en Nutrición */
    .card-large{{ width:100%; }}
    .card-center{{ text-align:center; }}
    .card-water{{ border-top-color:#00BFFF; }}
    
    .card:before{{ content:''; position:absolute; width:220px; height:220px; opacity:0.4; transform:rotate(25deg); background: radial-gradient(circle, rgba(255,255,255,0.04), transparent 70%); top:-130px; right:-100px; }}
    .label{{ font-size:10px; letter-spacing:2px; color:{c_soft}; margin-bottom:8px; text-transform:uppercase; }}
    .value{{ font-family:'Bebas Neue'; font-size:34px; letter-spacing:2px; line-height:1; background: linear-gradient(180deg, #FFF3B0, {c_bright}, {c_accent}, #7A5A00); background-size:200% 200%; -webkit-background-clip:text; -webkit-text-fill-color:transparent; text-shadow: 0 4px 10px rgba(0,0,0,0.7); }}
    
    /* Trick CSS para que la hidratación quede azul perfecta sobre tu gradiente */
    .card-water .value {{ background: none; -webkit-text-fill-color: #00BFFF; text-shadow: 0 4px 10px rgba(0, 191, 255, 0.4); }}
    .card-water .bar-fill {{ background: linear-gradient(90deg, #80DFFF, #00BFFF); box-shadow: 0 0 12px rgba(0,191,255,0.5); }}

    .bar-bg{{ width:100%; height:6px; background:#1A1A1A; border-radius:20px; margin-top:15px; overflow:hidden; position:relative; }}
    .bar-fill{{ height:100%; border-radius:20px; position:relative; background: linear-gradient(90deg, #FFF6CC, {c_bright}, {c_accent}, #7A5A00); box-shadow: 0 0 12px {c_dark}; }}
    .bar-fill:after{{ content:''; position:absolute; top:0; left:0; width:100%; height:50%; background: linear-gradient(180deg, rgba(255,255,255,0.30), transparent); }}
    
    .list-card{{ background: linear-gradient(145deg, rgba(255,255,255,0.03), rgba(255,255,255,0.008)); border-left: 4px solid {c_accent}; border-radius:18px; padding:28px; margin-bottom:20px; box-shadow: inset 0 1px 1px rgba(255,255,255,0.03), 0 8px 20px rgba(0,0,0,0.85); }}
    .list-title{{ font-family:'Bebas Neue'; font-size:24px; letter-spacing:2px; margin-bottom:15px; color:{c_bright}; }}
    .item{{ padding:12px 0; border-bottom: 1px solid rgba(255,255,255,0.03); font-size:11px; color:#E0E0E0; line-height: 1.5; }}
    .bullet{{ margin-right:8px; }}
    
    .graph{{ width:100%; background:#050505; border-radius:18px; border: 1px solid rgba(255,255,255,0.06); box-shadow: 0 0 18px rgba(0,0,0,0.85); }}
    .footer{{ margin-top:45px; display:flex; justify-content:space-between; align-items:end; border-top: 1px solid rgba(255,255,255,0.05); padding-top:24px; }}
    .signature{{ font-family:'Great Vibes'; font-size:42px; color:{c_soft}; }}
    .qr{{ width:62px; height:62px; background:white; padding:5px; border-radius:10px; border: 1px solid {c_accent}; box-shadow: 0 0 18px rgba(0,0,0,0.8); }}
    </style>
    </head>
    <body>
    
    <div class="cover">
        {logo_main}
        <div class="cover-title">PLAN INTEGRAL ELITE</div>
        <div class="cover-sub">HIGH PERFORMANCE PHYSIQUE</div>
        <div class="badge">{edition}</div>
        <div class="athlete">
            <div class="label">ATLETA DE ÉLITE</div>
            <div class="athlete-name">{d['n'].upper()}</div>
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
            {logo_small}
        </div>
        
        <div class="grid">
            {render_metric_card("EDAD", d["edad"], "100%")}
            {render_metric_card("ESTATURA", f"{d['estatura']}CM", "80%")}
            {render_metric_card("PESO", f"{d['peso']}KG", "75%")}
            {render_metric_card("GRASA", f"{d['rfm']}%", "65%")}
        </div>
        
        <div class="grid">
            {render_metric_card("CINTURA", f"{d['cintura']}CM", "60%")}
            {render_metric_card("CADERA", f"{d['cadera']}CM", "60%")}
            {render_metric_card("ÍNDICE RCC", str(d['rcc']), "50%")}
            {render_metric_card("HIDRATACIÓN", f"{d['w']}L", "100%", "card-water")}
        </div>

        <div class="card card-large card-center" style="margin-bottom: 22px;">
            <div class="label">OBJETIVO ESTRATÉGICO</div>
            <div class="value" style="font-size:42px;">{d['meta'].upper()}</div>
            <div class="label" style="margin-top:10px;">DIETA ASIGNADA: {d['dt'].upper()}</div>
        </div>

        <div class="card card-large card-center">
            <div class="label">PROYECCIÓN CORPORAL</div>
            <br>
            <img src="data:image/png;base64,{grafico_b64}" class="graph">
        </div>

        <div class="footer">
            {qr_html}
            <div class="signature">Eddy Personal Trainer</div>
        </div>
    </div>

    <div class="page">
        <div class="header">
            <div class="header-title">ESTRATEGIA NUTRICIONAL</div>
            {logo_small}
        </div>
        
        <div class="grid">
            {render_metric_card("KCAL DIARIAS", f"{d['k']:.0f}", "100%", "card-medium card-center")}
            {render_metric_card("PROTEÍNAS", f"P:{d['p']:.0f}g", "100%", "card-medium card-center")}
            {render_metric_card("CARBOS / GRASAS", f"C:{d['c']:.0f} / G:{d['g']:.0f}", "100%", "card-medium card-center")}
        </div>
    """

    for comida, opciones in d['m'].items():
        html += render_list_card(comida, opciones, c_accent)

    html += render_list_card("SUPLEMENTACIÓN Y MICRONUTRIENTES", d['s'], "#00BFFF")

    html += f"""
        <div class="footer">
            {qr_html}
            <div class="signature">Eddy Personal Trainer</div>
        </div>
    </div>

    <div class="page">
        <div class="header">
            <div class="header-title">PLAN DE ENTRENAMIENTO</div>
            {logo_small}
        </div>
        
        <div class="card card-large card-center" style="margin-bottom: 22px;">
            <span class="label" style="display:inline-block; margin-right:20px;">TIPO DE RUTINA: <span style="color:{c_txt}; font-size:12px;">{d['entreno'].upper()}</span></span>
            <span class="label" style="display:inline-block;">FRECUENCIA: <span style="color:{c_txt}; font-size:12px;">{d['dias']} DÍAS/SEM</span></span>
        </div>
    """

    for dia, ejercicios in d['rutina'].items():
        html += render_list_card(dia, ejercicios, c_accent)

    html += f"""
        <div class="footer">
            {qr_html}
            <div class="signature">Eddy Personal Trainer</div>
        </div>
    </div>

    <div class="page">
        <div class="header">
            <div class="header-title">TICKET DE COMPRA MENSUAL</div>
            {logo_small}
        </div>
        
        {render_shopping_card(d['compras'], c_accent, c_soft)}
        
        <div class="footer">
            {qr_html}
            <div class="signature">Eddy Personal Trainer</div>
        </div>
    </div>
    
    </body>
    </html>
    """

    pdf = HTML(string=html).write_pdf()
    return pdf