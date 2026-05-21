# =========================================================
# 🔥 EDDY ULTRA ELITE PDF ENGINE v100.7 - TOTAL GROCERY MASTER
# COMPRAS MENSUALES DETALLADAS (KG + CONSUMO LIBRE) • WEASYPRINT SAFE
# =========================================================

from weasyprint import HTML
from io import BytesIO
from datetime import datetime
import base64
import os
import re

def safe_int(v):
    try:
        return int(round(float(v)))
    except:
        return 0

def img_to_b64(path):
    if path and os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

def build_pdf_ultra_elite(data, grafico_b64="", genero="m"):

    # =====================================================
    # SISTEMA DINÁMICO DE TEMAS Y LOGOS POR GÉNERO
    # =====================================================
    if genero == "f":
        ACCENT = "#FF2D75"       # Magenta Neón Elite
        logo_path = "logo_rosa.png"
        footer_text = "EDICIÓN ELITE FEMENINA"
    else:
        ACCENT = "#D4AF37"       # Dorado VIP
        logo_path = "logo_dorado.png"
        footer_text = "EDICIÓN ELITE MASCULINA"

    if not os.path.exists(logo_path):
        logo_path = "logo_tanque.png"

    WHITE = "#FFFFFF"
    BLACK = "#050505"
    CARD = "#111111"
    BORDER = "rgba(255,255,255,0.15)"
    CYAN = "#00D9FF"

    logo_b64 = img_to_b64(logo_path)
    qr_b64 = img_to_b64("qr_code.png")

    # Extracción segura de variables
    nombre = data.get("n", "ATLETA")
    edad = safe_int(data.get("edad", 0))
    peso = safe_int(data.get("peso", 0))
    estatura = safe_int(data.get("estatura", 0))
    rfm = safe_int(data.get("rfm", 0))

    calorias = safe_int(data.get("k", 0))
    proteinas = safe_int(data.get("p", 0))
    carbos = safe_int(data.get("c", 0))
    grasas = safe_int(data.get("g", 0))

    objetivo = str(data.get("meta", "RECOMPOSICIÓN"))
    nivel = str(data.get("nivel", "INTERMEDIO"))
    agua = data.get("w", 3)

    menus = data.get("m", {})
    rutina = data.get("rutina", {})

    # =====================================================
    # MATEMÁTICA Y PORCENTAJES PARA GRÁFICO SVG PASTEL
    # =====================================================
    total_macros = proteinas + carbos + grasas
    if total_macros == 0: total_macros = 1
    
    pct_p = (proteinas / total_macros) * 100
    pct_c = (carbos / total_macros) * 100
    pct_g = (grasas / total_macros) * 100

    offset_p = 25
    offset_c = 25 - pct_p
    offset_g = 25 - pct_p - pct_c

    # =====================================================
    # 🧠 ALGORITMO DE EXTRACCIÓN TOTAL DE COMPRAS (TODO)
    # =====================================================
    compras_mensuales_gramos = {}
    articulos_consumo_libre = set()

    if isinstance(menus, dict):
        for opciones in menus.values():
            if opciones and isinstance(opciones, list):
                # Procesamos la opción principal para las métricas exactas
                texto_dia = str(opciones[0]).replace('\n', ' ')
                # Dividimos tanto por el símbolo "+" como por la barra "|" de las infusiones
                componentes = re.split(r'[\+|]', texto_dia)
                
                for comp in componentes:
                    comp = comp.strip()
                    # Limpieza exhaustiva de prefijos del sistema
                    comp = re.sub(r'(?i)^Opcion\s*\d+:\s*', '', comp)
                    comp = re.sub(r'(?i)^Infusion\s*:\s*', '', comp)
                    comp = re.sub(r'(?i)^Infusión\s*:\s*', '', comp)
                    comp = comp.strip()
                    
                    if not comp:
                        continue
                    
                    # 1. Verificar si el ingrediente tiene gramaje especificado
                    match = re.search(r'(\d+)\s*g', comp)
                    if match:
                        gramos_diarios = int(match.group(1))
                        # Extraemos el nombre limpio quitándole los gramos
                        nombre_item = re.sub(r'\d+\s*g\s*', '', comp).strip().capitalize()
                        if nombre_item:
                            compras_mensuales_gramos[nombre_item] = compras_mensuales_gramos.get(nombre_item, 0) + gramos_diarios
                    else:
                        # 2. Si no tiene gramos (ej: "Mate amargo", "Aceite de oliva"), va a consumo libre
                        nombre_libre = comp.capitalize()
                        if nombre_libre and len(nombre_libre) > 2:
                            articulos_consumo_libre.add(nombre_libre)

    # Consolidación final de la lista de compras combinada
    lista_compras_final = []
    
    # Añadimos los elementos calculados en KG
    for alimento, gramos_totales in compras_mensuales_gramos.items():
        total_mes = gramos_totales * 30
        if total_mes >= 1000:
            lista_compras_final.append(f"{alimento} ({total_mes/1000:.1f} KG)")
        else:
            lista_compras_final.append(f"{alimento} ({total_mes} Gramos)")
            
    # Añadimos las infusiones y artículos libres (evitando duplicar nombres)
    for articulo in articulos_consumo_libre:
        if articulo.lower() not in [k.lower() for k in compras_mensuales_gramos.keys()]:
            lista_compras_final.append(f"{articulo} (Cantidad al gusto / Mes)")
            
    lista_compras_final.sort()
    
    if not lista_compras_final:
        lista_compras_final = ["Proteínas Magras de Alta Calidad", "Carbohidratos Complejos", "Fuentes de Grasas Saludables"]

    # =====================================================
    # MAQUETADO HTML + CSS REFORZADO PARA WEASYPRINT
    # =====================================================
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="UTF-8">
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
    @page {{
        size: A4;
        margin: 0;
        background: {BLACK};
    }}
    * {{
        box-sizing: border-box;
    }}
    body {{
        margin: 0;
        padding: 0;
        background: {BLACK};
        color: white;
        font-family: 'Montserrat', sans-serif;
    }}
    .page {{
        width: 210mm;
        min-height: 297mm;
        position: relative;
        page-break-after: always;
        background: {BLACK};
    }}
    .fluid-page {{
        width: 210mm;
        position: relative;
        page-break-inside: auto;
        background: {BLACK};
    }}
    .content {{
        position: relative;
        z-index: 2;
        padding: 50px;
    }}
    .qr-corner {{
        position: absolute;
        top: 45px;
        right: 45px;
        width: 80px;
        background: white;
        padding: 6px;
        border-radius: 10px;
        border: 2px solid {ACCENT};
    }}
    .hero-logo {{
        width: 260px;
        margin-bottom: 15px;
    }}
    .hero-title {{
        font-size: 54px;
        font-weight: 900;
        letter-spacing: 4px;
        margin-top: 10px;
        margin-bottom: 0px;
        color: {ACCENT};
        text-transform: uppercase;
    }}
    .hero-sub {{
        color: #888;
        letter-spacing: 3px;
        font-size: 12px;
        margin-top: 5px;
        font-weight: 700;
    }}
    .premium-card {{
        background: {CARD};
        border: 1px solid {BORDER};
        border-top: 3px solid {ACCENT};
        border-radius: 12px;
        padding: 25px;
        margin-bottom: 25px;
        page-break-inside: avoid;
    }}
    .section-title {{
        font-size: 24px;
        font-weight: 900;
        color: white;
        margin-top: 10px;
        margin-bottom: 25px;
        letter-spacing: 1px;
        text-transform: uppercase;
        border-left: 4px solid {ACCENT};
        padding-left: 15px;
    }}
    .label {{
        color: {ACCENT};
        font-size: 11px;
        letter-spacing: 1px;
        text-transform: uppercase;
        font-weight: 700;
    }}
    .value {{
        font-size: 26px;
        font-weight: 900;
        color: white;
        margin-top: 5px;
    }}
    .macro-bar {{
        width: 100%;
        height: 10px;
        background: #222;
        border-radius: 10px;
        margin-top: 8px;
    }}
    .macro-fill {{
        height: 100%;
        border-radius: 10px;
    }}
    .exercise {{
        padding: 12px 15px;
        border-left: 3px solid {ACCENT};
        background: #1A1A1A;
        margin-bottom: 8px;
        border-radius: 6px;
        font-size: 13px;
        color: #eee;
        font-weight: bold;
    }}
    .contract-box {{
        border: 2px dashed {ACCENT};
        padding: 40px;
        text-align: center;
        border-radius: 15px;
        background: rgba(255,255,255,0.02);
        margin-top: 20px;
    }}
    .footer-container {{
        position: absolute;
        bottom: 30px;
        left: 50px;
        right: 50px;
        height: 40px;
    }}
    .footer-table {{
        width: 100%;
        border-top: 1px solid rgba(255,255,255,0.15);
        padding-top: 15px;
    }}
    .footer-left {{
        text-align: left;
        color: #666;
        font-size: 10px;
        font-weight: bold;
    }}
    .footer-right {{
        text-align: right;
        color: {ACCENT};
        font-size: 10px;
        font-weight: bold;
        text-transform: uppercase;
    }}
    .graphics-table {{
        width: 100%;
        border-collapse: collapse;
        margin-top: 15px;
    }}
    .graphics-table td {{
        padding: 0;
        vertical-align: middle;
    }}
    
    /* Estructura de tabla blindada para la checklist */
    .checklist-table {{
        width: 100%;
        border-collapse: collapse;
        background: rgba(255,255,255,0.03);
        border: 1px solid {BORDER};
        margin-bottom: 10px;
        border-radius: 8px;
    }}
    .checklist-td-box {{
        padding: 14px 0 14px 18px;
        width: 35px;
        vertical-align: middle;
    }}
    .checklist-td-text {{
        padding: 14px 18px 14px 0;
        vertical-align: middle;
        font-size: 14px;
        font-weight: bold;
        color: #ddd;
    }}
    .checkbox-indicator {{
        width: 16px;
        height: 16px;
        border: 2px solid {ACCENT};
        border-radius: 4px;
    }}
    </style>
    </head>
    <body>

    <div class="page">
        <img src="data:image/png;base64,{qr_b64}" class="qr-corner">
        
        <div class="content" style="text-align:center; padding-top:110px;">
            <img src="data:image/png;base64,{logo_b64}" class="hero-logo">
            <div class="hero-title">Elite System</div>
            <div class="hero-sub">INGENIERÍA CORPORAL DE ALTO RENDIMIENTO</div>

            <div class="premium-card" style="margin-top:60px; text-align: left;">
                <div class="label">ATLETA AUTORIZADO</div>
                <div class="value" style="font-size: 32px;">{nombre.upper()}</div>
                <div style="margin-top:5px; color:#aaa; letter-spacing:2px; font-size:12px; font-weight: bold;">
                    NIVEL {nivel.upper()}
                </div>

                <table style="width:100%; margin-top:35px; border-spacing: 15px; margin-left: -15px; margin-right: -15px;">
                    <tr>
                        <td class="premium-card" style="margin-bottom:0; width:50%;">
                            <div class="label">CALORÍAS</div>
                            <div class="value">{calorias} <span style="font-size:14px; color:{ACCENT};">KCAL</span></div>
                        </td>
                        <td class="premium-card" style="margin-bottom:0; width:50%;">
                            <div class="label">PROTEÍNAS</div>
                            <div class="value">{proteinas}G</div>
                        </td>
                    </tr>
                    <tr>
                        <td class="premium-card" style="margin-bottom:0; width:50%;">
                            <div class="label">CARBOS</div>
                            <div class="value">{carbos}G</div>
                        </td>
                        <td class="premium-card" style="margin-bottom:0; width:50%;">
                            <div class="label">GRASAS</div>
                            <div class="value">{grasas}G</div>
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="footer-container">
            <table class="footer-table">
                <tr>
                    <td class="footer-left">EDDY ELITE SYSTEM © {datetime.now().year}</td>
                    <td class="footer-right">{footer_text}</td>
                </tr>
            </table>
        </div>
    </div>

    <div class="page">
        <div class="content">
            <div class="section-title">Analítica Corporal</div>
            <table style="width:100%; border-spacing:15px; margin-left: -15px; margin-right: -15px; margin-bottom: 10px;">
                <tr>
                    <td class="premium-card" style="margin-bottom:0; text-align: center;">
                        <div class="label">EDAD</div>
                        <div class="value">{edad}</div>
                    </td>
                    <td class="premium-card" style="margin-bottom:0; text-align: center;">
                        <div class="label">ESTATURA</div>
                        <div class="value">{estatura} <span style="font-size:14px; color:#aaa;">CM</span></div>
                    </td>
                    <td class="premium-card" style="margin-bottom:0; text-align: center;">
                        <div class="label">PESO</div>
                        <div class="value">{peso} <span style="font-size:14px; color:#aaa;">KG</span></div>
                    </td>
                </tr>
            </table>

            <div class="premium-card">
                <div class="label">OBJETIVO PRINCIPAL</div>
                <div class="value">{objetivo.upper()}</div>
            </div>

            <div class="premium-card">
                <div class="label">AGUA / GRASA CORPORAL ESPERADA</div>
                <div class="value">{agua}L <span style="font-size:16px; color:#888;">Hidratación</span> &nbsp;|&nbsp; {rfm}% <span style="font-size:16px; color:#888;">RFM</span></div>
            </div>

            <div class="premium-card">
                <div class="label" style="margin-bottom: 15px;">MÉTRICAS COLECTIVAS DE RENDIMIENTO</div>
                <table class="graphics-table">
                    <tr>
                        <td style="width: 38%; text-align: center; border-right: 1px solid rgba(255,255,255,0.08); padding-right: 15px;">
                            <svg viewBox="0 0 42 42" style="width: 125px; height: 125px; margin: 0 auto; display: block;">
                                <circle cx="21" cy="21" r="15.915" fill="transparent" stroke="#222" stroke-width="5" />
                                <circle cx="21" cy="21" r="15.915" fill="transparent" stroke="{ACCENT}" stroke-width="5" stroke-dasharray="{pct_p} {100-pct_p}" stroke-dashoffset="{offset_p}" />
                                <circle cx="21" cy="21" r="15.915" fill="transparent" stroke="{CYAN}" stroke-width="5" stroke-dasharray="{pct_c} {100-pct_c}" stroke-dashoffset="{offset_c}" />
                                <circle cx="21" cy="21" r="15.915" fill="transparent" stroke="#FF9800" stroke-width="5" stroke-dasharray="{pct_g} {100-pct_g}" stroke-dashoffset="{offset_g}" />
                                <text x="21" y="20" fill="white" font-size="6" font-weight="900" text-anchor="middle">AI</text>
                                <text x="21" y="25" fill="{ACCENT}" font-size="3.5" font-weight="bold" text-anchor="middle">MACROS</text>
                            </svg>
                            <div style="margin-top: 15px; font-size: 11px; font-weight: bold; line-height: 1.5; text-align: center; color: #aaa; white-space: nowrap;">
                                <span style="color:{ACCENT};">■</span> {pct_p:.0f}% P &nbsp;&nbsp;&nbsp;&nbsp;
                                <span style="color:{CYAN};">■</span> {pct_c:.0f}% C &nbsp;&nbsp;&nbsp;&nbsp;
                                <span style="color:#FF9800;">■</span> {pct_g:.0f}% G
                            </div>
                        </td>
                        <td style="width: 62%; padding-left: 20px; text-align: center;">
                            <img src="data:image/png;base64,{grafico_b64}" style="width:100%; border-radius:6px;">
                        </td>
                    </tr>
                </table>
            </div>
        </div>
        <div class="footer-container">
            <table class="footer-table">
                <tr>
                    <td class="footer-left">EDDY ELITE SYSTEM</td>
                    <td class="footer-right">BIOMETRÍA</td>
                </tr>
            </table>
        </div>
    </div>

    <div class="fluid-page" style="page-break-after: always; padding-bottom: 60px;">
        <div class="content">
            <div class="section-title">Sistema Nutricional</div>
            <div class="premium-card">
                <div class="label">PROTEÍNAS DIARIAS</div>
                <div class="macro-bar"><div class="macro-fill" style="width:90%; background:{ACCENT};"></div></div>
                <div class="value">{proteinas}G</div>
                <br>
                <div class="label">CARBOHIDRATOS DIARIOS</div>
                <div class="macro-bar"><div class="macro-fill" style="width:75%; background:{CYAN};"></div></div>
                <div class="value">{carbos}G</div>
                <br>
                <div class="label">GRASAS SALUDABLES</div>
                <div class="macro-bar"><div class="macro-fill" style="width:55%; background:#FF9800;"></div></div>
                <div class="value">{grasas}G</div>
            </div>
            <div style="margin-top: 30px; margin-bottom: 20px; font-weight: 900; letter-spacing: 1px; color: #aaa; font-size: 14px; text-transform: uppercase;">
                Distribución de Menús Dinámicos
            </div>
    """

    for comida, opciones in menus.items():
        opcion = str(opciones[0]) if opciones else "Planificación Nutricional Elite Personalizada."
        html += f"""
            <div class="premium-card">
                <div class="label">{comida.upper()}</div>
                <div style="margin-top:12px; color:#ccc; line-height:1.8; font-size:14px; font-weight: bold;">
                    {opcion}
                </div>
            </div>
        """

    html += f"""
        </div>
    </div>

    <div class="fluid-page" style="page-break-after: always; padding-bottom: 60px;">
        <div class="content">
            <div class="section-title">Protocolo de Abastecimiento</div>
            <div style="margin-bottom: 25px; color: #888; font-size: 13px; letter-spacing: 1px; text-transform: uppercase; font-weight: bold;">
                Lista Completa y Detallada para el Mes Completo (30 Días)
            </div>
    """

    for item in lista_compras_final:
        html += f"""
            <table class="checklist-table">
                <tr>
                    <td class="checklist-td-box">
                        <div class="checkbox-indicator"></div>
                    </td>
                    <td class="checklist-td-text">
                        {item}
                    </td>
                </tr>
            </table>
        """

    html += f"""
        </div>
    </div>

    <div class="fluid-page" style="page-break-after: always; padding-bottom: 60px;">
        <div class="content">
            <div class="section-title">Entrenamiento Elite</div>
            <div class="premium-card">
                <div class="label">SISTEMA DE ENTRENAMIENTO ASIGNADO</div>
                <div class="value" style="color: {WHITE};">{str(data.get("entreno","")).upper()}</div>
            </div>
    """

    for dia, ejercicios in rutina.items():
        html += f"""
            <div class="premium-card">
                <div class="label" style="margin-bottom: 15px; font-size: 14px; color: {ACCENT};">{dia.upper()}</div>
        """
        for e in ejercicios:
            html += f"""
                <div class="exercise">{str(e)}</div>
            """
        html += "</div>"

    html += f"""
        </div>
    </div>

    <div class="page">
        <div class="content" style="padding-top: 80px;">
            <div class="section-title">Mentalidad Elite</div>
            
            <div class="contract-box">
                <h2 style="color:{ACCENT}; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 30px;">Contrato de Disciplina</h2>
                <p style="color:#ddd; font-size: 16px; line-height: 2; font-style: italic; margin-bottom: 50px;">
                    "Yo, <strong>{nombre.upper()}</strong>, me comprometo a seguir este protocolo con disciplina inquebrantable. Entiendo que los resultados excepcionales requieren un esfuerzo excepcional. No hay excusas, solo ejecución. Mi transformación física y mental empieza hoy."
                </p>
                
                <div style="border-bottom: 1px solid #555; width: 70%; margin: 0 auto;"></div>
                <div style="margin-top: 15px; color: #888; font-size: 12px; letter-spacing: 3px; font-weight: bold;">FIRMA DEL ATLETA</div>
                
                <div style="margin-top: 50px;">
                    <img src="data:image/png;base64,{logo_b64}" style="width: 120px; opacity: 0.3;">
                </div>
            </div>
        </div>
        <div class="footer-container">
            <table class="footer-table">
                <tr>
                    <td class="footer-left">EDDY ELITE SYSTEM</td>
                    <td class="footer-right">COMPROMISO</td>
                </tr>
            </table>
        </div>
    </div>

    </body>
    </html>
    """

    return HTML(string=html).write_pdf()