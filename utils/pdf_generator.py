import os
import base64
from weasyprint import HTML

# =========================================================
# EDDY PT ELITE - 3D LUXURY ENGINE V26.0 (MASTERPIECE)
# =========================================================

def safe_int(value):
    """Filtro de titanio: Convierte CUALQUIER número a entero sin decimales basuras."""
    try: return int(round(float(value)))
    except: return 0

def generate_gauge_svg(percent, color, label_value):
    """Gauge con efecto Neón perfecto y centrado."""
    circumference = 251.2
    p = min(max(float(percent), 0), 100)
    offset = circumference - (p / 100) * circumference
    
    return f'''
    <div style="text-align: center; padding: 10px 0;">
        <svg width="85" height="85" viewBox="0 0 120 120" style="overflow: visible;">
            <circle cx="60" cy="60" r="40" stroke="#0a0a0a" stroke-width="12" fill="none" style="filter: drop-shadow(0 4px 4px rgba(0,0,0,0.8));" />
            <circle cx="60" cy="60" r="40" stroke="#1A1A1A" stroke-width="8" fill="none" />
            <circle cx="60" cy="60" r="40" stroke="{color}" stroke-width="8" fill="none"
                stroke-linecap="round" stroke-dasharray="{circumference}" 
                stroke-dashoffset="{offset}" transform="rotate(-90 60 60)" />
            <text x="50%" y="53%" dominant-baseline="middle" text-anchor="middle" 
                fill="#FFFFFF" font-size="26" font-weight="900" font-family="Arial" letter-spacing="1">{label_value}</text>
        </svg>
    </div>
    '''

def img_to_b64(path):
    if path and os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return ""def render_macro_bar(icon, title, grams, percent, accent):
    """Barra de Macros 3D con Icono integrado."""
    p = min(max(float(percent), 0), 100)
    g_val = safe_int(grams)
    
    return f"""
    <div class="card-3d" style="padding: 15px; margin-bottom: 15px;">
        <table style="width: 100%;">
            <tr>
                <td style="width: 40px;"><div class="icon-badge" style="border-color: {accent}; color: {accent};">{icon}</div></td>
                <td style="text-align: left;"><span class="lbl-luxury" style="margin: 0;">{title}</span></td>
                <td style="text-align: right;"><span class="val-3d" style="color: {accent}; font-size: 18px;">{g_val}g</span></td>
            </tr>
        </table>
        <div style="height: 8px; background: #050505; border-radius: 10px; margin-top: 10px; box-shadow: inset 0 2px 4px rgba(0,0,0,0.8);">
            <div style="height: 100%; width: {p}%; background: linear-gradient(90deg, {accent}, #FFF); border-radius: 10px; box-shadow: 0 0 10px {accent};"></div>
        </div>
    </div>
    """

