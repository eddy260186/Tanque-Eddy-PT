# =========================================================
# 🔥 EDDY ULTRA ELITE PDF ENGINE v100 - OPTIMIZED FOR WEASYPRINT
# BLACK EBONY • GOLD • DIAMOND EDITION - INDESTRUCTIBLE
# =========================================================

from weasyprint import HTML
from io import BytesIO
from datetime import datetime
import base64
import os

# =========================================================
# HELPERS
# =========================================================

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

# =========================================================
# PDF ENGINE
# =========================================================

def build_pdf_ultra_elite(data, grafico_b64="", genero="m"):

    # =====================================================
    # THEME SYSTEM (DYNAMIC GENERO)
    # =====================================================
    if genero == "f":
        ACCENT = "#FF2D75"  # Neon Magenta Elite
        GLOW = "rgba(255,45,117,0.18)"
    else:
        ACCENT = "#D4AF37"  # Gold Premium
        GLOW = "rgba(212,175,55,0.18)"

    WHITE = "#FFFFFF"
    BLACK = "#050505"
    CARD = "#121212"  # Negro Obsidiana Sólido para máxima compatibilidad
    BORDER = "rgba(255,255,255,0.08)"
    CYAN = "#00D9FF"

    # =====================================================
    # LOGOS & GRAPHICS
    # =====================================================
    logo_path = "logo_tanque.png"
    logo_b64 = img_to_b64(logo_path)
    qr_b64 = img_to_b64("qr_code.png")

    # =====================================================
    # DATA EXTRACTION
    # =====================================================
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
    # HTML MASTER TEMPLATE
    # =====================================================
    html = f"""
    <html>
    <head>
    <meta charset="UTF-8">
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
        font-family: 'Segoe UI', Arial, sans-serif;
    }}
    /* Contenedores de Página Estrictos */
    .page {{
        width: 210mm;
        min-height: 297mm;
        position: relative;
        page-break-after: always;
        background: radial-gradient(circle at top left, {GLOW}, transparent 45%), {BLACK};
    }}
    /* Páginas de contenido fluido (evita el colapso de datos largos) */
    .fluid-page {{
        width: 210mm;
        position: relative;
        page-break-inside: auto;
        background: radial-gradient(circle at bottom right, rgba(0,217,255,0.04), transparent 40%), {BLACK};
    }}
    .overlay {{
        position: absolute;
        width: 700px;
        right: -120px;
        top: 120px;
        opacity: 0.02;
        z-index: 1;
    }}
    .content {{
        position: relative;
        z-index: 2;
        padding: 45px;
    }}
    /* Componentes Premium de Diseño */
    .hero-logo {{
        width: 240px;
        margin-bottom: 10px;
    }}
    .hero-title {{
        font-size: 52px;
        font-weight: 900;
        letter-spacing: 5px;
        margin-top: 15px;
        margin-bottom: 5px;
        color: {ACCENT};
        text-transform: uppercase;
    }}
    .hero-sub {{
        color: #888;
        letter-spacing: 4px;
        font-size: 11px;
        margin-top: 5px;
        font-weight: 700;
    }}
    .premium-card {{
        background: linear-gradient(145deg, #161616, #0e0e0e);
        border: 1px solid {BORDER};
        border-top: 3px solid {ACCENT};
        border-radius: 20px;
        padding: 24px;
        margin-bottom: 20px;
        page-break-inside: avoid; /* Impide que la tarjeta se parta a la mitad entre páginas */
    }}
    .section-title {{
        font-size: 26px;
        font-weight: 900;
        color: white;
        margin-top: 10px;
        margin-bottom: 25px;
        letter-spacing: 2px;
        text-transform: uppercase;
        border-left: 4px solid {ACCENT};
        padding-left: 12px;
    }}
    .label {{
        color: {ACCENT};
        font-size: 11px;
        letter-spacing: 2px;
        text-transform: uppercase;
        font-weight: 700;
    }}
    .value {{
        font-size: 28px;
        font-weight: 900;
        color: white;
        margin-top: 6px;
    }}
    /* Sistema de Barras de Macros Realistas */
    .macro-bar {{
        width: 100%;
        height: 12px;
        background: #1a1a1a;
        border-radius: 30px;
        overflow: hidden;
        margin-top: 8px;
    }}
    .macro-fill {{
        height: 100%;
        border-radius: 30px;
    }}
    .exercise {{
        padding: 12px 15px;
        border-left: 3px solid {ACCENT};
        background: rgba(255,255,255,0.02);
        margin-bottom: 8px;
        border-radius: 8px;
        font-size: 13px;
        color: #ddd;
    }}
    /* Footer Ultra-Compatible con WeasyPrint (Estructura de Tabla) */
    .footer-container {{
        position: absolute;
        bottom: 30px;
        left: 45px;
        right: 45px;
        height: 40px;
    }}
    .footer-table {{
        width: 100%;
        border-top: 1px solid rgba(255,255,255,0.08);
        padding-top: 12px;
    }}
    .footer-left {{
        text-align: left;
        color: #555;
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

    # PORTADA (PAGE 1)
    <div class="page">
        <img src="data:image/png;base64,{logo_b64}" class="overlay">
        
        <div class="content" style="text-align:center; padding-top:80px;">
            <img src="data:image/png;base64,{logo_b64}" class="hero-logo">
            <div class="hero-title">Elite System</div>
            <div class="hero-sub">INGENIERÍA CORPORAL DE ALTO RENDIMIENTO</div>

            <div class="premium-card" style="margin-top:50px; text-align: left;">
                <div class="label">ATLETA AUTORIZADO</div>
                <div class="value" style="font-size: 36px; color: white;">{nombre.upper()}</div>
                <div style="margin-top:5px; color:#aaa; letter-spacing:2px; font-size:12px; font-weight: bold;">
                    NIVEL {nivel.upper()}
                </div>

                <table style="width:100%; margin-top:30px; border-spacing: 12px; margin-left: -12px; margin-right: -12px;">
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

                <div style="margin-top:30px; text-align: center;">
                    <img src="data:image/png;base64,{qr_b64}" style="width:85px; background:white; padding:6px; border-radius:12px; border:2px solid {ACCENT};">
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

    # ANALÍTICA CORPORAL (PAGE 2)
    <div class="page">
        <div class="content">
            <div class="section-title">Analítica Corporal</div>

            <table style="width:100%; border-spacing:12px; margin-left: -12px; margin-right: -12px; margin-bottom: 10px;">
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
                <div class="value">{agua}L <span style="font-size:16px; color:#888;">Hidratación</span> | {rfm}% <span style="font-size:16px; color:#888;">RFM</span></div>
            </div>

            <div class="premium-card">
                <div class="label">EVOLUCIÓN PROYECTADA ALTA PRECISIÓN</div>
                <img src="data:image/png;base64,{grafico_b64}" style="width:100%; margin-top:15px; border-radius:12px; border:1px solid rgba(255,255,255,0.06);">
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

    # SISTEMA NUTRICIONAL (FLUID PAGE)
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

            <div style="margin-top: 25px; margin-bottom: 15px; font-weight: 800; letter-spacing: 1px; color: #aaa; font-size: 12px; text-transform: uppercase;">
                Distribución de Menús
            </div>
    """

    # Bloque de Menús dinámicos con prevención de desbordes
    for comida, opciones in menus.items():
        opcion = str(opciones[0]) if opciones else "Planificación Nutricional Elite Personalizada."
        html += f"""
            <div class="premium-card">
                <div class="label">{comida.upper()}</div>
                <div style="margin-top:12px; color:#ddd; line-height:1.7; font-size:13px;">
                    {opcion}
                </div>
            </div>
        """

    html += f"""
        </div>
    </div>

    # PLAN DE ENTRENAMIENTO (FLUID PAGE)
    <div class="fluid-page" style="padding-bottom: 60px;">
        <div class="content">
            <div class="section-title">Entrenamiento Elite</div>

            <div class="premium-card">
                <div class="label">SISTEMA DE ENTRENAMIENTO ASIGNADO</div>
                <div class="value" style="color: {WHITE};">{str(data.get("entreno","")).upper()}</div>
            </div>
    """

    # Bloque de Rutinas dinámicas con prevención de cortes extraños
    for dia, ejercicios in rutina.items():
        html += f"""
            <div class="premium-card">
                <div class="label" style="margin-bottom: 12px; font-size: 13px; color: {ACCENT};">{dia.upper()}</div>
        """
        for e in ejercicios:
            html += f"""
                <div class="exercise">{str(e)}</div>
            """
        html += "</div>"

    html += """
        </div>
    </body>
    </html>
    """

    # =====================================================
    # GENERAR COMPILACIÓN PDF VIA WEASYPRINT
    # =====================================================
    return HTML(string=html).write_pdf()