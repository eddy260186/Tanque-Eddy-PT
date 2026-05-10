import os
import base64
from datetime import datetime
from weasyprint import HTML

# =========================================================
# EDDY ELITE PDF ENGINE V80.1 (WEASYPRINT BLINDADO)
# BLACK GOLD / RUBY EDITION - CINEMATIC FITNESS SYSTEM
# =========================================================

def safe_int(value):
    """Filtro de titanio: Aniquila decimales basuras."""
    try: return int(round(float(value)))
    except: return 0

def img_to_b64(path):
    """Convierte imágenes a Base64 de forma segura."""
    if path and os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return ""
# =========================================================
# THEMES
# =========================================================

THEMES = {
    "gold": {
        "accent": "#D4AF37",
        "bright": "#FFD700",
        "soft": "rgba(212,175,55,0.12)",
        "card": "#111111",
        "border": "rgba(212,175,55,0.25)",
        "text": "#FFFFFF",
        "muted": "#8A8A8A",
        "logo": "logo_dorado.png",
        "overlay": "logo_dorado.png"
    },
    "ruby": {
        "accent": "#FF2D75",
        "bright": "#FF73A8",
        "soft": "rgba(255,45,117,0.12)",
        "card": "#111111",
        "border": "rgba(255,45,117,0.25)",
        "text": "#FFFFFF",
        "muted": "#8A8A8A",
        "logo": "logo_rosa.png",
        "overlay": "logo_rosa.png"
    }
}
# =========================================================
# SVG PREMIUM GAUGE
# =========================================================

def generate_gauge(percent, color, title, value):
    circumference = 339.292
    p = min(max(float(percent), 0), 100)
    offset = circumference - (p / 100) * circumference

    return f"""
    <div style="text-align:center; width:100%; padding: 10px 0;">
        <div style="font-size:10px; letter-spacing:2px; color:#888; margin-bottom:10px; text-transform:uppercase; font-weight:bold;">
            {title}
        </div>
        <svg width="140" height="140" viewBox="0 0 220 220" style="overflow: visible;">
            <circle cx="110" cy="110" r="54" stroke="#000" stroke-width="16" fill="none" style="filter: drop-shadow(0 5px 10px rgba(0,0,0,0.9));"/>
            <circle cx="110" cy="110" r="54" stroke="#1F1F1F" stroke-width="12" fill="none"/>
            <circle cx="110" cy="110" r="54" stroke="{color}" stroke-width="12" fill="none"
                stroke-linecap="round" stroke-dasharray="{circumference}" stroke-dashoffset="{offset}"
                transform="rotate(-90 110 110)" style="filter: drop-shadow(0 0 10px {color});" />
            <text x="50%" y="53%" dominant-baseline="middle" text-anchor="middle" fill="white" font-size="34" font-weight="900" font-family="Arial">
                {value}
            </text>
        </svg>
    </div>
    """
# =========================================================
# MACRO BAR
# =========================================================

def macro_bar(title, grams, percent, accent):
    p = min(max(float(percent), 0), 100)
    g_val = safe_int(grams)
    return f"""
    <div style="margin-bottom:25px;">
        <table style="width: 100%; margin-bottom: 8px;">
            <tr>
                <td style="text-align: left; color:white; font-size:12px; font-weight:700; letter-spacing:1px; text-transform:uppercase;">{title}</td>
                <td style="text-align: right; color:{accent}; font-size:16px; font-weight:900;">{g_val}g</td>
            </tr>
        </table>
        <div style="height:12px; border-radius:10px; background:#1A1A1A; box-shadow: inset 0 2px 4px rgba(0,0,0,0.8);">
            <div style="width:{p}%; height:100%; border-radius:10px; background:linear-gradient(90deg, {accent}, #FFF); box-shadow:0 0 15px {accent};"></div>
        </div>
    </div>
    """
# =========================================================
# PDF ENGINE MAIN
# =========================================================

