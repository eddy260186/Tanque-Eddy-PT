import os
import base64
from weasyprint import HTML

# =========================================================
# EDDY PT ELITE - 3D LUXURY ENGINE V27.0 (100% ESPAÑOL & PERFECTO)
# =========================================================

def safe_int(value):
    """Filtro de titanio: Sin decimales basuras."""
    try: return int(round(float(value)))
    except: return 0

def generate_gauge_svg(percent, color, label_value):
    """Gauge con efecto relieve 3D perfecto y centrado."""
    circumference = 251.2
    p = min(max(float(percent), 0), 100)
    offset = circumference - (p / 100) * circumference
    
    return f'''
    <div style="text-align: center; padding: 10px 0;">
        <svg width="85" height="85" viewBox="0 0 120 120" style="overflow: visible;">
            <circle cx="60" cy="60" r="40" stroke="#000" stroke-width="12" fill="none" style="filter: drop-shadow(4px 4px 5px rgba(0,0,0,0.8));" />
            <circle cx="60" cy="60" r="40" stroke="#151515" stroke-width="8" fill="none" />
            <circle cx="60" cy="60" r="40" stroke="{color}" stroke-width="8" fill="none"
                stroke-linecap="round" stroke-dasharray="{circumference}" 
                stroke-dashoffset="{offset}" transform="rotate(-90 60 60)" />
            <text x="50%" y="53%" dominant-baseline="middle" text-anchor="middle" 
                fill="#FFFFFF" font-size="26" font-weight="900" font-family="Arial">{label_value}</text>
        </svg>
    </div>
    '''

