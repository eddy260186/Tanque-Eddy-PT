import os
import base64
from weasyprint import HTML

# =========================================================
# EDDY PT ELITE - LUXURY SAAS ENGINE V24 (ANTI-OVERLAP)
# =========================================================

def generate_gauge_svg(percent, color, label_value):
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
        <div style="height:8px; background:#1A1A1A; border-radius:10px; overflow:hidden;">
            <div style="height:100%; width:{p}%; background:{accent}; border-radius:10px; box-shadow:0 0 10px {accent};"></div>
        </div>
    </div>
    """

THEMES = {
    "gold": {"acc": "#D4AF37", "dark": "rgba(212,175,55,0.15)", "logo": "logo_dorado.png"},
    "ruby": {"acc": "#C2185B", "dark": "rgba(194,24,91,0.15)", "logo": "logo_rosa.png"}
}
def build_pdf_v60_7(d, grafico_b64="", ruta_img="", gen="m"):
    theme = THEMES["ruby"] if gen == "f" else THEMES["gold"]
    c_acc = theme["acc"]; c_dark = theme["dark"]
    
    css = f"""
    <style>
        @page {{ size: A4; margin: 0; background-color: #000; }}
        body {{ font-family: 'Arial', sans-serif; color: #FFF; margin: 0; padding: 0; background-color: #000; }}
        
        .page-container {{ width: 210mm; min-height: 297mm; overflow: hidden; position: relative; page-break-after: always; }}
        .content-padding {{ padding: 40px; }}

        .cover-bg {{
            background: radial-gradient(circle at top, rgba(255,255,255,0.05), transparent 60%),
                        radial-gradient(circle at center, {c_dark}, transparent 80%),
                        #050505;
        }}

        .metal-text {{ color: {c_acc}; text-shadow: 0px 2px 5px rgba(0,0,0,0.8); }}

        .premium-card {{
            background: linear-gradient(145deg, rgba(255,255,255,0.04), rgba(255,255,255,0.01));
            box-shadow: inset 0 1px 1px rgba(255,255,255,0.05), inset 0 -2px 4px rgba(0,0,0,0.5), 0 10px 25px rgba(0,0,0,0.8);
            border-radius: 15px; position: relative; overflow: hidden;
            page-break-inside: avoid; /* CRÍTICO PARA EVITAR CORTES Y SUPERPOSICIONES */
        }}
        .premium-card:before {{
            content: ''; position: absolute; width: 200px; height: 40px;
            background: rgba(255,255,255,0.04); transform: rotate(-25deg);
            top: -20px; left: -100px;
        }}

        .grid-table {{ width: 100%; border-collapse: separate; border-spacing: 10px; table-layout: fixed; margin-left: -10px; margin-right: -10px; }}
        .grid-td {{ vertical-align: top; }}
        
        .lbl-luxury {{ font-size: 9px; color: #888; text-transform: uppercase; font-weight: bold; letter-spacing: 2px; margin-bottom: 8px; }}
        .qr-premium {{ border: 1px solid {c_acc}; padding: 5px; background: white; border-radius: 8px; width: 75px; }}
    </style>
    """
    logo_b64 = img_to_b64(theme["logo"] if os.path.exists(theme["logo"]) else ruta_img)
    qr_b64 = img_to_b64("qr_code.png")
    
    html = f"""
    <html><head>{css}</head><body>
    <div class="page-container cover-bg" style="text-align: center; display: block;">
        <div class="content-padding" style="padding-top: 80px;">
            <img src="data:image/png;base64,{logo_b64}" style="height:230px; margin-bottom:10px;">
            <div class="metal-text" style="font-family:'Arial'; font-size:55px; font-weight:900; letter-spacing:8px; margin-bottom:5px;">ELITE SYSTEM</div>
            <div style="color:#666; letter-spacing:6px; font-size:10px; font-weight:bold;">HIGH PERFORMANCE PHYSIQUE</div>
            
            <div class="premium-card" style="margin:50px auto; width:85%; padding:40px 0;">
                <div class="lbl-luxury" style="color:{c_acc}; font-size:11px;">AUTHORIZED ATHLETE</div>
                <div style="font-size:48px; font-weight:bold; margin:10px 0; color:#FFF; line-height:1.1;">{str(d.get('n','ATLETA')).upper()}</div>
                <div class="lbl-luxury" style="font-size:10px; color:#888;">TIER: {str(d.get('nivel','')).upper()}</div>
            </div>

            <table style="width:100%; margin-top:60px; border-collapse: collapse;">
                <tr>
                    <td style="text-align:left; width:30%; vertical-align: middle;"><img src="data:image/png;base64,{qr_b64}" class="qr-premium"></td>
                    <td style="text-align:right; width:70%; vertical-align: middle;">
                        <div style="font-style:italic; font-size:38px; color:#666; font-family: 'Arial'; font-weight:bold;">Eddy</div>
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
                    <td class="grid-td"><div class="premium-card" style="padding:12px; text-align:center;"><div class="lbl-luxury">AGE</div>{generate_gauge_svg(100, c_acc, d.get('edad',0))}</div></td>
                    <td class="grid-td"><div class="premium-card" style="padding:12px; text-align:center;"><div class="lbl-luxury">HEIGHT</div>{generate_gauge_svg(85, c_acc, f"{d.get('estatura',0)}")}</div></td>
                    <td class="grid-td"><div class="premium-card" style="padding:12px; text-align:center;"><div class="lbl-luxury">WEIGHT</div>{generate_gauge_svg(75, c_acc, f"{d.get('peso',0)}")}</div></td>
                    <td class="grid-td"><div class="premium-card" style="padding:12px; text-align:center;"><div class="lbl-luxury">BODY FAT</div>{generate_gauge_svg(d.get('rfm',0), c_acc, f"{d.get('rfm',0)}%")}</div></td>
                </tr>
            </table>

            <div class="premium-card" style="padding:25px; margin-bottom:15px; text-align:center;">
                <div class="lbl-luxury">MAIN GOAL</div>
                <div class="metal-text" style="font-size:36px; font-weight:bold; letter-spacing:2px; margin-top:5px;">{str(d.get('meta','')).upper()}</div>
            </div>

            <div class="premium-card" style="padding:20px; text-align:center;">
                <div class="lbl-luxury">PREDICTIVE EVOLUTION</div>
                <img src="data:image/png;base64,{grafico_b64}" style="width:100%; border-radius:8px; margin-top:10px;">
            </div>
        </div>
    </div>
    """
    html += f"""
    <div class="page-container">
        <div class="content-padding">
            <div class="metal-text" style="font-size: 28px; font-weight: bold; letter-spacing: 3px; border-bottom: 1px solid #222; padding-bottom: 10px; margin-bottom: 20px;">NUTRITION MATRIX</div>
            
            <div style="margin-bottom:25px;">
                {render_macro_bar("PROTEIN", f"{d.get('p',0):.0f}", 100, c_acc)}
                {render_macro_bar("CARBS", f"{d.get('c',0):.0f}", 80, "#4CAF50")}
                {render_macro_bar("FATS", f"{d.get('g',0):.0f}", 60, "#FFC107")}
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
        </div>
    </div>
    
    <div class="page-container">
        <div class="content-padding">
            <div class="metal-text" style="font-size: 28px; font-weight: bold; letter-spacing: 3px; border-bottom: 1px solid #222; padding-bottom: 10px; margin-bottom: 20px;">WORKOUT PROTOCOL</div>
            
            <div class="premium-card" style="padding:15px; text-align:center; margin-bottom:20px;">
                <span class="lbl-luxury" style="margin-right:20px;">MODE: <span style="color:#FFF;">{str(d.get('entreno','')).upper()}</span></span>
                <span class="lbl-luxury">FREQ: <span style="color:#FFF;">{str(d.get('dias',''))} DAYS/WEEK</span></span>
            </div>
    """
    
    for dia, ejercicios in d.get('rutina', {}).items():
        html += f"""
        <div class="premium-card" style="padding:16px; margin-bottom:12px;">
            <div style="font-weight:bold; color:{c_acc}; font-size:14px; letter-spacing:1px; margin-bottom:8px;">{dia.upper()}</div>
        """
        for ej in ejercicios:
            html += f'<div style="font-size:11px; color:#AAA; padding:5px 0; border-bottom:1px solid #1A1A1A;">› {str(ej).strip()}</div>'
        html += "</div>"

    html += f"""
        </div>
    </div>

    <div class="page-container">
        <div class="content-padding">
            <div class="metal-text" style="font-size: 28px; font-weight: bold; letter-spacing: 3px; border-bottom: 1px solid #222; padding-bottom: 10px; margin-bottom: 20px;">SUPPLY LIST</div>
            
            <div class="premium-card" style="padding:20px;">
                <table style="width:100%; border-collapse:collapse;">
    """
    
    for item, cant in d.get('compras', {}).items():
        it = str(item).replace('\n', '').strip()
        if "Huevo" in it or "Claras" in it:
            res = f"{int(cant/50)} Uni."
        elif any(x in it for x in ["Café", "Mate", "Té", "Infusión"]):
            res = f"{int(cant)} Tazas"
        else:
            res = f"{round(cant/1000,2)} KG" if cant>=1000 else f"{int(cant)} g"
        
        html += f'<tr><td style="padding:12px 0; border-bottom:1px solid #1A1A1A; font-size:11px; color:#DDD;">{it}</td><td style="padding:12px 0; border-bottom:1px solid #1A1A1A; text-align:right; font-size:11px; font-weight:bold; color:{c_acc};">{res}</td></tr>'

    html += f"""
                </table>
            </div>
            
            <div style="margin-top:50px; text-align:center; opacity:0.3;">
                <div class="lbl-luxury" style="letter-spacing:6px;">EDDY PT ELITE | PROTOCOL V24</div>
            </div>
        </div>
    </div>
    </body></html>
    """

    return HTML(string=html).write_pdf()