def build_pdf_elite_v80(data, grafico_b64="", genero="m"):
    theme = THEMES["ruby"] if genero == "f" else THEMES["gold"]
    
    accent = theme["accent"]
    bright = theme["bright"]
    soft = theme["soft"]
    border = theme["border"]
    
    logo_main = img_to_b64(theme["logo"])
    logo_overlay = img_to_b64(theme["overlay"])
    logo_tanque = img_to_b64("logo_tanque.png")
    qr = img_to_b64("qr_code.png")

    css = f"""
    <style>
    @page {{ size: A4; margin: 0; background: #050505; }}
    body {{ margin: 0; padding: 0; font-family: Arial, Helvetica, sans-serif; color: #FFF; background: #050505; }}
    
    .page-container {{ width: 210mm; min-height: 297mm; position: relative; padding: 45px; page-break-after: always; box-sizing: border-box; }}
    """
    css += f"""
    /* FONDOS Y EFECTOS SEGUROS PARA WEASYPRINT */
    .bg-glow {{ position: absolute; width: 800px; height: 800px; border-radius: 50%; background: radial-gradient(circle, {soft}, transparent 70%); top: -300px; left: -100px; z-index: -1; }}
    
    .hero-title {{ font-size: 58px; font-weight: 900; margin-top: 20px; letter-spacing: 8px; color: {accent}; text-shadow: 0 4px 15px rgba(0,0,0,0.8); text-transform: uppercase; }}
    .hero-sub {{ color: #888; letter-spacing: 5px; font-size: 11px; font-weight: bold; margin-top: 10px; text-transform: uppercase; }}

    .premium-card {{
        background: linear-gradient(145deg, #111, #080808);
        border: 1px solid {border}; border-top: 2px solid {accent}; border-radius: 20px;
        box-shadow: 0 15px 30px rgba(0,0,0,0.9), inset 0 2px 5px rgba(255,255,255,0.03);
        position: relative; overflow: hidden; margin-bottom: 25px;
        page-break-inside: avoid;
    }}
    .premium-card::before {{ content: ''; position: absolute; width: 200px; height: 40px; background: rgba(255,255,255,0.03); transform: rotate(-35deg); top: -10px; left: -100px; }}

    .section-title {{ font-size: 24px; font-weight: 900; letter-spacing: 3px; margin-bottom: 25px; color: #FFF; text-transform: uppercase; border-bottom: 1px solid #222; padding-bottom: 10px; }}
    
    .grid-table {{ width: 100%; border-collapse: separate; border-spacing: 15px; margin-left: -15px; margin-right: -15px; }}
    .grid-td {{ vertical-align: top; text-align: center; }}
    </style>
    """
    html = f"""
    <html><head>{css}</head><body>

    <div class="page-container" style="text-align:center;">
        <div class="bg-glow"></div>
        <table style="width: 100%; height: 850px; border-collapse: collapse;">
            <tr>
                <td style="vertical-align: top; padding-top: 50px;">
                    <img src="data:image/png;base64,{logo_main}" style="width: 200px; filter: drop-shadow(0 0 20px {accent});">
                    <div class="hero-title">EDDY ELITE</div>
                    <div class="hero-sub">HIGH PERFORMANCE SYSTEM</div>

                    <div class="premium-card" style="margin-top: 60px; padding: 45px; width: 85%; margin-left: auto; margin-right: auto;">
                        <div style="font-size: 13px; color: {accent}; letter-spacing: 3px; font-weight: bold; margin-bottom: 15px;">AUTHORIZED ATHLETE</div>
                        <div style="font-size: 45px; font-weight: 900; letter-spacing: 2px;">{str(data.get('n','ATLETA')).upper()}</div>
                        <div style="margin-top: 10px; color: #888; font-size: 12px; letter-spacing: 2px;">LEVEL: {str(data.get('nivel','ELITE')).upper()}</div>
                    </div>
                </td>
            </tr>
            <tr>
                <td style="vertical-align: bottom; height: 150px;">
                    <table style="width: 100%;">
                        <tr>
                            <td style="text-align: left; width: 50%;"><img src="data:image/png;base64,{qr}" style="width: 80px; border-radius: 12px; border: 2px solid {accent}; padding: 5px; background: #FFF;"></td>
                            <td style="text-align: right; width: 50%;">
                                <div style="font-style: italic; font-size: 35px; color: #666; font-weight: bold;">Eddy</div>
                                <div style="font-size: 10px; color: {accent}; letter-spacing: 2px; font-weight: bold;">PERFORMANCE DIRECTOR</div>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </div>
    """
    html += f"""
    <div class="page-container">
        <div class="bg-glow" style="top: 200px;"></div>
        <div class="section-title">BODY ANALYTICS</div>
        
        <table class="grid-table">
            <tr>
                <td class="grid-td"><div class="premium-card" style="padding:15px;">{generate_gauge(100, accent, 'EDAD', safe_int(data.get('edad',0)))}</div></td>
                <td class="grid-td"><div class="premium-card" style="padding:15px;">{generate_gauge(85, accent, 'ALTURA', safe_int(data.get('estatura',0)))}</div></td>
                <td class="grid-td"><div class="premium-card" style="padding:15px;">{generate_gauge(75, accent, 'PESO (KG)', safe_int(data.get('peso',0)))}</div></td>
            </tr>
        </table>

        <table style="width: 100%; margin-bottom: 25px;">
            <tr>
                <td style="width: 50%; padding-right: 10px;">
                    <div class="premium-card" style="padding: 25px; text-align: center;">
                        <div style="color: #888; font-size: 11px; letter-spacing: 2px; margin-bottom: 10px;">OBJETIVO PRINCIPAL</div>
                        <div style="font-size: 20px; font-weight: 900; color: {accent};">{str(data.get('meta','')).upper()}</div>
                    </div>
                </td>
                <td style="width: 50%; padding-left: 10px;">
                    <div class="premium-card" style="padding: 25px; text-align: center;">
                        <div style="color: #888; font-size: 11px; letter-spacing: 2px; margin-bottom: 10px;">HIDRATACIÓN / RFM</div>
                        <div style="font-size: 20px; font-weight: 900; color: #FFF;">{data.get('w',3)}L <span style="color:{accent};">|</span> {safe_int(data.get('rfm',0))}%</div>
                    </div>
                </td>
            </tr>
        </table>

        <div class="premium-card" style="padding: 25px; text-align: center;">
            <div style="color: #888; font-size: 11px; letter-spacing: 2px; margin-bottom: 15px;">PREDICTIVE EVOLUTION</div>
            <img src="data:image/png;base64,{grafico_b64}" style="width: 100%; border-radius: 12px; border: 1px solid #222;">
        </div>
    </div>
    """
    html += f"""
    <div class="page-container">
        <div class="section-title">NUTRITION SYSTEM</div>
        
        <div class="premium-card" style="padding: 30px;">
            {macro_bar('PROTEÍNAS', data.get('p',0), 90, accent)}
            {macro_bar('CARBOHIDRATOS', data.get('c',0), 75, '#00BFFF')}
            {macro_bar('GRASAS', data.get('g',0), 55, '#FF9800')}
            
            <div style="text-align: center; margin-top: 25px; padding-top: 15px; border-top: 1px solid #222;">
                <span style="font-size: 12px; color: #888; letter-spacing: 2px;">CALORÍAS OBJETIVO: </span>
                <span style="font-size: 18px; font-weight: 900; color: #FFF;">{safe_int(data.get('k',0))} KCAL</span>
            </div>
        </div>
    """

    for comida, opciones in data.get('m', {}).items():
        html += f"""
        <div class="premium-card" style="padding: 20px; border-left: 5px solid {accent}; margin-bottom: 15px;">
            <div style="font-size: 14px; color: {accent}; font-weight: 900; letter-spacing: 1px; margin-bottom: 8px;">{comida.upper()}</div>
            <div style="font-size: 12px; color: #CCC; line-height: 1.6;">{str(opciones[0]).strip() if opciones else ""}</div>
        </div>
        """
        
    html += "</div>"
    html += f"""
    <div class="page-container">
        <div class="section-title">WORKOUT PROTOCOL</div>
        
        <div class="premium-card" style="padding: 20px; text-align: center;">
            <span style="color:#888; font-size:12px; letter-spacing:2px; margin-right:15px;">MODALIDAD: <span style="color:#FFF; font-weight:bold;">{str(data.get('entreno','')).upper()}</span></span>
            <span style="color:#888; font-size:12px; letter-spacing:2px;">FRECUENCIA: <span style="color:#FFF; font-weight:bold;">{str(data.get('dias',''))} DÍAS/SEM</span></span>
        </div>
    """
    
    for dia, ejercicios in data.get('rutina', {}).items():
        html += f"""
        <div class="premium-card" style="padding: 20px; margin-bottom: 15px;">
            <div style="font-size: 16px; color: {accent}; font-weight: 900; border-bottom: 1px solid #222; padding-bottom: 10px; margin-bottom: 12px;">{dia.upper()}</div>
        """
        for ej in ejercicios:
            html += f'<div style="font-size: 12px; color: #DDD; padding: 6px 0; border-bottom: 1px dashed #1A1A1A;"><span style="color:{accent}; font-weight:bold; margin-right:8px;">›</span>{str(ej).strip()}</div>'
        html += "</div>"

    html += f"""
        <div class="section-title" style="margin-top: 40px;">SUPPLY LIST</div>
        <div class="premium-card" style="padding: 25px;">
            <table style="width: 100%; border-collapse: collapse;">
    """
    
    for item, cant in data.get('compras', {}).items():
        it = str(item).replace('\n', '').strip()
        c_val = safe_int(cant)
        
        if "Huevo" in it or "Claras" in it: res = f"{safe_int(c_val/50)} Uni."
        elif any(x in it for x in ["Café", "Mate", "Té", "Infusión"]): res = f"{c_val} Tazas"
        else: res = f"{c_val/1000:.2f} KG" if c_val>=1000 else f"{c_val} g"
        
        html += f'<tr><td style="padding: 12px 0; border-bottom: 1px solid #1A1A1A; font-size: 12px; color: #EEE;">{it}</td><td style="padding: 12px 0; border-bottom: 1px solid #1A1A1A; text-align: right; font-size: 14px; font-weight: 900; color: {accent};">{res}</td></tr>'

    html += f"""
            </table>
        </div>
        <div style="text-align: center; margin-top: 50px; opacity: 0.3;">
            <div style="font-size: 10px; color: #FFF; letter-spacing: 5px;">EDDY ELITE PERFORMANCE SYSTEM</div>
        </div>
    </div>
    </body></html>
    """

    # Retorna los bytes directamente para que Streamlit los pueda descargar
    return HTML(string=html).write_pdf()