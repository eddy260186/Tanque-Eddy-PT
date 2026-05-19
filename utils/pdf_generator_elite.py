# =========================================================
# 🔥 EDDY ULTRA ELITE PDF ENGINE v100.2 - MASTER EDITION
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

    if genero == "f":
        ACCENT = "#FF2D75"
    else:
        ACCENT = "#D4AF37"

    WHITE = "#FFFFFF"
    BLACK = "#050505"
    CARD = "#111111"
    BORDER = "rgba(255,255,255,0.15)"
    CYAN = "#00D9FF"

    logo_path = "logo_tanque.png"
    logo_b64 = img_to_b64(logo_path)
    qr_b64 = img_to_b64("qr_code.png")

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
    # 🧠 SMART GROCERY LIST EXTRACTOR
    # Extrae automáticamente los ingredientes de los menús
    # =====================================================
    lista_compras = data.get("compras", [])
    if not lista_compras and isinstance(menus, dict):
        compras_set = set()
        for comidas in menus.values():
            if comidas and isinstance(comidas, list):
                texto = str(comidas[0])
                partes = texto.split('+')
                for p in partes:
                    p_clean = p.split('|')[0].strip()
                    p_clean = re.sub(r'(?i)Opcion\s*\d+:\s*', '', p_clean)
                    p_clean = re.sub(r'\d+\s*g\s*', '', p_clean).strip()
                    if p_clean and p_clean.lower() not in ["infusion", "infusión"]:
                        compras_set.add(p_clean.capitalize())
        lista_compras = sorted(list(compras_set))
        if not lista_compras:
            lista_compras = ["Proteínas Magras", "Carbohidratos Complejos", "Grasas Saludables", "Vegetales Verdes"]

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
    .hero-logo {{
        width: 260px;
        margin-bottom: 15px;
    }}
    .hero-title {{
        font-size: 58px;
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
    .checklist-item {{
        background: rgba(255,255,255,0.03);
        border: 1px solid {BORDER};
        padding: 14px 18px;
        margin-bottom: 10px;
        border-radius: 8px;
    }}
    .checkbox-box {{
        width: 18px;
        height: 18px;
        border: 2px solid {ACCENT};
        border-radius: 4px;
        display: inline-block;
        vertical-align: middle;
        margin-right: 15px;
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
    </style>
    </head>
    <body>

    <div class="page">
        <div class="content" style="text-align:center; padding-top:90px;">
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

                <div style="margin-top:35px; text-align: center;">
                    <img src="data:image/png;base64,{qr_b64}" style="width:90px; background:white; padding:8px; border-radius:10px; border:2px solid {ACCENT};">
                </div>
            </div>
        </div>
        <div class="footer-container">
            <table class="footer-table">
                <tr>
                    <td class="footer-left">EDDY ELITE SYSTEM © {datetime.now().year}</td>
                    <td class="footer-right">BLACK EBONY EDITION</td>
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
                <div class="label" style="margin-bottom: 15px;">EVOLUCIÓN PROYECTADA ALTA PRECISIÓN</div>
                <img src="data:image/png;base64,{grafico_b64}" style="width:100%; border-radius:8px; border:1px solid rgba(255,255,255,0.1);">
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
                Distribución de Menús
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
                Checklist de Compras Inteligente
            </div>
    """

    for item in lista_compras:
        html += f"""
            <div class="checklist-item">
                <div class="checkbox-box"></div>
                <span style="font-size:14px; font-weight:bold; color:#ddd;">{item}</span>
            </div>
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