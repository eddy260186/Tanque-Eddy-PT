import os
import base64
from weasyprint import HTML

# =========================================================
# EDDY PT ELITE - MOTOR PDF ULTRA-PREMIUM V11.0 (5 PARTES)
# =========================================================

THEMES = {
    "gold": {
        "bg": "#030303",
        "bg2": "#080808",
        "card": "#0E0E0E",
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
        "txt": "#F5F5F5",
        "soft": "#8C8C8C",
        "accent": "#C2185B",
        "bright": "#FF4D8D",
        "dark": "rgba(194,24,91,0.28)",
        "edition": "RUBY BLACK ELITE",
        "logo": "logo_rosa.png"
    }
}
def img_to_b64(path):
    try:
        if not path or not os.path.exists(path): return ""
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    except: return ""

def render_logo(path, class_name):
    b64 = img_to_b64(path)
    return f'<img src="data:image/png;base64,{b64}" class="{class_name}">' if b64 else ""

def safe_val(d, key, default="0"):
    try: return d.get(key, default)
    except: return default

def render_metric_card(title, value, percent="80%", extra_class=""):
    return f"""
    <div class="card {extra_class}">
        <div class="label">{title}</div>
        <div class="value">{value}</div>
        <div class="bar-bg"><div class="bar-fill" style="width:{percent};"></div></div>
    </div>
    """