THEMES = {
    "gold": {"acc": "#D4AF37", "dark": "rgba(212,175,55,0.1)", "logo": "logo_dorado.png"},
    "ruby": {"acc": "#C2185B", "dark": "rgba(194,24,91,0.1)", "logo": "logo_rosa.png"}
}
def build_pdf_v60_7(d, grafico_b64="", ruta_img="", gen="m"):
    theme = THEMES["ruby"] if gen == "f" else THEMES["gold"]
    c_acc = theme["acc"]; c_dark = theme["dark"]
    
    css = f"""
    <style>
        @page {{ size: A4; margin: 0; background-color: #030303; }}
        body {{ font-family: 'Arial', sans-serif; color: #FFF; margin: 0; padding: 0; background: #030303; }}
        
        .page-container {{ width: 210mm; min-height: 297mm; padding: 45px; page-break-after: always; box-sizing: border-box; }}
        
        /* Efectos 3D y Gradientes */
        .card-3d {{
            background: linear-gradient(145deg, #111111, #0a0a0a);
            border: 1px solid #1c1c1c;
            border-top: 3px solid {c_acc};
            border-radius: 15px;
            box-shadow: 0 15px 25px rgba(0,0,0,0.8), inset 0 2px 2px rgba(255,255,255,0.05);
            page-break-inside: avoid; /* NUNCA SE CORTA A LA MITAD */
        }}
        
        /* Iconos Espectaculares */
        .icon-badge {{
            display: inline-block; width: 32px; height: 32px; line-height: 32px;
            text-align: center; border-radius: 50%; background: #050505;
            border: 2px solid {c_acc}; font-size: 14px; box-shadow: 0 0 12px {c_dark};
        }}

        /* Tipografía Premium */
        .title-3d {{ font-size: 30px; font-weight: 900; color: #FFF; letter-spacing: 4px; text-shadow: 0 4px 10px rgba(0,0,0,0.9), 0 0 15px {c_dark}; border-bottom: 2px solid #111; padding-bottom: 12px; margin-bottom: 25px; text-transform: uppercase; }}
        .lbl-luxury {{ font-size: 10px; color: #999; text-transform: uppercase; font-weight: bold; letter-spacing: 2px; }}
        .val-3d {{ font-size: 24px; font-weight: 900; color: #FFF; text-shadow: 0 2px 5px rgba(0,0,0,0.8); margin-top: 5px; }}

        /* Grillas Rígidas (Cero Encimamientos) */
        .grid-table {{ width: 100%; border-collapse: separate; border-spacing: 15px; margin-left: -15px; margin-right: -15px; }}
        .grid-td {{ vertical-align: top; }}
    </style>
    """
    logo_b64 = img_to_b64(theme["logo"] if os.path.exists(theme["logo"]) else ruta_img)
    qr_b64 = img_to_b64("qr_code.png")
    
    html = f"""
    <html><head>{css}</head><body>
    
    <div class="page-container" style="background: radial-gradient(circle at center, {c_dark}, #030303 80%);">
        <table style="width: 100%; height: 850px; border-collapse: collapse;">
            <tr>
                <td style="vertical-align: middle; text-align: center;">
                    <img src="data:image/png;base64,{logo_b64}" style="height: 240px; margin-bottom: 20px; filter: drop-shadow(0 10px 20px rgba(0,0,0,0.9));">
                    <div class="title-3d" style="border: none; font-size: 55px; color: {c_acc}; letter-spacing: 8px; margin-bottom: 5px;">ELITE SYSTEM</div>
                    <div style="color: #888; font-size: 12px; letter-spacing: 8px; font-weight: bold;">ENGINEERED PHYSIQUE</div>
                    
                    <div class="card-3d" style="margin: 60px auto; width: 85%; padding: 40px 0;">
                        <div class="icon-badge" style="margin-bottom: 10px;">👑</div>
                        <div class="lbl-luxury" style="color: {c_acc};">ATHLETE PROFILE</div>
                        <div class="val-3d" style="font-size: 45px; margin: 15px 0; line-height: 1.1;">{str(d.get('n','ATLETA')).upper()}</div>
                        <div class="lbl-luxury">TIER: {str(d.get('nivel','')).upper()}</div>
                    </div>
                </td>
            </tr>
            <tr>
                <td style="vertical-align: bottom; height: 120px;">
                    <table style="width: 100%;">
                        <tr>
                            <td style="width: 20%;"><img src="data:image/png;base64,{qr_b64}" style="width: 80px; border-radius: 10px; border: 2px solid {c_acc}; padding: 4px; background: #FFF;"></td>
                            <td style="text-align: right; width: 80%;">
                                <div style="font-size: 40px; font-weight: 900; color: #555; font-style: italic; letter-spacing: 2px;">Eddy</div>
                                <div class="lbl-luxury" style="color: {c_acc};">HEAD COACH & DIRECTOR</div>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </div>

    <div class="page-container">
        <div class="title-3d">📊 PERFORMANCE DASHBOARD</div>
        
        <table class="grid-table">
            <tr>
                <td class="grid-td"><div class="card-3d" style="padding: 20px; text-align: center;"><div class="lbl-luxury">AGE</div>{generate_gauge_svg(100, c_acc, safe_int(d.get('edad',0)))}</div></td>
                <td class="grid-td"><div class="card-3d" style="padding: 20px; text-align: center;"><div class="lbl-luxury">HEIGHT</div>{generate_gauge_svg(85, c_acc, safe_int(d.get('estatura',0)))}</div></td>
                <td class="grid-td"><div class="card-3d" style="padding: 20px; text-align: center;"><div class="lbl-luxury">WEIGHT</div>{generate_gauge_svg(75, c_acc, safe_int(d.get('peso',0)))}</div></td>
                <td class="grid-td"><div class="card-3d" style="padding: 20px; text-align: center;"><div class="lbl-luxury">BODY FAT</div>{generate_gauge_svg(d.get('rfm',0), c_acc, f"{safe_int(d.get('rfm',0))}%")}</div></td>
            </tr>
        </table>

        <div class="card-3d" style="padding: 30px; margin-bottom: 25px; text-align: center; border-left: none; border-right: none; border-bottom: none;">
            <div class="icon-badge" style="margin-bottom: 10px;">🎯</div>
            <div class="lbl-luxury">STRATEGIC GOAL</div>
            <div class="val-3d" style="color: {c_acc}; font-size: 32px; letter-spacing: 2px;">{str(d.get('meta','')).upper()}</div>
        </div>

        <div class="card-3d" style="padding: 20px; text-align: center;">
            <div class="lbl-luxury" style="margin-bottom: 15px;"><span class="icon-badge" style="width: 20px; height: 20px; line-height: 20px; font-size: 10px;">📈</span> PREDICTIVE EVOLUTION</div>
            <img src="data:image/png;base64,{grafico_b64}" style="width: 100%; border-radius: 8px; box-shadow: 0 5px 15px rgba(0,0,0,0.5);">
        </div>
    </div>
    """
    html += f"""
    <div class="page-container">
        <div class="title-3d">🍎 NUTRITION MATRIX</div>
        
        <div class="card-3d" style="padding: 25px; margin-bottom: 30px;">
            {render_macro_bar("🥩", "PROTEIN", d.get('p',0), 100, c_acc)}
            {render_macro_bar("🍚", "CARBS", d.get('c',0), 80, "#4CAF50")}
            {render_macro_bar("🥑", "FATS", d.get('g',0), 60, "#FFC107")}
        </div>
    """
    
    for comida, opciones in d.get('m', {}).items():
        html += f"""
        <div class="card-3d" style="padding: 20px; margin-bottom: 15px; border-left: 5px solid {c_acc};">
            <div style="display: flex; align-items: center; margin-bottom: 10px;">
                <div class="icon-badge" style="margin-right: 15px;">🍽️</div>
                <div class="val-3d" style="font-size: 18px; color: {c_acc}; text-transform: uppercase;">{comida}</div>
            </div>
            <div style="font-size: 12px; color: #CCC; line-height: 1.6; padding-left: 47px;">{str(opciones[0]).strip() if opciones else ""}</div>
        </div>
        """

    html += f"""
    </div>
    
    <div class="page-container">
        <div class="title-3d">⚡ WORKOUT PROTOCOL</div>
        
        <table style="width: 100%; margin-bottom: 25px;">
            <tr>
                <td style="width: 50%; padding-right: 10px;">
                    <div class="card-3d" style="padding: 20px; text-align: center;">
                        <div class="icon-badge">🏋️</div><br><span class="lbl-luxury">MODE</span>
                        <div class="val-3d" style="font-size: 16px;">{str(d.get('entreno','')).upper()}</div>
                    </div>
                </td>
                <td style="width: 50%; padding-left: 10px;">
                    <div class="card-3d" style="padding: 20px; text-align: center;">
                        <div class="icon-badge">📅</div><br><span class="lbl-luxury">FREQ</span>
                        <div class="val-3d" style="font-size: 16px;">{str(d.get('dias',''))} DAYS/WEEK</div>
                    </div>
                </td>
            </tr>
        </table>
    """
    
    for dia, ejercicios in d.get('rutina', {}).items():
        html += f"""
        <div class="card-3d" style="padding: 20px; margin-bottom: 15px;">
            <div class="val-3d" style="font-size: 18px; color: {c_acc}; margin-bottom: 15px; border-bottom: 1px solid #222; padding-bottom: 10px;">{dia.upper()}</div>
        """
        for ej in ejercicios:
            html += f'<div style="font-size: 13px; color: #DDD; padding: 6px 0; border-bottom: 1px dashed #222;"><span style="color:{c_acc}; margin-right:8px;">›</span> {str(ej).strip()}</div>'
        html += "</div>"

    html += f"""
    </div>

    <div class="page-container">
        <div class="title-3d">🛒 SUPPLY LIST</div>
        
        <div class="card-3d" style="padding: 25px;">
            <table style="width: 100%; border-collapse: collapse;">
    """
    
    for item, cant in d.get('compras', {}).items():
        it = str(item).replace('\n', '').strip()
        c_val = safe_int(cant)
        
        if "Huevo" in it or "Claras" in it: res = f"{safe_int(c_val/50)} Uni."
        elif any(x in it for x in ["Café", "Mate", "Té", "Infusión"]): res = f"{c_val} Tazas"
        else: res = f"{c_val/1000:.2f} KG" if c_val>=1000 else f"{c_val} g"
        
        html += f'<tr><td style="padding: 12px 0; border-bottom: 1px solid #1A1A1A; font-size: 13px; color: #EEE;">{it}</td><td style="padding: 12px 0; border-bottom: 1px solid #1A1A1A; text-align: right; font-size: 14px; font-weight: 900; color: {c_acc};">{res}</td></tr>'

    html += f"""
            </table>
        </div>
        
        <div style="margin-top: 60px; text-align: center; opacity: 0.4;">
            <div class="icon-badge" style="width: 40px; height: 40px; line-height: 40px; font-size: 18px; border-color: #555; color: #555; margin-bottom: 10px;">🏆</div>
            <div class="lbl-luxury" style="letter-spacing: 6px;">EDDY PT ELITE | ENGINEERED PROTOCOL V26</div>
        </div>
    </div>
    </body></html>
    """

    return HTML(string=html).write_pdf()