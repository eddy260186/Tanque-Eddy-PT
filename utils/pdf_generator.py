import os
import base64
from datetime import datetime
from weasyprint import HTML

# =========================================================
# EDDY ELITE PDF ENGINE - CINEMATIC V80 (100% ESPAÑOL & CORREGIDO)
# BLACK GOLD / RUBY EDITION
# =========================================================

def safe_int(value):
    """Filtro de precisión: Elimina decimales rotos."""
    try: return int(round(float(value)))
    except: return 0

def img_to_b64(path):
    if path and os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return ""

THEMES = {
    "gold": {
        "accent": "#D4AF37", "bright": "#FFD700", "soft": "rgba(212,175,55,0.12)",
        "card": "#111111", "border": "rgba(212,175,55,0.25)", "text": "#FFFFFF",
        "logo": "logo_dorado.png", "overlay": "logo_dorado.png"
    },
    "ruby": {
        "accent": "#FF2D75", "bright": "#FF73A8", "soft": "rgba(255,45,117,0.12)",
        "card": "#111111", "border": "rgba(255,45,117,0.25)", "text": "#FFFFFF",
        "logo": "logo_rosa.png", "overlay": "logo_rosa.png"
    }
}

# =========================================================
# COMPONENTES VISUALES
# =========================================================

def generate_gauge(percent, color, title, value):
    circumference = 339.292
    p = min(max(float(percent), 0), 100)
    offset = circumference - (p / 100) * circumference

    return f"""
    <div style="text-align:center; width:220px;">
        <div style="font-size:11px; letter-spacing:2px; color:#888; margin-bottom:10px; text-transform:uppercase; font-weight:700; font-family:'Montserrat', sans-serif;">
            {title}
        </div>
        <svg width="180" height="180" viewBox="0 0 220 220" style="overflow: visible;">
            <circle cx="110" cy="110" r="54" stroke="#000" stroke-width="16" fill="none" style="filter: drop-shadow(0 4px 6px rgba(0,0,0,0.8));"/>
            <circle cx="110" cy="110" r="54" stroke="#1F1F1F" stroke-width="12" fill="none"/>
            <circle cx="110" cy="110" r="54" stroke="{color}" stroke-width="12" fill="none"
                stroke-linecap="round" stroke-dasharray="{circumference}" stroke-dashoffset="{offset}"
                transform="rotate(-90 110 110)" />
            <text x="50%" y="53%" dominant-baseline="middle" text-anchor="middle" fill="white" font-size="34" font-weight="900" font-family="'Montserrat', sans-serif">
                {value}
            </text>
        </svg>
    </div>
    """

def macro_bar(title, grams, percent, accent):
    p = min(max(float(percent), 0), 100)
    g_val = safe_int(grams)
    return f"""
    <div style="margin-bottom:25px;">
        <div style="display:flex; justify-content:space-between; margin-bottom:8px; font-family:'Montserrat', sans-serif;">
            <div style="color:white; font-size:13px; font-weight:700; letter-spacing:1px; text-transform:uppercase;">{title}</div>
            <div style="color:{accent}; font-size:15px; font-weight:900;">{g_val}g</div>
        </div>
        <div style="height:12px; border-radius:20px; background:#1A1A1A; box-shadow: inset 0 2px 5px rgba(0,0,0,0.8);">
            <div style="width:{p}%; height:100%; border-radius:20px; background:{accent}; box-shadow:0 0 10px {accent};"></div>
        </div>
    </div>
    """

# =========================================================
# MOTOR PDF
# =========================================================

