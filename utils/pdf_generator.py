import os
import base64
from weasyprint import HTML

# =========================================================
# EDDY PT ELITE - LUXURY SAAS ENGINE V23.0
# =========================================================

def generate_gauge_svg(percent, color, label_value):
    """Gauges con efecto Neon Glow (drop-shadow)"""
    circumference = 251.2
    p = min(max(float(percent), 0), 100)
    offset = circumference - (p / 100) * circumference
    
    return f'''
    <div style="text-align: center;">
        <svg width="90" height="90" viewBox="0 0 120 120" style="overflow: visible;">
            <circle cx="60" cy="60" r="40" stroke="#1A1A1A" stroke-width="8" fill="none" />
            <circle cx="60" cy="60" r="40" stroke="{color}" stroke-width="8" fill="none"
                stroke-linecap="round" stroke-dasharray="{circumference}" 
                stroke-dashoffset="{offset}" transform="rotate(-90 60 60)" 
                style="filter: drop-shadow(0 0 6px {color});" />
            <text x="50%" y="53%" dominant-baseline="middle" text-anchor="middle" 
                fill="white" font-size="24" font-weight="bold" font-family="Arial">{label_value}</text>
        </svg>
    </div>
    '''

def img_to_b64(path):
    if path and os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return ""
def render_macro_bar(title, grams, percent, accent):
    p = min(max(float(percent), 0), 100)
    return f"""
    <div class="premium-card" style="padding:16px; margin-bottom:15px; border-radius:10px;">
        <div style="display:flex; justify-content:space-between; font-size:11px; margin-bottom:8px; font-weight:bold; letter-spacing:1px; color:#FFF;">
            <span>{title}</span>
            <span style="color:{accent};">{grams}g</span>
        </div>
        <div style="height:8px; background:#1A1A1A; border-radius:10px; overflow:visible;">
            <div style="height:100%; width:{p}%; background:{accent}; border-radius:10px; color:{accent}; box-shadow:0 0 12px currentColor;"></div>
        </div>
    </div>
    """

