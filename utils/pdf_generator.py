import os
import base64
from weasyprint import HTML

# =========================================================
# EDDY PT ELITE - MOTOR V100 (LIMPIO, ELEGANTE, 100% ESPAÑOL)
# =========================================================

def safe_int(value):
    """Filtra decimales basuras. Deja números puros y enteros."""
    try: return int(round(float(value)))
    except: return 0

def img_to_b64(path):
    if path and os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return ""

def generate_gauge_svg(percent, color, label_value):
    """Gauges perfectos. Espaciados y limpios."""
    circumference = 251.2
    p = min(max(float(percent), 0), 100)
    offset = circumference - (p / 100) * circumference
    
    return f'''
    <div style="text-align: center; padding: 15px 0;">
        <svg width="90" height="90" viewBox="0 0 120 120" style="overflow: visible;">
            <circle cx="60" cy="60" r="40" stroke="#000" stroke-width="12" fill="none" />
            <circle cx="60" cy="60" r="40" stroke="#151515" stroke-width="8" fill="none" />
            <circle cx="60" cy="60" r="40" stroke="{color}" stroke-width="8" fill="none"
                stroke-linecap="round" stroke-dasharray="{circumference}" 
                stroke-dashoffset="{offset}" transform="rotate(-90 60 60)" />
            <text x="50%" y="53%" dominant-baseline="middle" text-anchor="middle" 
                fill="#FFFFFF" font-size="24" font-weight="900" font-family="Arial">{label_value}</text>
        </svg>
    </div>
    '''

def render_macro_bar(title, grams, percent, accent):
    """Barras de nutrición separadas para no amontonar."""
    p = min(max(float(percent), 0), 100)
    g_val = safe_int(grams)
    return f"""
    <div class="card-3d" style="padding: 18px; margin-bottom: 20px;">
        <table style="width: 100%; margin-bottom: 10px;">
            <tr>
                <td style="text-align: left;"><span class="lbl-luxury" style="font-size: 13px;">{title}</span></td>
                <td style="text-align: right;"><span class="val-3d" style="color: {accent}; font-size: 22px;">{g_val}g</span></td>
            </tr>
        </table>
        <div style="height: 10px; background: #000; border-radius: 10px;">
            <div style="height: 100%; width: {p}%; background: {accent}; border-radius: 10px;"></div>
        </div>
    </div>
    """

THEMES = {
    "gold": {"acc": "#D4AF37", "logo": "logo_dorado.png"},
    "ruby": {"acc": "#C2185B", "logo": "logo_rosa.png"}
}

