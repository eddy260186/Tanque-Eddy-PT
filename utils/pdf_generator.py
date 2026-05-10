import os
import base64
from weasyprint import HTML

# =========================================================
# EDDY PT ELITE - VISUAL DASHBOARD ENGINE V21.0
# =========================================================

def render_gauge_card(title, value, subtitle, percent, accent):
    # Circunferencia para radio 40 = 251.2
    circumference = 251.2
    # Aseguramos que el porcentaje sea float y esté entre 0 y 100
    p = min(max(float(percent), 0), 100)
    offset = circumference - (p / 100) * circumference
    
    return f"""
    <div class="gauge-card">
        <div class="gauge-title">{title}</div>
        <svg width="100" height="100" viewBox="0 0 120 120">
            <circle cx="60" cy="60" r="40" stroke="#1A1A1A" stroke-width="8" fill="none" />
            <circle cx="60" cy="60" r="40" stroke="{accent}" stroke-width="8" fill="none"
                stroke-linecap="round" stroke-dasharray="{circumference}" 
                stroke-dashoffset="{offset}" transform="rotate(-90 60 60)" />
            <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" 
                fill="white" font-size="24" font-weight="bold" font-family="Arial">{value}</text>
        </svg>
        <div class="gauge-sub">{subtitle}</div>
    </div>
    """

def img_to_b64(path):
    if path and os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return ""
def render_macro_bar(title, grams, percent, accent):
    p = min(max(float(percent), 0), 100)
    return f"""
    <div class="macro-box">
        <div class="macro-top">
            <span style="font-weight:bold; letter-spacing:1px;">{title}</span>
            <span style="color:{accent}; font-weight:bold;">{grams}g</span>
        </div>
        <div class="macro-bg">
            <div class="macro-fill" style="width:{p}%; background:{accent}; shadow: 0 0 10px {accent};"></div>
        </div>
    </div>
    """

def render_metric_box(title, value, label, accent):
    return f"""
    <div class="metric-mini-card">
        <div class="lbl">{title}</div>
        <div class="val-small" style="color:{accent};">{value}</div>
        <div class="lbl" style="font-size:8px;">{label}</div>
    </div>
    """
