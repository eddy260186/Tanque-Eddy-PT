import os
import base64
from weasyprint import HTML

# =========================================================
# EDDY PT ELITE - ENGINE V13.0 (ULTRA-PREMIUM GAUGES)
# =========================================================

def generate_gauge_svg(percent, color, label_value):
    """Genera un indicador circular en SVG blindado para WeasyPrint"""
    # Calculamos el perímetro del círculo (2 * PI * r) donde r=18
    # Circunferencia = 113
    circumference = 113
    offset = circumference - (percent / 100) * circumference
    
    return f'''
    <svg width="80" height="80" viewBox="0 0 40 40" style="margin: 0 auto; display: block;">
        <circle cx="20" cy="20" r="18" fill="transparent" stroke="#1A1A1A" stroke-width="3" />
        <circle cx="20" cy="20" r="18" fill="transparent" stroke="{color}" stroke-width="3" 
                stroke-dasharray="{circumference}" stroke-dashoffset="{offset}" 
                stroke-linecap="round" transform="rotate(-90 20 20)" />
        <text x="20" y="22" text-anchor="middle" font-family="Bebas Neue" font-size="9" fill="#FFFFFF">{label_value}</text>
    </svg>
    '''

def img_to_b64(path):
    try:
        if not path or not os.path.exists(path): return ""
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    except: return ""

def render_logo(path, class_name):
    b64 = img_to_b64(path)
    return f'<img src="data:image/png;base64,{b64}" class="{class_name}">' if b64 else ""
# =========================================================
# THEMES: CONFIGURACIÓN DE IDENTIDAD VISUAL
# =========================================================

THEMES = {
    "gold": {
        "bg": "#030303", "bg2": "#080808", "card": "#0E0E0E",
        "txt": "#F5F5F5", "soft": "#8C8C8C", "accent": "#D4AF37",
        "bright": "#FFD700", "dark": "rgba(212,175,55,0.22)",
        "edition": "BLACK GOLD ALPHA", "logo": "logo_dorado.png"
    },
    "ruby": {
        "bg": "#030303", "bg2": "#080808", "card": "#0E0E0E",
        "txt": "#F5F5F5", "soft": "#8C8C8C", "accent": "#C2185B",
        "bright": "#FF4D8D", "dark": "rgba(194,24,91,0.22)",
        "edition": "RUBY BLACK ELITE", "logo": "logo_rosa.png"
    }
}