def img_to_b64(path):
    if path and os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return ""def render_macro_bar(icon, title, grams, percent, accent):
    """Barra de Macros 3D con Icono integrado en español."""
    p = min(max(float(percent), 0), 100)
    g_val = safe_int(grams)
    
    return f"""
    <div class="card-3d" style="padding: 15px; margin-bottom: 15px;">
        <table style="width: 100%;">
            <tr>
                <td style="width: 45px;"><div class="icon-3d" style="border-color: {accent}; color: {accent};">{icon}</div></td>
                <td style="text-align: left;"><span class="lbl-luxury" style="margin: 0; font-size:12px;">{title}</span></td>
                <td style="text-align: right;"><span class="val-3d" style="color: {accent}; font-size: 20px;">{g_val}g</span></td>
            </tr>
        </table>
        <div style="height: 10px; background: #000; border-radius: 10px; margin-top: 10px; box-shadow: inset 2px 2px 5px rgba(0,0,0,0.8);">
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
        /* MARGEN DE SEGURIDAD: 3.5cm arriba y abajo para el logo y la firma */
        @page {{ size: A4; margin: 35mm 15mm 35mm 15mm; background-color: #050505; }}
        body {{ font-family: 'Arial', sans-serif; color: #FFF; margin: 0; padding: 0; }}
        
        /* LOGO A LOS COSTADOS Y FIRMA: Se repite en CADA hoja automáticamente */
        .fixed-logo {{ position: fixed; top: -25mm; right: 0; width: 60px; height: 60px; text-align: right; }}
        .fixed-footer {{ position: fixed; bottom: -25mm; left: 0; right: 0; text-align: center; border-top: 1px solid #222; padding-top: 8mm; }}
        
        .footer-name {{ font-family: 'Arial', sans-serif; font-weight: 900; font-size: 16px; color: #666; font-style: italic; letter-spacing: 2px; }}
        .footer-title {{ font-size: 10px; color: {c_acc}; text-transform: uppercase; letter-spacing: 3px; font-weight: bold; margin-top: 3px; }}

        /* EFECTO 3D REALISTA PARA CARTAS E ICONOS */
        .card-3d {{
            background: linear-gradient(145deg, #111, #080808);
            border: 1px solid #1a1a1a;
            border-top: 2px solid {c_acc};
            border-radius: 15px;
            box-shadow: 5px 5px 15px rgba(0,0,0,0.8), -5px -5px 15px rgba(30,30,30,0.3);
            page-break-inside: avoid; /* NUNCA SE CORTA A LA MITAD */
        }}
        
        .icon-3d {{
            display: inline-block; width: 35px; height: 35px; line-height: 35px;
            text-align: center; border-radius: 50%;
            background: linear-gradient(145deg, #1a1a1a, #050505);
            border: 1px solid {c_acc}; font-size: 16px;
            box-shadow: 3px 3px 6px rgba(0,0,0,0.8), -3px -3px 6px rgba(30,30,30,0.5);
        }}

        .title-3d {{ font-size: 26px; font-weight: 900; color: #FFF; letter-spacing: 3px; border-bottom: 2px solid #111; padding-bottom: 10px; margin-bottom: 20px; text-transform: uppercase; margin-top: 20px; }}
        .lbl-luxury {{ font-size: 10px; color: #999; text-transform: uppercase; font-weight: bold; letter-spacing: 2px; }}
        .val-3d {{ font-size: 24px; font-weight: 900; color: #FFF; margin-top: 5px; }}

        .grid-table {{ width: 100%; border-collapse: separate; border-spacing: 12px; margin-left: -12px; margin-right: -12px; }}
        .grid-td {{ vertical-align: top; }}
    </style>
    """
    logo_b64 = img_to_b64(theme["logo"] if os.path.exists(theme["logo"]) else ruta_img)
    qr_b64 = img_to_b64("qr_code.png")
    
    html = f"""
    <html><head>{css}</head><body>
    
    <div class="fixed-logo">
        <img src="data:image/png;base64,{logo_b64}" style="width: 60px; filter: drop-shadow(0 5px 5px rgba(0,0,0,0.8));">
    </div>
    <div class="fixed-footer">
        <div class="footer-name">Eddy Personal Trainer</div>
        <div class="footer-title">DIRECTOR DE RENDIMIENTO ELITE</div>
    </div>

    <div style="text-align: center; margin-top: 20px; margin-bottom: 80px;">
        <img src="data:image/png;base64,{logo_b64}" style="height: 220px; margin-bottom: 20px; filter: drop-shadow(0 15px 25px rgba(0,0,0,0.9));">
        <div style="font-size: 55px; font-weight: 900; color: {c_acc}; letter-spacing: 8px; margin-bottom: 5px; text-transform: uppercase;">SISTEMA ÉLITE</div>
        <div style="color: #888; font-size: 14px; letter-spacing: 6px; font-weight: bold;">INGENIERÍA FÍSICA DE ALTO RENDIMIENTO</div>
        
        <div class="card-3d" style="margin: 60px auto; width: 85%; padding: 45px 0;">
            <div class="icon-3d" style="margin-bottom: 15px;">👑</div><br>
            <span class="lbl-luxury" style="color: {c_acc};">PERFIL DEL ATLETA AUTORIZADO</span>
            <div class="val-3d" style="font-size: 42px; margin: 15px 0; line-height: 1.1;">{str(d.get('n','ATLETA')).upper()}</div>
            <span class="lbl-luxury">NIVEL: {str(d.get('nivel','')).upper()}</span>
        </div>
        
        <div style="margin-top: 50px;">
            <img src="data:image/png;base64,{qr_b64}" style="width: 80px; border-radius: 10px; border: 2px solid {c_acc}; padding: 5px; background: #FFF; box-shadow: 0 10px 20px rgba(0,0,0,0.5);">
            <div class="lbl-luxury" style="margin-top: 15px; color:#666;">ESCANEAR PARA ACCESO DIGITAL</div>
        </div>
    </div>

    <div>
        <div class="title-3d">📊 TABLERO DE RENDIMIENTO</div>
        
        <table class="grid-table">
            <tr>
                <td class="grid-td"><div class="card-3d" style="padding: 15px; text-align: center;"><div class="lbl-luxury">EDAD</div>{generate_gauge_svg(100, c_acc, safe_int(d.get('edad',0)))}</div></td>
                <td class="grid-td"><div class="card-3d" style="padding: 15px; text-align: center;"><div class="lbl-luxury">ESTATURA</div>{generate_gauge_svg(85, c_acc, safe_int(d.get('estatura',0)))}</div></td>
                <td class="grid-td"><div class="card-3d" style="padding: 15px; text-align: center;"><div class="lbl-luxury">PESO (KG)</div>{generate_gauge_svg(75, c_acc, safe_int(d.get('peso',0)))}</div></td>
                <td class="grid-td"><div class="card-3d" style="padding: 15px; text-align: center;"><div class="lbl-luxury">GRASA %</div>{generate_gauge_svg(d.get('rfm',0), c_acc, f"{safe_int(d.get('rfm',0))}%")}</div></td>
            </tr>
        </table>

        <div class="card-3d" style="padding: 25px; margin-bottom: 20px; text-align: center;">
            <div class="icon-3d" style="margin-bottom: 10px;">🎯</div><br>
            <span class="lbl-luxury">OBJETIVO ESTRATÉGICO</span>
            <div class="val-3d" style="color: {c_acc}; font-size: 30px; letter-spacing: 2px;">{str(d.get('meta','')).upper()}</div>
        </div>

        <div class="card-3d" style="padding: 20px; text-align: center; margin-bottom: 40px;">
            <span class="lbl-luxury" style="margin-bottom: 15px; display: block;"><span class="icon-3d" style="width: 20px; height: 20px; line-height: 20px; font-size: 10px;">📈</span> EVOLUCIÓN PREDICTIVA</span>
            <img src="data:image/png;base64,{grafico_b64}" style="width: 100%; border-radius: 8px; border: 1px solid #222;">
        </div>
    </div>
    """
    html += f"""
    <div>
        <div class="title-3d">🍎 MATRIZ NUTRICIONAL</div>
        
        <div class="card-3d" style="padding: 20px; margin-bottom: 25px;">
            {render_macro_bar("🥩", "PROTEÍNAS", d.get('p',0), 100, c_acc)}
            {render_macro_bar("🍚", "CARBOHIDRATOS", d.get('c',0), 80, "#4CAF50")}
            {render_macro_bar("🥑", "GRASAS SALUDABLES", d.get('g',0), 60, "#FFC107")}
        </div>
    """
    
    for comida, opciones in d.get('m', {}).items():
        html += f"""
        <div class="card-3d" style="padding: 18px; margin-bottom: 15px; border-left: 5px solid {c_acc};">
            <div style="display: flex; align-items: center; margin-bottom: 8px;">
                <div class="icon-3d" style="margin-right: 12px; font-size: 14px; width: 28px; height: 28px; line-height: 28px;">🍽️</div>
                <div class="val-3d" style="font-size: 16px; color: {c_acc}; text-transform: uppercase; margin: 0;">{comida}</div>
            </div>
            <div style="font-size: 12px; color: #CCC; line-height: 1.5; padding-left: 40px;">{str(opciones[0]).strip() if opciones else ""}</div>
        </div>
        """

    html += f"""
    </div>
    
    <div style="margin-top: 40px;">
        <div class="title-3d">⚡ PROTOCOLO DE ENTRENAMIENTO</div>
        
        <table style="width: 100%; margin-bottom: 20px;">
            <tr>
                <td style="width: 50%; padding-right: 10px;">
                    <div class="card-3d" style="padding: 15px; text-align: center;">
                        <div class="icon-3d" style="margin-bottom: 5px;">🏋️</div><br><span class="lbl-luxury">MODALIDAD</span>
                        <div class="val-3d" style="font-size: 14px;">{str(d.get('entreno','')).upper()}</div>
                    </div>
                </td>
                <td style="width: 50%; padding-left: 10px;">
                    <div class="card-3d" style="padding: 15px; text-align: center;">
                        <div class="icon-3d" style="margin-bottom: 5px;">📅</div><br><span class="lbl-luxury">FRECUENCIA</span>
                        <div class="val-3d" style="font-size: 14px;">{str(d.get('dias',''))} DÍAS/SEM</div>
                    </div>
                </td>
            </tr>
        </table>
    """
    
    for dia, ejercicios in d.get('rutina', {}).items():
        html += f"""
        <div class="card-3d" style="padding: 18px; margin-bottom: 15px;">
            <div class="val-3d" style="font-size: 16px; color: {c_acc}; margin-bottom: 12px; border-bottom: 1px solid #222; padding-bottom: 8px;">{dia.upper()}</div>
        """
        for ej in ejercicios:
            html += f'<div style="font-size: 12px; color: #DDD; padding: 5px 0; border-bottom: 1px dashed #1a1a1a;"><span style="color:{c_acc}; margin-right:8px; font-weight:bold;">›</span> {str(ej).strip()}</div>'
        html += "</div>"

    html += f"""
    </div>

    <div style="margin-top: 40px;">
        <div class="title-3d">🛒 LISTA DE ABASTECIMIENTO</div>
        
        <div class="card-3d" style="padding: 20px;">
            <table style="width: 100%; border-collapse: collapse;">
    """
    
    for item, cant in d.get('compras', {}).items():
        it = str(item).replace('\n', '').strip()
        c_val = safe_int(cant)
        
        if "Huevo" in it or "Claras" in it: res = f"{safe_int(c_val/50)} Uni."
        elif any(x in it for x in ["Café", "Mate", "Té", "Infusión"]): res = f"{c_val} Tazas"
        else: res = f"{c_val/1000:.2f} KG" if c_val>=1000 else f"{c_val} g"
        
        html += f'<tr><td style="padding: 10px 0; border-bottom: 1px solid #1A1A1A; font-size: 12px; color: #EEE;">{it}</td><td style="padding: 10px 0; border-bottom: 1px solid #1A1A1A; text-align: right; font-size: 13px; font-weight: 900; color: {c_acc};">{res}</td></tr>'

    html += f"""
            </table>
        </div>
    </div>
    </body></html>
    """

    return HTML(string=html).write_pdf()