def build_pdf_v60_7(d, grafico_b64="", ruta_img="", gen="m"):
    theme = THEMES["ruby"] if gen == "f" else THEMES["gold"]
    c_acc = theme["acc"]
    
    logo_b64 = img_to_b64(theme["logo"] if os.path.exists(theme["logo"]) else ruta_img)
    qr_b64 = img_to_b64("qr_code.png")

    css = f"""
    <style>
        /* MÁRGENES GIGANTES: Garantiza que nada se amontone arriba ni abajo */
        @page {{ size: A4; margin: 35mm 20mm 45mm 20mm; background-color: #050505; }}
        body {{ font-family: 'Arial', sans-serif; color: #FFF; margin: 0; padding: 0; line-height: 1.6; }}
        
        /* LOGO FIJO A LA DERECHA (Se repite sin chocar con el texto) */
        .header-fijo {{ position: fixed; top: -25mm; right: 0; width: 65px; }}
        
        /* FIRMA Y QR FIJOS ABAJO (Se repiten ordenados) */
        .footer-fijo {{ position: fixed; bottom: -35mm; left: 0; right: 0; border-top: 1px solid #222; padding-top: 15px; }}

        /* TARJETAS LIMPIAS: page-break-inside avoid evita que se partan a la mitad */
        .card-3d {{
            background: #0E0E0E;
            border: 1px solid #1a1a1a;
            border-left: 4px solid {c_acc};
            border-radius: 12px;
            page-break-inside: avoid;
            margin-bottom: 25px;
        }}
        
        /* TIPOGRAFÍA ORDENADA Y LEGIBLE */
        .title-3d {{ font-size: 24px; font-weight: 900; color: #FFF; letter-spacing: 3px; border-bottom: 2px solid #222; padding-bottom: 12px; margin-bottom: 30px; text-transform: uppercase; margin-top: 20px; }}
        .lbl-luxury {{ font-size: 11px; color: #999; text-transform: uppercase; font-weight: bold; letter-spacing: 2px; }}
        .val-3d {{ font-size: 26px; font-weight: 900; color: #FFF; margin-top: 8px; display: block; }}

        /* TABLA DE MÉTRICAS (Uso de tablas para alinear sin errores) */
        .grid-table {{ width: 100%; border-collapse: separate; border-spacing: 15px; margin-left: -15px; margin-right: -15px; }}
        .grid-td {{ vertical-align: top; width: 25%; background: #0E0E0E; border-top: 3px solid {c_acc}; border-radius: 12px; padding: 20px 10px; }}
    </style>
    """
    
    html = f"""
    <html><head>{css}</head><body>
    
    <div class="header-fijo">
        <img src="data:image/png;base64,{logo_b64}" style="width: 65px;">
    </div>
    
    <div class="footer-fijo">
        <table style="width: 100%;">
            <tr>
                <td style="text-align: left; vertical-align: middle; width: 50%;">
                    <img src="data:image/png;base64,{qr_b64}" style="width: 65px; border-radius: 8px; border: 1px solid {c_acc}; padding: 4px; background: #FFF;">
                    <div style="font-size: 9px; color: #888; font-weight: bold; margin-top: 5px; letter-spacing: 1px;">ESCANEAR ACCESO</div>
                </td>
                <td style="text-align: right; vertical-align: middle; width: 50%;">
                    <div style="font-family: Arial; font-weight: 900; font-style: italic; font-size: 32px; color: #555;">Eddy</div>
                    <div style="font-size: 10px; color: {c_acc}; font-weight: bold; letter-spacing: 2px; margin-top: 5px;">DIRECTOR DE RENDIMIENTO</div>
                </td>
            </tr>
        </table>
    </div>

    <div style="text-align: center; margin-bottom: 50px; padding-top: 30px;">
        <img src="data:image/png;base64,{logo_b64}" style="height: 190px; margin-bottom: 25px;">
        <div style="font-size: 50px; font-weight: 900; color: {c_acc}; letter-spacing: 6px; margin-bottom: 10px;">SISTEMA ÉLITE</div>
        <div style="color: #888; font-size: 13px; letter-spacing: 5px; font-weight: bold;">INGENIERÍA FÍSICA DE ALTO RENDIMIENTO</div>
        
        <div class="card-3d" style="margin: 60px auto; width: 90%; padding: 45px 0; border-left: none; border-top: 3px solid {c_acc};">
            <span class="lbl-luxury" style="color: {c_acc}; font-size: 13px;">PERFIL DEL ATLETA AUTORIZADO</span>
            <div class="val-3d" style="font-size: 42px; margin: 20px 0;">{str(d.get('n','ATLETA')).upper()}</div>
            <span class="lbl-luxury" style="font-size: 12px;">NIVEL: {str(d.get('nivel','')).upper()}</span>
        </div>
    </div>

    <div class="title-3d">TABLERO DE RENDIMIENTO</div>
    <table class="grid-table">
        <tr>
            <td class="grid-td" style="text-align: center;"><div class="lbl-luxury">EDAD</div>{generate_gauge_svg(100, c_acc, safe_int(d.get('edad',0)))}</td>
            <td class="grid-td" style="text-align: center;"><div class="lbl-luxury">ESTATURA</div>{generate_gauge_svg(85, c_acc, safe_int(d.get('estatura',0)))}</td>
            <td class="grid-td" style="text-align: center;"><div class="lbl-luxury">PESO (KG)</div>{generate_gauge_svg(75, c_acc, safe_int(d.get('peso',0)))}</td>
            <td class="grid-td" style="text-align: center;"><div class="lbl-luxury">GRASA %</div>{generate_gauge_svg(d.get('rfm',0), c_acc, f"{safe_int(d.get('rfm',0))}%")}</td>
        </tr>
    </table>

    <div class="card-3d" style="padding: 30px; text-align: center; border-left: none; border-top: 3px solid {c_acc};">
        <span class="lbl-luxury">OBJETIVO ESTRATÉGICO</span>
        <div class="val-3d" style="color: {c_acc}; font-size: 30px; letter-spacing: 2px;">{str(d.get('meta','')).upper()}</div>
    </div>

    <div class="card-3d" style="padding: 25px; text-align: center; border-left: none; border-top: 1px solid #222;">
        <span class="lbl-luxury" style="margin-bottom: 20px; display: block;">EVOLUCIÓN PREDICTIVA</span>
        <img src="data:image/png;base64,{grafico_b64}" style="width: 100%; border-radius: 8px;">
    </div>

    <div class="title-3d">MATRIZ NUTRICIONAL</div>
    <div style="margin-bottom: 35px;">
        {render_macro_bar("PROTEÍNAS", d.get('p',0), 100, c_acc)}
        {render_macro_bar("CARBOHIDRATOS", d.get('c',0), 80, "#4CAF50")}
        {render_macro_bar("GRASAS SALUDABLES", d.get('g',0), 60, "#FFC107")}
    </div>
    """
    
    for comida, opciones in d.get('m', {}).items():
        html += f"""
        <div class="card-3d" style="padding: 22px;">
            <div class="val-3d" style="font-size: 18px; color: {c_acc}; margin-top: 0; margin-bottom: 12px; text-transform: uppercase;">{comida}</div>
            <div style="font-size: 14px; color: #CCC; line-height: 1.8;">{str(opciones[0]).strip() if opciones else ""}</div>
        </div>
        """

    html += f"""
    <div style="margin-top: 45px;">
        <div class="title-3d">PROTOCOLO DE ENTRENAMIENTO</div>
        <table style="width: 100%; margin-bottom: 25px; border-spacing: 15px; margin-left: -15px;">
            <tr>
                <td style="width: 50%; background: #0E0E0E; border-top: 3px solid {c_acc}; border-radius: 12px; padding: 25px; text-align: center;">
                    <span class="lbl-luxury">MODALIDAD</span>
                    <div class="val-3d" style="font-size: 16px;">{str(d.get('entreno','')).upper()}</div>
                </td>
                <td style="width: 50%; background: #0E0E0E; border-top: 3px solid {c_acc}; border-radius: 12px; padding: 25px; text-align: center;">
                    <span class="lbl-luxury">FRECUENCIA</span>
                    <div class="val-3d" style="font-size: 16px;">{str(d.get('dias',''))} DÍAS/SEM</div>
                </td>
            </tr>
        </table>
    """
    
    for dia, ejercicios in d.get('rutina', {}).items():
        html += f"""
        <div class="card-3d" style="padding: 22px;">
            <div class="val-3d" style="font-size: 18px; color: {c_acc}; margin-top: 0; margin-bottom: 15px; border-bottom: 1px solid #222; padding-bottom: 12px;">{dia.upper()}</div>
        """
        for ej in ejercicios:
            html += f'<div style="font-size: 14px; color: #DDD; padding: 8px 0; border-bottom: 1px solid #1a1a1a;"><span style="color:{c_acc}; font-weight:bold; margin-right:10px; font-size: 16px;">•</span> {str(ej).strip()}</div>'
        html += "</div>"

    html += f"""
    </div>

    <div style="margin-top: 45px;">
        <div class="title-3d">LISTA DE ABASTECIMIENTO</div>
        <div class="card-3d" style="padding: 25px; border-left: none; border-top: 3px solid {c_acc};">
            <table style="width: 100%; border-collapse: collapse;">
    """
    
    for item, cant in d.get('compras', {}).items():
        it = str(item).replace('\n', '').strip()
        c_val = safe_int(cant)
        
        if "Huevo" in it or "Claras" in it: res = f"{safe_int(c_val/50)} Uni."
        elif any(x in it for x in ["Café", "Mate", "Té", "Infusión"]): res = f"{c_val} Tazas"
        else: res = f"{c_val/1000:.2f} KG" if c_val>=1000 else f"{c_val} g"
        
        html += f'<tr><td style="padding: 14px 0; border-bottom: 1px solid #1A1A1A; font-size: 14px; color: #EEE;">{it}</td><td style="padding: 14px 0; border-bottom: 1px solid #1A1A1A; text-align: right; font-size: 15px; font-weight: 900; color: {c_acc};">{res}</td></tr>'

    html += f"""
            </table>
        </div>
    </div>
    
    </body></html>
    """

    return HTML(string=html).write_pdf()