def build_pdf_v60_7(data, grafico_b64="", ruta_img="", genero="m"):
    theme = THEMES["ruby"] if genero == "f" else THEMES["gold"]

    accent = theme["accent"]
    soft = theme["soft"]
    border = theme["border"]

    logo_main = img_to_b64(theme["logo"] if os.path.exists(theme["logo"]) else ruta_img)
    logo_overlay = img_to_b64(theme["overlay"] if os.path.exists(theme["overlay"]) else ruta_img)
    qr = img_to_b64("qr_code.png")

    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700;900&display=swap');

    @page {{ size: A4; margin: 0; background: #020202; }}
    
    body {{ margin: 0; padding: 0; background: #020202; color: #FFF; font-family: 'Montserrat', Arial, sans-serif; }}

    .page {{ width: 210mm; height: 297mm; position: relative; overflow: hidden; page-break-after: always; background: #020202; }}

    .bg-glow {{
        position: absolute; width: 900px; height: 900px; border-radius: 100%;
        background: radial-gradient(circle, {soft}, transparent 70%);
        top: -350px; left: -200px; z-index: 0;
    }}

    .overlay-logo {{ position: absolute; width: 700px; opacity: 0.02; top: 160px; right: -120px; z-index: 0; }}

    .content {{ position: relative; z-index: 2; padding: 45px; }}

    .hero-logo {{ width: 220px; filter: drop-shadow(0 5px 15px rgba(0,0,0,0.8)); margin-bottom: 10px; }}

    .hero-title {{
        font-size: 55px; font-weight: 900; letter-spacing: 6px; line-height: 1.1;
        color: {accent}; text-shadow: 0 4px 10px rgba(0,0,0,0.8); text-transform: uppercase;
    }}

    .hero-sub {{ color: #888; letter-spacing: 4px; font-size: 11px; margin-top: 10px; font-weight: 700; text-transform: uppercase; }}

    .premium-card {{
        background: linear-gradient(145deg, rgba(25,25,25,0.8), rgba(10,10,10,0.9));
        border: 1px solid {border}; border-top: 2px solid {accent}; border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.9), inset 0 2px 5px rgba(255,255,255,0.03);
        position: relative; overflow: hidden; margin-bottom: 25px; padding: 30px;
    }}
    .premium-card::before {{
        content: ''; position: absolute; width: 240px; height: 40px;
        background: rgba(255,255,255,0.02); transform: rotate(-35deg); top: -10px; left: -100px;
    }}

    .athlete-name {{ font-size: 38px; font-weight: 900; letter-spacing: 2px; color: #FFF; line-height: 1.2; text-shadow: 0 2px 5px rgba(0,0,0,0.8); }}
    .label {{ color: {accent}; font-size: 11px; letter-spacing: 2px; text-transform: uppercase; font-weight: 700; }}
    
    .section-title {{
        font-size: 22px; font-weight: 900; letter-spacing: 2px; margin-bottom: 25px;
        color: #FFF; text-transform: uppercase; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 10px;
    }}

    .table-dark {{ width: 100%; border-collapse: separate; border-spacing: 15px; margin-top: 10px; }}
    .mini-card {{ background: rgba(0,0,0,0.6); border-radius: 12px; padding: 15px; border-left: 3px solid {accent}; text-align: left; }}
    .mini-val {{ font-size: 24px; font-weight: 900; color: #FFF; margin-top: 5px; }}
    .mini-lbl {{ font-size: 10px; color: #888; text-transform: uppercase; letter-spacing: 1px; font-weight: bold; }}

    .footer {{ position: absolute; bottom: 25px; left: 45px; right: 45px; display: flex; justify-content: space-between; align-items: center; color: #555; font-size: 10px; border-top: 1px solid #111; padding-top: 15px; font-weight: bold; letter-spacing: 1px; }}
    </style>
    """

    html = f"""
    <html><head>{css}</head><body>

    <div class="page">
        <div class="bg-glow"></div>
        <img src="data:image/png;base64,{logo_overlay}" class="overlay-logo">

        <div class="content" style="text-align:center; padding-top:50px;">
            <img src="data:image/png;base64,{logo_main}" class="hero-logo">
            <div class="hero-title">SISTEMA ÉLITE</div>
            <div class="hero-sub">INGENIERÍA FÍSICA DE ALTO RENDIMIENTO</div>

            <div class="premium-card" style="margin-top:50px; padding: 40px;">
                <div class="label">ATLETA AUTORIZADO</div>
                <div class="athlete-name" style="margin-top:10px;">{str(data.get('n','ATLETA')).upper()}</div>
                <div style="margin-top:10px; color:#888; font-size:12px; letter-spacing: 2px; font-weight: bold;">NIVEL: {str(data.get('nivel','PRINCIPIANTE')).upper()}</div>

                <table style="width: 100%; border-collapse: separate; border-spacing: 15px; margin-top: 25px; margin-left: -15px; margin-right: -15px;">
                    <tr>
                        <td class="mini-card" style="width: 50%;">
                            <div class="mini-lbl">CALORÍAS OBJETIVO</div>
                            <div class="mini-val">{safe_int(data.get('k',0))} <span style="font-size:14px; color:{accent};">KCAL</span></div>
                        </td>
                        <td class="mini-card" style="width: 50%;">
                            <div class="mini-lbl">PROTEÍNAS</div>
                            <div class="mini-val">{safe_int(data.get('p',0))} <span style="font-size:14px; color:{accent};">G</span></div>
                        </td>
                    </tr>
                    <tr>
                        <td class="mini-card" style="width: 50%;">
                            <div class="mini-lbl">CARBOHIDRATOS</div>
                            <div class="mini-val">{safe_int(data.get('c',0))} <span style="font-size:14px; color:{accent};">G</span></div>
                        </td>
                        <td class="mini-card" style="width: 50%;">
                            <div class="mini-lbl">GRASAS</div>
                            <div class="mini-val">{safe_int(data.get('g',0))} <span style="font-size:14px; color:{accent};">G</span></div>
                        </td>
                    </tr>
                </table>

                <div style="margin-top: 30px;">
                    <img src="data:image/png;base64,{qr}" style="width:75px; background:white; padding:5px; border-radius:10px; border:2px solid {accent}; box-shadow: 0 5px 15px rgba(0,0,0,0.5);">
                </div>
            </div>
        </div>

        <div class="footer">
            <div style="text-align: left;">EDDY ELITE SYSTEM © {datetime.now().year}</div>
            <div style="text-align: right; color:{accent};">DISEÑO DE ALTO RENDIMIENTO</div>
        </div>
    </div>

    <div class="page">
        <div class="bg-glow"></div>
        <div class="content">
            <div class="section-title">ANALÍTICA CORPORAL</div>

            <table style="width: 100%; border-collapse: separate; border-spacing: 0;">
                <tr>
                    <td style="width: 33%;">{generate_gauge(100, accent, 'EDAD', f"{safe_int(data.get('edad',0))}")}</td>
                    <td style="width: 33%;">{generate_gauge(85, accent, 'ESTATURA', f"{safe_int(data.get('estatura',0))}")}</td>
                    <td style="width: 33%;">{generate_gauge(75, accent, 'PESO (KG)', f"{safe_int(data.get('peso',0))}")}</td>
                </tr>
            </table>

            <table style="width: 100%; border-collapse: separate; border-spacing: 15px; margin-left: -15px; margin-right: -15px;">
                <tr>
                    <td style="width: 50%; vertical-align: top;">
                        <div class="premium-card" style="text-align:center; padding: 25px;">
                            <div style="color:#888; font-size:10px; letter-spacing:2px; font-weight:bold; margin-bottom:10px;">OBJETIVO ESTRATÉGICO</div>
                            <div style="font-size:22px; font-weight:900; color:{accent}; text-transform: uppercase;">{str(data.get('meta','')).upper()}</div>
                        </div>
                    </td>
                    <td style="width: 50%; vertical-align: top;">
                        <div class="premium-card" style="text-align:center; padding: 25px;">
                            <div style="color:#888; font-size:10px; letter-spacing:2px; font-weight:bold; margin-bottom:10px;">AGUA / GRASA CORP.</div>
                            <div style="font-size:24px; font-weight:900; color:#FFF;">{data.get('w',3)}L <span style="color:{accent}; font-weight:300;">|</span> {safe_int(data.get('rfm',0))}%</div>
                        </div>
                    </td>
                </tr>
            </table>

            <div class="premium-card" style="padding: 25px; text-align: center;">
                <div style="color:#888; font-size:11px; letter-spacing:2px; font-weight:bold; margin-bottom:15px; text-transform: uppercase;">EVOLUCIÓN PREDICTIVA</div>
                <img src="data:image/png;base64,{grafico_b64}" style="width:100%; border-radius:12px; border:1px solid rgba(255,255,255,0.1); box-shadow: 0 10px 20px rgba(0,0,0,0.8);">
            </div>
        </div>
        <div class="footer">
            <div style="text-align: left;">EDDY ELITE SYSTEM</div><div style="text-align: right;">ANALÍTICA CORPORAL</div>
        </div>
    </div>

    <div class="page">
        <div class="bg-glow"></div>
        <div class="content">
            <div class="section-title">SISTEMA NUTRICIONAL</div>

            <div class="premium-card" style="padding: 30px;">
                {macro_bar('PROTEÍNAS', data.get('p',0), 90, accent)}
                {macro_bar('CARBOHIDRATOS', data.get('c',0), 75, '#00BFFF')}
                {macro_bar('GRASAS', data.get('g',0), 55, '#FF9800')}
            </div>
    """
    
    for comida, opciones in data.get('m', {}).items():
        html += f"""
            <div class="premium-card" style="padding: 20px; border-left: 4px solid {accent}; margin-bottom: 15px;">
                <div style="font-size: 15px; font-weight: 900; color: {accent}; letter-spacing: 1px; margin-bottom: 8px; text-transform: uppercase;">{comida}</div>
                <div style="font-size: 12px; color: #CCC; line-height: 1.6;">{str(opciones[0]).strip() if opciones else ""}</div>
            </div>
        """

    html += f"""
        </div>
        <div class="footer">
            <div style="text-align: left;">EDDY ELITE SYSTEM</div><div style="text-align: right;">PLAN DE ALIMENTACIÓN</div>
        </div>
    </div>

    <div class="page">
        <div class="bg-glow"></div>
        <div class="content">
            <div class="section-title">PROTOCOLO DE ENTRENAMIENTO</div>
            
            <table style="width: 100%; border-collapse: separate; border-spacing: 15px; margin-left: -15px; margin-right: -15px;">
                <tr>
                    <td style="width: 50%; vertical-align: top;">
                        <div class="premium-card" style="padding: 20px; text-align: center;">
                            <div class="mini-lbl" style="margin-bottom: 5px;">MODALIDAD</div>
                            <div style="font-size: 16px; font-weight: 900; color: #FFF; text-transform: uppercase;">{str(data.get('entreno','')).upper()}</div>
                        </div>
                    </td>
                    <td style="width: 50%; vertical-align: top;">
                        <div class="premium-card" style="padding: 20px; text-align: center;">
                            <div class="mini-lbl" style="margin-bottom: 5px;">FRECUENCIA</div>
                            <div style="font-size: 16px; font-weight: 900; color: #FFF; text-transform: uppercase;">{str(data.get('dias',''))} DÍAS/SEM</div>
                        </div>
                    </td>
                </tr>
            </table>
    """
    
    for dia, ejercicios in data.get('rutina', {}).items():
        html += f"""
            <div class="premium-card" style="padding: 20px; margin-bottom: 15px;">
                <div style="font-size: 16px; font-weight: 900; color: {accent}; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 8px; margin-bottom: 12px; text-transform: uppercase;">{dia}</div>
        """
        for ej in ejercicios:
            html += f'<div style="font-size: 12px; color: #DDD; padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.05);"><span style="color:{accent}; font-weight:bold; margin-right:8px;">›</span>{str(ej).strip()}</div>'
        html += "</div>"

    html += f"""
        </div>
        <div class="footer">
            <div style="text-align: left;">EDDY ELITE SYSTEM</div><div style="text-align: right;">RUTINA Y RENDIMIENTO</div>
        </div>
    </div>

    <div class="page">
        <div class="bg-glow"></div>
        <div class="content">
            <div class="section-title">LISTA DE ABASTECIMIENTO</div>
            
            <div class="premium-card" style="padding: 30px;">
                <table style="width: 100%; border-collapse: collapse;">
    """
    
    for item, cant in data.get('compras', {}).items():
        it = str(item).replace('\n', '').strip()
        c_val = safe_int(cant)
        
        if "Huevo" in it or "Claras" in it: res = f"{safe_int(c_val/50)} Uni."
        elif any(x in it for x in ["Café", "Mate", "Té", "Infusión"]): res = f"{c_val} Tazas"
        else: res = f"{c_val/1000:.2f} KG" if c_val>=1000 else f"{c_val} g"
        
        html += f'<tr><td style="padding: 12px 0; border-bottom: 1px solid rgba(255,255,255,0.05); font-size: 12px; color: #EEE; text-transform: capitalize;">{it}</td><td style="padding: 12px 0; border-bottom: 1px solid rgba(255,255,255,0.05); text-align: right; font-size: 14px; font-weight: 900; color: {accent};">{res}</td></tr>'

    html += f"""
                </table>
            </div>
            
            <div style="text-align:center; margin-top:40px;">
                <img src="data:image/png;base64,{logo_main}" style="width: 150px; opacity: 0.5;">
            </div>
        </div>
        <div class="footer">
            <div style="text-align: left;">EDDY ELITE SYSTEM</div><div style="text-align: right;">COMPRAS Y SUMINISTROS</div>
        </div>
    </div>

    </body></html>
    """

    return HTML(string=html).write_pdf()