def build_pdf_v60_7(d, grafico_b64="", ruta_img="", gen="m"):
    c_accent = "#C2185B" if gen == "f" else "#D4AF37"
    c_bg = "#030303"
    
    css = f"""
    <style>
        @page {{ size: A4; margin: 0; background: {c_bg}; }}
        body {{ font-family: 'Arial', sans-serif; color: #FFF; margin: 0; padding: 0; }}
        .page {{ padding: 40px; page-break-before: always; height: 100vh; position: relative; }}
        
        /* DASHBOARD GRID */
        .dashboard-grid {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
        .dashboard-td {{ padding: 5px; vertical-align: top; }}
        
        /* GAUGE CARDS */
        .gauge-card {{ background: #0E0E0E; border: 1px solid #1A1A1A; border-radius: 15px; padding: 15px; text-align: center; }}
        .gauge-title {{ font-size: 9px; color: #888; letter-spacing: 1px; font-weight: bold; margin-bottom: 10px; text-transform: uppercase; }}
        .gauge-sub {{ font-size: 10px; color: #666; margin-top: 5px; font-weight: bold; }}
        
        /* MACRO BARS */
        .macro-box {{ margin-bottom: 15px; background: #0E0E0E; padding: 12px; border-radius: 10px; border: 1px solid #1A1A1A; }}
        .macro-top {{ display: flex; justify-content: space-between; font-size: 10px; margin-bottom: 8px; text-transform: uppercase; }}
        .macro-bg {{ height: 6px; background: #222; border-radius: 10px; overflow: hidden; }}
        .macro-fill {{ height: 100%; border-radius: 10px; }}
        
        .metric-mini-card {{ background: #0E0E0E; padding: 10px; border-radius: 10px; text-align: center; border: 1px solid #1A1A1A; }}
        .lbl {{ font-size: 8px; color: #888; text-transform: uppercase; font-weight: bold; }}
        .val-small {{ font-size: 18px; font-weight: bold; margin: 3px 0; }}
        
        .title-elite {{ font-size: 24px; font-weight: bold; color: {c_accent}; letter-spacing: 2px; border-bottom: 1px solid #222; padding-bottom: 10px; margin-bottom: 20px; }}
    </style>
    """
    logo_b64 = img_to_b64("logo_dorado.png" if gen != "f" else "logo_rosa.png")
    qr_b64 = img_to_b64("qr_code.png")
    
    html = f"""
    <html><head>{css}</head><body>
    <div class="page" style="text-align:center; padding-top:100px; background: #000;">
        <img src="data:image/png;base64,{logo_b64}" style="height:250px; margin-bottom:20px;">
        <div style="font-size:45px; font-weight:bold; color:{c_accent}; letter-spacing:5px;">PLAN INTEGRAL ELITE</div>
        <div style="margin:40px auto; width:70%; border-top:1px solid #333; border-bottom:1px solid #333; padding:40px 0;">
            <div class="lbl" style="font-size:14px; color:{c_accent};">ATLETA DE ÉLITE</div>
            <div style="font-size:50px; font-weight:bold; margin:10px 0;">{str(d.get('n','ATLETA')).upper()}</div>
            <div class="lbl" style="font-size:12px;">SOFTWARE ELITE V21.0</div>
        </div>
        <div style="position:absolute; bottom:50px; width:90%; left:5%;">
            <table style="width:100%;">
                <tr>
                    <td style="text-align:left;"><img src="data:image/png;base64,{qr_b64}" style="width:70px; border-radius:5px;"></td>
                    <td style="text-align:right; font-style:italic; color:#888; font-size:30px;">Eddy Personal Trainer</td>
                </tr>
            </table>
        </div>
    </div>

    <div class="page">
        <div class="title-elite">DASHBOARD DE ANALÍTICA</div>
        <table class="dashboard-grid">
            <tr>
                <td class="dashboard-td">{render_gauge_card("SCORE FÍSICO", "81", "Elite Score", 81, c_accent)}</td>
                <td class="dashboard-td">{render_gauge_card("METABOLISMO", "92", "Nivel Alto", 92, c_accent)}</td>
                <td class="dashboard-td">{render_gauge_card("GRASA", f"{d.get('rfm',0)}%", "RFM Estimado", d.get('rfm',0), c_accent)}</td>
                <td class="dashboard-td">{render_gauge_card("AGUA", f"{d.get('w',0)}L", "Hidratación", 100, "#00BFFF")}</td>
            </tr>
        </table>
        
        <table class="dashboard-grid">
            <tr>
                <td class="dashboard-td">{render_metric_box("EDAD", d.get('edad',0), "Años", c_accent)}</td>
                <td class="dashboard-td">{render_metric_box("PESO", d.get('peso',0), "Kilogramos", c_accent)}</td>
                <td class="dashboard-td">{render_metric_box("CINTURA", d.get('cintura',0), "Centímetros", c_accent)}</td>
                <td class="dashboard-td">{render_metric_box("ESTATURA", d.get('estatura',0), "Centímetros", c_accent)}</td>
            </tr>
        </table>

        <div style="background:#0E0E0E; padding:20px; border-radius:15px; border:1px solid #1A1A1A; text-align:center;">
            <div class="lbl">PROYECCIÓN DE EVOLUCIÓN CORPORAL</div>
            <img src="data:image/png;base64,{grafico_b64}" style="width:100%; border-radius:10px; margin-top:15px;">
        </div>
    </div>
    """
    html += f"""
    <div class="page">
        <div class="title-elite">INGENIERÍA NUTRICIONAL</div>
        <div style="margin-bottom:25px;">
            {render_macro_bar("Proteínas", d.get('p',0), 100, c_accent)}
            {render_macro_bar("Carbohidratos", d.get('c',0), 80, "#4CAF50")}
            {render_macro_bar("Grasas Saludables", d.get('g',0), 60, "#FFC107")}
        </div>
    """
    
    # Comidas con estilo visual limpio
    for comida, opciones in d.get('m', {}).items():
        html += f"""
        <div style="background:#0E0E0E; border-left:4px solid {c_accent}; padding:15px; margin-bottom:12px; border-radius:0 10px 10px 0;">
            <div style="font-weight:bold; color:{c_accent}; font-size:14px; margin-bottom:5px;">{comida.upper()}</div>
            <div style="font-size:11px; color:#AAA;">» {str(opciones[0]).strip() if opciones else ""}</div>
        </div>
        """

    html += """
        <div style="margin-top:50px; border-top:1px solid #222; padding-top:20px; text-align:center;">
            <div style="font-size:10px; color:#555; letter-spacing:5px;">SOFTWARE ELITE | BY EDDY PT</div>
        </div>
    </div></body></html>
    """

    return HTML(string=html).write_pdf()