def build_pdf_v60_7(d, grafico_b64="", ruta_img="", gen="m"):
    theme = THEMES["ruby"] if gen == "f" else THEMES["gold"]
    c_bg = theme["bg"]; c_acc = theme["accent"]; c_dark = theme["dark"]; c_soft = theme["soft"]

    css = f"""
    <style>
        @page {{ size: A4; margin: 0; background: {c_bg}; }}
        * {{ box-sizing: border-box; }}
        body {{ margin: 0; padding: 0; font-family: 'Montserrat', sans-serif; color: #FFF; line-height: 1.4; }}
        
        /* DISEÑO DE GAUGE GRID */
        .gauge-grid {{ 
            width: 100%; 
            display: table; 
            border-spacing: 10px; 
            margin-bottom: 20px; 
        }}
        .gauge-item {{ 
            display: table-cell; 
            background: linear-gradient(145deg, #111, #080808); 
            border: 1px solid rgba(255,255,255,0.05);
            border-radius: 15px; 
            padding: 15px 5px; 
            text-align: center; 
            vertical-align: middle;
        }}
        
        /* ESTILOS DE PORTADA V13 */
        .cover {{ height: 100vh; padding: 40px; text-align: center; background: radial-gradient(circle at center, {c_dark}, transparent 85%); }}
        .logo-main {{ height: 260px; margin-bottom: 10px; }}
        .cover-title {{ font-family: 'Bebas Neue'; font-size: 65px; letter-spacing: 5px; margin: 0; color: {c_acc}; }}
        .badge {{ margin: 15px auto; padding: 10px 30px; border-radius: 40px; border: 2px solid {c_acc}; font-weight: 700; letter-spacing: 3px; display: inline-block; }}
        
        .athlete-box {{ width: 85%; margin: 25px auto; padding: 25px 0; border-top: 1px solid #333; border-bottom: 1px solid #333; }}
        .athlete-name {{ font-family: 'Bebas Neue'; font-size: 52px; color: #FFF; margin: 5px 0; letter-spacing: 2px; }}
        
        /* INTERIORES */
        .page {{ padding: 45px; page-break-before: always; }}
        .header {{ border-bottom: 1px solid #333; padding-bottom: 15px; margin-bottom: 30px; display: flex; justify-content: space-between; align-items: end; }}
        .section-title {{ font-family: 'Bebas Neue'; font-size: 36px; color: {c_acc}; letter-spacing: 2px; }}
        
        .card-inner {{ background: #0E0E0E; border-radius: 15px; padding: 20px; border-top: 3px solid {c_acc}; }}
        .label-gauge {{ font-size: 9px; color: {c_soft}; letter-spacing: 1px; text-transform: uppercase; font-weight: 700; margin-top: 8px; }}
        
        .signature {{ font-family: 'Great Vibes'; font-size: 40px; color: #888; }}
        .qr {{ width: 75px; background: white; padding: 4px; border-radius: 8px; border: 1px solid {c_acc}; }}
    </style>
    """
    # =====================================================
    # PROCESAMIENTO DE LOGOS Y QR
    # =====================================================
    
    logo_path = theme["logo"] if os.path.exists(theme["logo"]) else ruta_img
    logo_m = render_logo(logo_path, "logo-main")
    logo_s = render_logo(logo_path, "logo-small")
    
    qr_path = "qr_code.png"
    qr_h = f'<img src="data:image/png;base64,{img_to_b64(qr_path)}" class="qr">' if os.path.exists(qr_path) else ""

    # =====================================================
    # INICIO DEL HTML Y CUERPO DE PORTADA
    # =====================================================

    html_content = f"""
    <html>
    <head>
    <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Montserrat:wght@300;400;500;700;900&family=Great+Vibes&display=swap" rel="stylesheet">
    {css}
    </head>
    <body>
    
    <div class="cover">
        <div style="margin-bottom: 10px;">
            {logo_m}
        </div>
        
        <div class="cover-title">PLAN INTEGRAL ELITE</div>
        <div style="color:{theme['soft']}; letter-spacing:4px; font-size:11px; margin-bottom: 20px;">
            HIGH PERFORMANCE PHYSIQUE ENGINEERING
        </div>
        
        <div class="badge">{theme['edition']}</div>
        
        <div class="athlete-box">
            <div class="label-gauge" style="color:{c_acc}; font-size:12px; margin-bottom:10px;">ATLETA DE ÉLITE</div>
            <div class="athlete-name">{str(d.get('n', 'ATLETA')).upper()}</div>
            <div class="label-gauge" style="margin-top:10px; font-size:10px;">
                NIVEL SELECCIONADO: <span style="color:#FFF;">{str(d.get('nivel', 'PRINCIPIANTE')).upper()}</span>
            </div>
        </div>

        <div style="margin-top: 50px; width: 100%; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 30px;">
            <table style="width: 100%; border-collapse: collapse;">
                <tr>
                    <td style="width: 30%; text-align: left; vertical-align: middle;">
                        {qr_h}
                    </td>
                    <td style="width: 40%; text-align: center; vertical-align: middle;">
                        <div class="label-gauge">SISTEMA DE GESTIÓN ELITE</div>
                        <div style="font-size: 11px; color: {theme['soft']}; margin-top: 5px;">
                            FECHA: {d.get('fecha', '10/05/2026')}
                        </div>
                    </td>
                    <td style="width: 30%; text-align: right; vertical-align: middle;">
                        <div class="signature" style="margin-bottom: -10px; color: #FFF;">Eddy</div>
                        <div class="label-gauge" style="font-size: 10px;">Personal Trainer</div>
                    </td>
                </tr>
            </table>
        </div>
    </div>
    """
    # =====================================================
    # PÁGINA 2: ANALÍTICA FÍSICA (TABLERO DE COMANDOS)
    # =====================================================
    
    # Calculamos algunos porcentajes visuales para los gauges
    # (Esto es solo para la animación visual del arco)
    p_grasa = float(d.get('rfm', 0))
    p_agua = 100 # El agua siempre se muestra como meta cumplida
    
    html_content += f"""
    <div class="page">
        <div class="header">
            <div class="section-title">ANALÍTICA FÍSICA</div>
            {logo_s}
        </div>

        <div class="gauge-grid">
            <div class="gauge-item">
                <div class="label-gauge">EDAD</div>
                {generate_gauge_svg(100, c_acc, d.get('edad', '0'))}
                <div class="label-gauge">AÑOS</div>
            </div>
            <div class="gauge-item">
                <div class="label-gauge">ESTATURA</div>
                {generate_gauge_svg(85, c_acc, f"{d.get('estatura', '0')}")}
                <div class="label-gauge">CM</div>
            </div>
            <div class="gauge-item">
                <div class="label-gauge">PESO</div>
                {generate_gauge_svg(75, c_acc, f"{d.get('peso', '0')}")}
                <div class="label-gauge">KG</div>
            </div>
            <div class="gauge-item">
                <div class="label-gauge">GRASA (RFM)</div>
                {generate_gauge_svg(p_grasa, c_acc, f"{p_grasa}%")}
                <div class="label-gauge" style="color:{c_acc};">ESTIMADA</div>
            </div>
        </div>

        <div class="gauge-grid">
            <div class="gauge-item">
                <div class="label-gauge">CINTURA</div>
                {generate_gauge_svg(60, c_acc, f"{d.get('cintura', '0')}")}
                <div class="label-gauge">CM</div>
            </div>
            <div class="gauge-item">
                <div class="label-gauge">CADERA</div>
                {generate_gauge_svg(60, c_acc, f"{d.get('cadera', '0')}")}
                <div class="label-gauge">CM</div>
            </div>
            <div class="gauge-item">
                <div class="label-gauge">ÍNDICE RCC</div>
                {generate_gauge_svg(50, c_acc, d.get('rcc', '0'))}
                <div class="label-gauge">RELACIÓN</div>
            </div>
            <div class="gauge-item" style="border-top: 2px solid #00BFFF;">
                <div class="label-gauge" style="color:#00BFFF;">HIDRATACIÓN</div>
                {generate_gauge_svg(p_agua, "#00BFFF", f"{d.get('w', '0')}L")}
                <div class="label-gauge">DIARIA</div>
            </div>
        </div>

        <div class="card-inner" style="text-align:center; margin-bottom: 25px;">
            <div class="label-gauge">OBJETIVO ESTRATÉGICO SELECCIONADO</div>
            <div class="value" style="font-size:42px; margin: 10px 0;">{str(d.get('meta','')).upper()}</div>
            <div class="label-gauge" style="color:{c_acc};">PROTOCOLO: {str(d.get('dt','')).upper()}</div>
        </div>

        <div class="card-inner">
            <div class="label-gauge">PROYECCIÓN DE EVOLUCIÓN CORPORAL</div>
            <div style="margin-top:15px; border-radius:10px; overflow:hidden;">
                <img src="data:image/png;base64,{grafico_b64}" class="graph">
            </div>
        </div>

        <div style="margin-top: 30px; display: flex; justify-content: space-between; align-items: end; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 15px;">
            {qr_h}
            <div class="signature">Eddy Personal Trainer</div>
        </div>
    </div>
    """
    # =====================================================
    # PÁGINA 3: ESTRATEGIA NUTRICIONAL
    # =====================================================
    html_content += f"""
    <div class="page">
        <div class="header">
            <div class="section-title">ESTRATEGIA NUTRICIONAL</div>
            {logo_s}
        </div>
        
        <div class="gauge-grid">
            <div class="gauge-item" style="width:33%;">
                <div class="label-gauge">KCAL DIARIAS</div>
                {generate_gauge_svg(100, c_acc, f"{d.get('k', 0):.0f}")}
            </div>
            <div class="gauge-item" style="width:33%;">
                <div class="label-gauge">PROTEÍNAS</div>
                {generate_gauge_svg(100, c_acc, f"{d.get('p', 0):.0f}G")}
            </div>
            <div class="gauge-item" style="width:33%;">
                <div class="label-gauge">CARBOS / GRASAS</div>
                <div class="value" style="font-size:22px; margin-top:20px;">
                    {d.get('c', 0):.0f}G / {d.get('g', 0):.0f}G
                </div>
            </div>
        </div>
    """

    # Bucle de Comidas
    for comida, opciones in d.get('m', {}).items():
        html_content += f"""
        <div class="card-inner" style="margin-bottom:15px; border-left:4px solid {c_acc}; border-top:none;">
            <div style="font-family:'Bebas Neue'; color:{c_acc}; font-size:22px; margin-bottom:8px;">{comida}</div>
        """
        for op in opciones:
            op_limpia = str(op).replace('\n', ' ').strip()
            html_content += f'<div style="font-size:11px; color:#CCC; padding:6px 0; border-bottom:1px solid #1A1A1A;">› {op_limpia}</div>'
        html_content += "</div>"

    html_content += f"""
        <div class="card-inner" style="border-top-color:#00BFFF; margin-top:20px;">
            <div class="label-gauge" style="color:#00BFFF;">SUPLEMENTACIÓN Y MICRONUTRIENTES</div>
            <div style="display: flex; flex-wrap: wrap; gap: 10px; margin-top:10px;">
    """
    for sup in d.get('s', []):
        sup_l = str(sup).replace('\n', ' ').strip()
        html_content += f'<span style="font-size:10px; background:#1A1A1A; padding:5px 12px; border-radius:20px; color:#00BFFF; border:1px solid #00BFFF33;">{sup_l}</span>'
    
    html_content += """</div></div></div>"""

    # =====================================================
    # PÁGINA 4: PLAN DE ENTRENAMIENTO
    # =====================================================
    html_content += f"""
    <div class="page">
        <div class="header">
            <div class="section-title">PLAN DE ENTRENAMIENTO</div>
            {logo_s}
        </div>
        <div class="card-inner" style="text-align:center; margin-bottom:25px; background:linear-gradient(to right, #0E0E0E, #151515);">
            <span class="label-gauge" style="margin-right:20px;">MODALIDAD: <span style="color:#FFF;">{str(d.get('entreno','')).upper()}</span></span>
            <span class="label-gauge">FRECUENCIA: <span style="color:#FFF;">{str(d.get('dias',''))} DÍAS/SEM</span></span>
        </div>
    """
    for dia, ejercicios in d.get('rutina', {}).items():
        html_content += f"""
        <div class="card-inner" style="margin-bottom:15px; border-left:4px solid {c_acc}; border-top:none;">
            <div style="font-family:'Bebas Neue'; color:{c_acc}; font-size:22px; margin-bottom:8px;">{dia}</div>
        """
        for ej in ejercicios:
            ej_l = str(ej).replace('\n', ' ').strip()
            html_content += f'<div style="font-size:11px; color:#CCC; padding:6px 0; border-bottom:1px solid #1A1A1A;">› {ej_l}</div>'
        html_content += "</div>"
    html_content += """</div>"""

    # =====================================================
    # PÁGINA 5: TICKET DE COMPRA
    # =====================================================
    html_content += f"""
    <div class="page">
        <div class="header">
            <div class="section-title">TICKET DE COMPRA MENSUAL</div>
            {logo_s}
        </div>
        <div class="card-inner" style="padding:0; overflow:hidden;">
            <table style="width:100%; border-collapse:collapse;">
    """
    for item, cant in d.get('compras', {}).items():
        it = str(item).replace('\n', '').strip()
        if "Huevo" in it or "Claras" in it:
            u = int(cant/50)
            res = f"<span style='color:{c_acc}; font-weight:bold;'>{u} Uni.</span>"
        elif any(x in it for x in ["Café", "Mate", "Té", "Infusión"]):
            res = f"<span style='color:{c_acc}; font-weight:bold;'>{int(cant)} Tazas</span>"
        else:
            res = f"<span style='color:{c_acc}; font-weight:bold;'>{round(cant/1000,2)} KG</span>" if cant>=1000 else f"<span style='color:{c_acc}; font-weight:bold;'>{int(cant)} g</span>"
        
        html_content += f'<tr><td style="padding:15px; border-bottom:1px solid #1A1A1A; font-size:12px;">{it}</td><td style="padding:15px; border-bottom:1px solid #1A1A1A; text-align:right; font-size:12px;">{res}</td></tr>'

    html_content += f"""
            </table>
        </div>
        <div style="margin-top:60px; text-align:center;">
            {qr_h}<br>
            <div class="signature" style="margin-top:15px;">Eddy Personal Trainer</div>
            <div class="label-gauge" style="letter-spacing:5px;">CERTIFIED ELITE SYSTEM</div>
        </div>
    </div>
    </body></html>
    """

    # RENDER FINAL
    try:
        return HTML(string=html_content).write_pdf()
    except Exception as e:
        print(f"FATAL ERROR: {e}")
        return b""