THEMES = {
    "gold": {"acc": "#D4AF37", "bright": "#FFD700", "dark": "rgba(212,175,55,0.15)", "logo": "logo_dorado.png", "overlay": "overlay_gold.png"},
    "ruby": {"acc": "#C2185B", "bright": "#FF4D8D", "dark": "rgba(194,24,91,0.15)", "logo": "logo_rosa.png", "overlay": "overlay_ruby.png"}
}
def build_pdf_v60_7(d, grafico_b64="", ruta_img="", gen="m"):
    theme = THEMES["ruby"] if gen == "f" else THEMES["gold"]
    c_acc = theme["acc"]; c_bright = theme["bright"]; c_dark = theme["dark"]; overlay = theme["overlay"]
    
    css = f"""
    <style>
        @page {{ size: A4; margin: 0; background-color: #000; }}
        body {{ font-family: 'Arial', sans-serif; color: #FFF; margin: 0; padding: 0; background-color: #000; }}
        
        .page-container {{ width: 210mm; height: 297mm; overflow: hidden; position: relative; page-break-after: always; }}
        .content-padding {{ padding: 40px; }}

        /* TU UPGRADE: Texturas y Luces Radiales en la Portada */
        .cover-bg {{
            background: 
                radial-gradient(circle at top, rgba(255,255,255,0.03), transparent 50%),
                radial-gradient(circle, {c_dark}, transparent 80%),
                #000;
            background-image: url('{overlay}');
            background-size: cover;
            background-blend-mode: overlay;
        }}

        /* TU UPGRADE: Efecto Metal en Texto */
        .metal-text {{
            background: linear-gradient(180deg, #FFF3B0, {c_bright}, {c_acc});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            color: {c_acc}; /* Fallback seguro */
        }}

        /* TU UPGRADE: Profundidad, Relieve y Light Streaks (Lamborghini) */
        .premium-card {{
            background: linear-gradient(145deg, rgba(255,255,255,0.03), rgba(255,255,255,0.008));
            box-shadow: inset 0 1px 1px rgba(255,255,255,0.04), inset 0 -2px 4px rgba(0,0,0,0.45), 0 10px 25px rgba(0,0,0,0.85);
            border-radius: 15px;
            position: relative;
            overflow: hidden;
        }}
        .premium-card:before {{
            content: '';
            position: absolute;
            width: 200px; height: 40px;
            background: rgba(255,255,255,0.03);
            transform: rotate(-25deg);
            top: -20px; left: -100px;
        }}

        /* Grillas */
        .grid-table {{ width: 100%; border-collapse: separate; border-spacing: 12px; table-layout: fixed; margin-left: -12px; margin-right: -12px; }}
        .grid-td {{ vertical-align: top; }}
        
        /* Tipografías Limpias */
        .lbl-luxury {{ font-size: 9px; color: #888; text-transform: uppercase; font-weight: bold; letter-spacing: 2px; margin-bottom: 8px; }}
        
        /* TU UPGRADE: QR Premium */
        .qr-premium {{ border: 1px solid {c_acc}; padding: 5px; background: white; border-radius: 8px; width: 75px; }}
    </style>
    """
    logo_b64 = img_to_b64(theme["logo"] if os.path.exists(theme["logo"]) else ruta_img)
    qr_b64 = img_to_b64("qr_code.png")
    
    html = f"""
    <html><head>{css}</head><body>
    <div class="page-container cover-bg" style="text-align: center;">
        <div class="content-padding" style="padding-top: 80px;">
            <img src="data:image/png;base64,{logo_b64}" style="height:230px; margin-bottom:10px;">
            <div class="metal-text" style="font-family:'Arial'; font-size:55px; font-weight:900; letter-spacing:8px; margin-bottom:5px;">ELITE SYSTEM</div>
            <div style="color:#555; letter-spacing:6px; font-size:10px; font-weight:bold;">HIGH PERFORMANCE PHYSIQUE</div>
            
            <div class="premium-card" style="margin:50px auto; width:85%; padding:40px 0;">
                <div class="lbl-luxury" style="color:{c_acc}; font-size:11px;">AUTHORIZED ATHLETE</div>
                <div style="font-size:48px; font-weight:bold; margin:10px 0; color:#FFF;">{str(d.get('n','ATLETA')).upper()}</div>
                <div class="lbl-luxury" style="font-size:10px; color:#666;">TIER: {str(d.get('nivel','')).upper()}</div>
            </div>

            <table style="width:100%; margin-top:50px;">
                <tr>
                    <td style="text-align:left; width:30%;"><img src="data:image/png;base64,{qr_b64}" class="qr-premium"></td>
                    <td style="text-align:right; width:70%;">
                        <div style="font-style:italic; font-size:38px; color:#555;">Eddy</div>
                        <div class="lbl-luxury" style="font-size:9px; margin-top:5px;">DIRECTOR DE RENDIMIENTO</div>
                    </td>
                </tr>
            </table>
        </div>
    </div>

    <div class="page-container">
        <div class="content-padding">
            <div class="metal-text" style="font-size: 28px; font-weight: bold; letter-spacing: 3px; border-bottom: 1px solid #222; padding-bottom: 10px; margin-bottom: 15px;">PERFORMANCE DASHBOARD</div>
            
            <table class="grid-table">
                <tr>
                    <td class="grid-td"><div class="premium-card" style="padding:16px; text-align:center;"><div class="lbl-luxury">AGE</div>{generate_gauge_svg(100, c_acc, d.get('edad',0))}</div></td>
                    <td class="grid-td"><div class="premium-card" style="padding:16px; text-align:center;"><div class="lbl-luxury">HEIGHT</div>{generate_gauge_svg(85, c_acc, f"{d.get('estatura',0)}")}</div></td>
                    <td class="grid-td"><div class="premium-card" style="padding:16px; text-align:center;"><div class="lbl-luxury">WEIGHT</div>{generate_gauge_svg(75, c_acc, f"{d.get('peso',0)}")}</div></td>
                    <td class="grid-td"><div class="premium-card" style="padding:16px; text-align:center;"><div class="lbl-luxury">BODY FAT</div>{generate_gauge_svg(d.get('rfm',0), c_acc, f"{d.get('rfm',0)}%")}</div></td>
                </tr>
            </table>

            <div class="premium-card" style="padding:25px; margin-bottom:15px; text-align:center;">
                <div class="lbl-luxury">MAIN GOAL</div>
                <div class="metal-text" style="font-size:36px; font-weight:bold; letter-spacing:2px; margin-top:5px;">{str(d.get('meta','')).upper()}</div>
            </div>

            <div class="premium-card" style="padding:20px; text-align:center;">
                <div class="lbl-luxury">PREDICTIVE EVOLUTION</div>
                <img src="data:image/png;base64,{grafico_b64}" style="width:100%; border-radius:8px; margin-top:10px; filter: drop-shadow(0 10px 15px rgba(0,0,0,0.5));">
            </div>
        </div>
    </div>
    """
    html += f"""
    <div class="page-container">
        <div class="content-padding">
            <div class="metal-text" style="font-size: 28px; font-weight: bold; letter-spacing: 3px; border-bottom: 1px solid #222; padding-bottom: 10px; margin-bottom: 20px;">NUTRITION MATRIX</div>
            
            <div style="margin-bottom:25px;">
                {render_macro_bar("PROTEIN", d.get('p',0), 100, c_acc)}
                {render_macro_bar("CARBS", d.get('c',0), 80, "#4CAF50")}
                {render_macro_bar("FATS", d.get('g',0), 60, "#FFC107")}
            </div>
    """
    
    for comida, opciones in d.get('m', {}).items():
        html += f"""
        <div class="premium-card" style="padding:16px; margin-bottom:12px; border-left: 4px solid {c_acc}; border-radius: 0 15px 15px 0;">
            <div style="font-weight:bold; color:{c_acc}; font-size:14px; letter-spacing:1px; margin-bottom:6px;">{comida.upper()}</div>
            <div style="font-size:11px; color:#AAA; line-height:1.4;">{str(opciones[0]).strip() if opciones else ""}</div>
        </div>
        """

    html += f"""
            <div style="margin-top:40px; text-align:center; opacity:0.3;">
                <div class="lbl-luxury" style="letter-spacing:6px;">EDDY PT ELITE | PROTOCOL V23.0</div>
            </div>
        </div>
    </div></body></html>
    """

    return HTML(string=html).write_pdf()