def build_pdf_v60_7(d, grafico_b64="", ruta_img="", gen="m"):
    theme = THEMES["ruby"] if gen == "f" else THEMES["gold"]
    c_bg = theme["bg"]; c_bg2 = theme["bg2"]; c_txt = theme["txt"]
    c_soft = theme["soft"]; c_accent = theme["accent"]; c_bright = theme["bright"]
    c_dark = theme["dark"]; edition = theme["edition"]

    css = f"""
    <style>
        @page {{ size: A4; margin: 0; background: {c_bg}; }}
        * {{ box-sizing: border-box; }}
        body {{ margin: 0; padding: 0; font-family: 'Montserrat', sans-serif; color: {c_txt}; line-height: 1.4; }}
        
        /* PORTADA */
        .cover {{ height: 100vh; position: relative; text-align: center; padding: 40px; background: radial-gradient(circle at center, {c_dark}, transparent 85%); }}
        .logo-main {{ height: 280px; margin-bottom: 10px; filter: drop-shadow(0 0 12px {c_accent}); }}
        .cover-title {{ font-family: 'Bebas Neue'; font-size: 68px; letter-spacing: 6px; margin: 0; background: linear-gradient(180deg, #FFF3B0, {c_bright}, {c_accent}); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        .badge {{ margin: 20px auto; padding: 10px 30px; border-radius: 50px; border: 1px solid {c_accent}; font-weight: 700; letter-spacing: 3px; display: inline-block; background: rgba(0,0,0,0.5); }}
        
        /* BOX ATLETA: Espacio garantizado */
        .athlete-section {{ width: 85%; margin: 20px auto; padding: 30px 0; border-top: 1px solid rgba(255,255,255,0.1); border-bottom: 1px solid rgba(255,255,255,0.1); }}
        .athlete-name {{ font-family: 'Bebas Neue'; font-size: 52px; color: #FFF; margin: 5px 0; letter-spacing: 2px; line-height: 1.1; }}
        
        /* FOOTER PORTADA: Subido para no caer al negro */
        .cover-footer {{ width: 100%; position: absolute; bottom: 60px; left: 0; padding: 0 50px; }}
        
        /* INTERIORES */
        .page {{ padding: 45px; page-break-before: always; }}
        .header {{ display: flex; justify-content: space-between; align-items: end; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 15px; margin-bottom: 30px; }}
        .header-title {{ font-family: 'Bebas Neue'; font-size: 36px; color: {c_accent}; letter-spacing: 2px; }}
        .logo-small {{ height: 50px; }}
        .grid {{ display: flex; flex-wrap: wrap; gap: 15px; margin-bottom: 20px; }}
        .card {{ width: 23.5%; background: {theme['card']}; border-top: 3px solid {c_accent}; border-radius: 15px; padding: 20px; text-align: center; }}
        .card-large {{ width: 100%; text-align: left; padding: 25px; }}
        .label {{ font-size: 10px; color: {c_soft}; letter-spacing: 2px; text-transform: uppercase; }}
        .value {{ font-family: 'Bebas Neue'; font-size: 32px; color: #FFF; margin-top: 5px; }}
        .bar-bg {{ width: 100%; height: 5px; background: #1A1A1A; border-radius: 10px; margin-top: 10px; }}
        .bar-fill {{ height: 100%; background: {c_accent}; border-radius: 10px; }}
        .graph {{ width: 100%; border-radius: 12px; margin-top: 15px; border: 1px solid #222; }}
        .signature {{ font-family: 'Great Vibes'; font-size: 38px; color: {c_soft}; }}
        .qr {{ width: 70px; background: white; padding: 4px; border-radius: 8px; }}
    </style>
    """
    logo_path = theme["logo"] if os.path.exists(theme["logo"]) else ruta_img
    logo_m = render_logo(logo_path, "logo-main")
    logo_s = render_logo(logo_path, "logo-small")
    qr_h = f'<img src="data:image/png;base64,{img_to_b64("qr_code.png")}" class="qr">' if os.path.exists("qr_code.png") else ""

    html_full = f"""
    <html><head>{css}</head><body>
    <div class="cover">
        {logo_m}
        <h1 class="cover-title">PLAN INTEGRAL ELITE</h1>
        <div style="color:{c_soft}; letter-spacing:4px; font-size:11px;">INGENIERÍA CORPORAL DE ALTO VALOR</div>
        <div class="badge">{edition}</div>
        
        <div class="athlete-section">
            <div class="label" style="color:{c_accent};">ATLETA DE ÉLITE</div>
            <div class="athlete-name">{str(d.get('n', 'ATLETA')).upper()}</div>
            <div class="label" style="margin-top:10px;">NIVEL: {str(d.get('nivel', 'PRINCIPIANTE')).upper()}</div>
        </div>

        <div class="cover-footer">
            <table style="width:100%; border-collapse:collapse;">
                <tr>
                    <td style="width:30%; text-align:left;">{qr_h}</td>
                    <td style="width:40%; text-align:center;">
                        <div class="label">POWERED BY EDDY PT ELITE</div>
                        <div style="font-size:11px; margin-top:5px; color:{c_soft};">FECHA: {d.get('fecha', '10/05/2026')}</div>
                    </td>
                    <td style="width:30%; text-align:right;">
                        <div class="signature">Eddy</div>
                        <div class="label" style="font-size:9px;">Personal Trainer</div>
                    </td>
                </tr>
            </table>
        </div>
    </div>

    <div class="page">
        <div class="header"><div class="header-title">ANALÍTICA FÍSICA</div>{logo_s}</div>
        <div class="grid">
            {render_metric_card("EDAD", d.get('edad','0'), "100%")}
            {render_metric_card("ESTATURA", f"{d.get('estatura','0')}CM", "85%")}
            {render_metric_card("PESO", f"{d.get('peso','0')}KG", "75%")}
            {render_metric_card("GRASA", f"{d.get('rfm','0')}%", "65%")}
        </div>
        <div class="grid">
            {render_metric_card("CINTURA", f"{d.get('cintura','0')}CM", "60%")}
            {render_metric_card("CADERA", f"{d.get('cadera','0')}CM", "60%")}
            {render_metric_card("ÍNDICE RCC", d.get('rcc','0'), "50%")}
            <div class="card" style="border-top-color:#00BFFF;"><div class="label">HIDRATACIÓN</div><div class="value" style="color:#00BFFF;">{d.get('w','0')}L</div></div>
        </div>
        <div class="card card-large" style="text-align:center; margin-bottom:15px;">
            <div class="label">OBJETIVO ESTRATÉGICO</div>
            <div class="value" style="font-size:42px;">{str(d.get('meta','')).upper()}</div>
        </div>
        <div class="card card-large">
            <div class="label">PROYECCIÓN CORPORAL</div>
            <img src="data:image/png;base64,{grafico_b64}" class="graph">
        </div>
    </div>
    """
    # NUTRICIÓN Y COMPRAS (SIMPLIFICADO PARA EVITAR CORTES)
    html_full += f"""
    <div class="page">
        <div class="header"><div class="header-title">ESTRATEGIA NUTRICIONAL</div>{logo_s}</div>
        <table style="width:100%; border-collapse:separate; border-spacing:10px; margin-bottom:20px;">
            <tr>
                <td style="background:#0E0E0E; padding:20px; border-radius:12px; text-align:center; border-top:3px solid {c_accent};">
                    <div class="label">KCAL DIARIAS</div><div class="value">{d.get('k',0):.0f}</div>
                </td>
                <td style="background:#0E0E0E; padding:20px; border-radius:12px; text-align:center; border-top:3px solid {c_accent};">
                    <div class="label">PROTEÍNAS</div><div class="value">{d.get('p',0):.0f}g</div>
                </td>
                <td style="background:#0E0E0E; padding:20px; border-radius:12px; text-align:center; border-top:3px solid {c_accent};">
                    <div class="label">CARBOS / GRASAS</div><div class="value" style="font-size:24px;">{d.get('c',0):.0f}g / {d.get('g',0):.0f}g</div>
                </td>
            </tr>
        </table>
    """
    
    for comida, opciones in d.get('m', {}).items():
        html_full += f'<div style="background:#0E0E0E; border-left:4px solid {c_accent}; padding:15px; margin-bottom:10px; border-radius:10px;">'
        html_full += f'<div style="font-family:Bebas Neue; color:{c_accent}; font-size:20px;">{comida}</div>'
        for op in opciones:
            html_full += f'<div style="font-size:11px; color:#DDD; padding:5px 0;">› {str(op).strip()}</div>'
        html_full += '</div>'

    html_full += f"""
        <div style="margin-top:40px; border-top:1px solid #333; padding-top:20px; text-align:right;">
            <div class="signature">Eddy Personal Trainer</div>
        </div>
    </div></body></html>
    """

    return HTML(string=html_full).write_pdf()