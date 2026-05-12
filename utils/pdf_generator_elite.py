"""
PDF GENERATOR ELITE v7.0 - Diseño Premium con WeasyPrint
Genera PDFs con diseño profesional: Negros, Dorados, Tipografía Elite
"""

from weasyprint import HTML, CSS
from io import BytesIO
import base64
from datetime import datetime

def build_pdf_elite_design(data, logo_path=None):
    """
    Genera un PDF ELITE con diseño premium idéntico a la foto del cliente.
    
    Parámetros:
    - data: diccionario con todos los datos del atleta
    - logo_path: ruta del logo (opcional)
    """
    
    # Extraer datos del diccionario
    nombre = data.get("n", "ATLETA ELITE")
    edad = data.get("edad", 25)
    estatura = data.get("estatura", 170)
    peso = data.get("peso", 75)
    cintura = data.get("cintura", 85)
    cadera = data.get("cadera", 95)
    rcc = data.get("rcc", 0.89)
    rfm = data.get("rfm", 15)
    masa_magra = data.get("masa_magra", 63)
    tmb = data.get("tmb", 1800)
    cal_obj = data.get("k", 2680)
    proteina = data.get("p", 198)
    carbos = data.get("c", 280)
    grasas = data.get("g", 72)
    agua = data.get("w", 3.5)
    tipo_objetivo = data.get("meta", "GANAS MASA MUSCULAR")
    nivel = data.get("nivel", "INTERMEDIO")
    frecuencia = data.get("dias", 5)
    tipo_dieta = data.get("dt", "ALTA EN PROTEÍNAS")
    tipo_entreno = data.get("entreno", "FUERZA / HIPERTROFIA")
    
    menus = data.get("m", {})
    rutina = data.get("rutina", {})
    suples = data.get("s", [])
    compras = data.get("compras", {})
    
    # ==========================================
    # PÁGINA 1: PORTADA + PERFIL
    # ==========================================
    html_pagina1 = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            @page {{
                size: A4;
                margin: 0;
            }}
            
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: #0a0a0a;
                color: #ffffff;
            }}
            
            .page {{
                width: 100%;
                height: 100vh;
                background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
                display: flex;
                page-break-after: always;
            }}
            
            /* ===== PORTADA ===== */
            .portada {{
                width: 50%;
                background: radial-gradient(circle at center, #2a2a2a 0%, #0a0a0a 100%);
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                padding: 40px;
                border-right: 3px solid #d4af37;
                position: relative;
                overflow: hidden;
            }}
            
            .portada::before {{
                content: '';
                position: absolute;
                top: -50%;
                right: -50%;
                width: 300px;
                height: 300px;
                background: radial-gradient(circle, #d4af37 0%, transparent 70%);
                opacity: 0.1;
                border-radius: 50%;
            }}
            
            .portada-content {{
                position: relative;
                z-index: 1;
                text-align: center;
            }}
            
            .logo-circle {{
                width: 200px;
                height: 200px;
                margin: 0 auto 30px;
                background: radial-gradient(circle at 30% 30%, #d4af37, #8b7620);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 80px;
                font-weight: bold;
                color: #000;
                box-shadow: 0 0 40px rgba(212, 175, 55, 0.4);
            }}
            
            .edicion {{
                font-size: 12px;
                color: #d4af37;
                letter-spacing: 2px;
                margin-bottom: 20px;
                text-transform: uppercase;
            }}
            
            .titulo-principal {{
                font-size: 42px;
                font-weight: bold;
                color: #d4af37;
                letter-spacing: 3px;
                margin: 20px 0;
                text-shadow: 0 0 10px rgba(212, 175, 55, 0.3);
            }}
            
            .subtitulo {{
                font-size: 28px;
                color: #ffffff;
                letter-spacing: 2px;
                margin: 10px 0;
            }}
            
            .descripcion {{
                font-size: 14px;
                color: #aaa;
                margin: 30px 0;
                letter-spacing: 1px;
            }}
            
            .atleta-name {{
                font-size: 32px;
                color: #ffffff;
                font-weight: bold;
                margin: 20px 0;
                text-transform: uppercase;
            }}
            
            .level {{
                font-size: 12px;
                color: #d4af37;
                letter-spacing: 1px;
            }}
            
            .metadata {{
                display: flex;
                justify-content: space-around;
                margin-top: 40px;
                padding-top: 30px;
                border-top: 1px solid #d4af37;
                width: 100%;
            }}
            
            .meta-item {{
                text-align: center;
                font-size: 11px;
                color: #aaa;
            }}
            
            .meta-item-icon {{
                font-size: 20px;
                margin-bottom: 8px;
            }}
            
            .meta-item-value {{
                color: #d4af37;
                font-size: 12px;
                font-weight: bold;
            }}
            
            /* ===== PERFIL ===== */
            .perfil {{
                width: 50%;
                padding: 40px;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
            }}
            
            .perfil-header {{
                color: #d4af37;
                font-size: 12px;
                letter-spacing: 2px;
                text-transform: uppercase;
                margin-bottom: 20px;
            }}
            
            .perfil-number {{
                font-size: 48px;
                font-weight: bold;
                color: #d4af37;
                margin-bottom: 10px;
            }}
            
            .perfil-title {{
                font-size: 20px;
                font-weight: bold;
                color: #ffffff;
                margin-bottom: 30px;
                letter-spacing: 1px;
            }}
            
            .biometria-grid {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 15px;
                margin-bottom: 40px;
            }}
            
            .bio-card {{
                background: rgba(212, 175, 55, 0.05);
                border-left: 3px solid #d4af37;
                padding: 12px 15px;
                border-radius: 2px;
            }}
            
            .bio-label {{
                font-size: 10px;
                color: #aaa;
                text-transform: uppercase;
                letter-spacing: 1px;
                margin-bottom: 5px;
            }}
            
            .bio-value {{
                font-size: 16px;
                font-weight: bold;
                color: #d4af37;
            }}
            
            .objetivos-grid {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 12px;
                margin-bottom: 30px;
            }}
            
            .objetivo-box {{
                background: rgba(212, 175, 55, 0.08);
                border: 1px solid #d4af37;
                padding: 12px;
                text-align: center;
                border-radius: 2px;
            }}
            
            .objetivo-label {{
                font-size: 9px;
                color: #aaa;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                margin-bottom: 5px;
            }}
            
            .objetivo-value {{
                font-size: 13px;
                color: #ffffff;
                font-weight: bold;
            }}
            
            .balance-section {{
                background: rgba(212, 175, 55, 0.08);
                border: 1px solid #d4af37;
                padding: 20px;
                border-radius: 2px;
            }}
            
            .balance-title {{
                font-size: 11px;
                color: #d4af37;
                text-transform: uppercase;
                letter-spacing: 1px;
                margin-bottom: 15px;
            }}
            
            .balance-grid {{
                display: grid;
                grid-template-columns: 1fr 1fr 1fr 1fr;
                gap: 15px;
            }}
            
            .balance-item {{
                text-align: center;
            }}
            
            .balance-icon {{
                font-size: 24px;
                margin-bottom: 5px;
            }}
            
            .balance-value {{
                font-size: 18px;
                font-weight: bold;
                color: #ffffff;
            }}
            
            .balance-label {{
                font-size: 9px;
                color: #aaa;
                text-transform: uppercase;
                margin-top: 3px;
            }}
            
            .water-section {{
                display: flex;
                align-items: center;
                margin-top: 15px;
                padding-top: 15px;
                border-top: 1px solid rgba(212, 175, 55, 0.3);
            }}
            
            .water-icon {{
                font-size: 32px;
                margin-right: 15px;
            }}
            
            .water-content {{
                flex: 1;
            }}
            
            .water-label {{
                font-size: 9px;
                color: #aaa;
                text-transform: uppercase;
            }}
            
            .water-value {{
                font-size: 24px;
                font-weight: bold;
                color: #d4af37;
            }}
            
            .footer-logo {{
                text-align: center;
                margin-top: 30px;
                font-size: 10px;
                color: #666;
                letter-spacing: 1px;
            }}
        </style>
    </head>
    <body>
        <div class="page">
            <!-- PORTADA IZQUIERDA -->
            <div class="portada">
                <div class="portada-content">
                    <div class="edicion">✦ EDICIÓN ELITE GOLD ✦</div>
                    <div class="logo-circle">💪</div>
                    <div class="titulo-principal">EDDY</div>
                    <div class="subtitulo">PERSONAL TRAINER</div>
                    <div class="descripcion">PLAN ELITE INTEGRAL<br>HIGH PERFORMANCE PHYSIQUE</div>
                    <div class="atleta-name">{nombre.upper()}</div>
                    <div class="level">ATLETA NIVEL: ELITE</div>
                    <div class="metadata">
                        <div class="meta-item">
                            <div class="meta-item-icon">📅</div>
                            <div>FECHA</div>
                            <div class="meta-item-value">{datetime.now().strftime('%d %b %Y')}</div>
                        </div>
                        <div class="meta-item">
                            <div class="meta-item-icon">⚙️</div>
                            <div>VERSIÓN</div>
                            <div class="meta-item-value">v60.7</div>
                        </div>
                        <div class="meta-item">
                            <div class="meta-item-icon">👨‍🏫</div>
                            <div>COACH</div>
                            <div class="meta-item-value">EDDY PT</div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- PERFIL DERECHA -->
            <div class="perfil">
                <div>
                    <div class="perfil-header">01 /// Perfil y Resumen</div>
                    <div class="perfil-number">01</div>
                    <div class="perfil-title">Perfil Físico</div>
                    
                    <div class="biometria-grid">
                        <div class="bio-card">
                            <div class="bio-label">Edad</div>
                            <div class="bio-value">{edad} años</div>
                        </div>
                        <div class="bio-card">
                            <div class="bio-label">Estatura</div>
                            <div class="bio-value">{estatura} cm</div>
                        </div>
                        <div class="bio-card">
                            <div class="bio-label">Peso Actual</div>
                            <div class="bio-value">{peso} kg</div>
                        </div>
                        <div class="bio-card">
                            <div class="bio-label">Cintura</div>
                            <div class="bio-value">{cintura} cm</div>
                        </div>
                        <div class="bio-card">
                            <div class="bio-label">Cadera</div>
                            <div class="bio-value">{cadera} cm</div>
                        </div>
                        <div class="bio-card">
                            <div class="bio-label">Índice RCC</div>
                            <div class="bio-value">{rcc:.2f}</div>
                        </div>
                        <div class="bio-card">
                            <div class="bio-label">Grasa Estimada</div>
                            <div class="bio-value">{rfm:.1f} %</div>
                        </div>
                        <div class="bio-card">
                            <div class="bio-label">Masa Magra</div>
                            <div class="bio-value">{masa_magra:.1f} kg</div>
                        </div>
                    </div>
                    
                    <div class="objetivos-grid">
                        <div class="objetivo-box">
                            <div class="objetivo-label">Objetivo Principal</div>
                            <div class="objetivo-value">{tipo_objetivo}</div>
                        </div>
                        <div class="objetivo-box">
                            <div class="objetivo-label">Nivel</div>
                            <div class="objetivo-value">{nivel}</div>
                        </div>
                        <div class="objetivo-box">
                            <div class="objetivo-label">Frecuencia</div>
                            <div class="objetivo-value">{frecuencia} días / SEMANA</div>
                        </div>
                        <div class="objetivo-box">
                            <div class="objetivo-label">Estilo de Dieta</div>
                            <div class="objetivo-value">{tipo_dieta}</div>
                        </div>
                    </div>
                </div>
                
                <div class="balance-section">
                    <div class="balance-title">Balance Nutricional Diario</div>
                    <div class="balance-grid">
                        <div class="balance-item">
                            <div class="balance-icon">🔥</div>
                            <div class="balance-value">{int(cal_obj)}</div>
                            <div class="balance-label">Calorías</div>
                        </div>
                        <div class="balance-item">
                            <div class="balance-icon">🥩</div>
                            <div class="balance-value">{int(proteina)}g</div>
                            <div class="balance-label">Proteínas</div>
                        </div>
                        <div class="balance-item">
                            <div class="balance-icon">🍞</div>
                            <div class="balance-value">{int(carbos)}g</div>
                            <div class="balance-label">Carbohidratos</div>
                        </div>
                        <div class="balance-item">
                            <div class="balance-icon">🧈</div>
                            <div class="balance-value">{int(grasas)}g</div>
                            <div class="balance-label">Grasas</div>
                        </div>
                    </div>
                    
                    <div class="water-section">
                        <div class="water-icon">💧</div>
                        <div class="water-content">
                            <div class="water-label">Objetivo de Hidratación Diaria</div>
                            <div class="water-value">{agua} LITROS</div>
                        </div>
                    </div>
                </div>
                
                <div class="footer-logo">EDDY PERSONAL TRAINER</div>
            </div>
        </div>
    </body>
    </html>
    """
    
    # ==========================================
    # PÁGINA 2: NUTRICIÓN INTELIGENTE (100% DINÁMICA)
    # ==========================================
    
    # 1. Calculamos los porcentajes reales para el PDF
    total_macros = proteina + carbos + grasas
    pct_p = int((proteina / total_macros) * 100) if total_macros > 0 else 0
    pct_c = int((carbos / total_macros) * 100) if total_macros > 0 else 0
    pct_g = int((grasas / total_macros) * 100) if total_macros > 0 else 0
    
    # 2. Armamos el código HTML de los menús leyendo tu variable 'menus'
    html_menus_dinamicos = ""
    if menus:
        for comida, opciones in menus.items():
            # Agarramos la primera opción generada para el resumen del PDF
            texto_opcion = str(opciones[0] if isinstance(opciones, list) and opciones else "Sin datos")
            texto_limpio = texto_opcion.replace("Opcion 1: ", "")
            
            html_menus_dinamicos += f'''
                    <li class="menu-item">
                        <div class="menu-meal">🍽️ {comida.upper()}</div>
                        {texto_limpio}
                    </li>'''
    else:
        html_menus_dinamicos = '''
                    <li class="menu-item">
                        <div class="menu-meal">⚠️ AVISO</div>
                        No se generó un menú para este perfil.
                    </li>'''

    html_pagina2 = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            @page {{
                size: A4;
                margin: 0;
            }}
            
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: #0a0a0a;
                color: #ffffff;
            }}
            
            .page {{
                width: 100%;
                height: 100vh;
                background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
                padding: 40px;
                page-break-after: always;
            }}
            
            .page-header {{
                display: flex;
                align-items: center;
                margin-bottom: 30px;
                border-bottom: 2px solid #d4af37;
                padding-bottom: 20px;
            }}
            
            .page-number {{
                font-size: 48px;
                font-weight: bold;
                color: #d4af37;
                margin-right: 20px;
            }}
            
            .page-title {{
                font-size: 18px;
                font-weight: bold;
                color: #ffffff;
                text-transform: uppercase;
                letter-spacing: 2px;
                flex: 1;
            }}
            
            .page-brand {{
                font-size: 10px;
                color: #d4af37;
                text-align: right;
            }}
            
            .content-grid {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 40px;
            }}
            
            .section {{
                background: rgba(212, 175, 55, 0.08);
                border: 1px solid #d4af37;
                padding: 25px;
                border-radius: 2px;
            }}
            
            .section-title {{
                font-size: 13px;
                font-weight: bold;
                color: #d4af37;
                text-transform: uppercase;
                letter-spacing: 1px;
                margin-bottom: 20px;
                padding-bottom: 10px;
                border-bottom: 1px solid #d4af37;
            }}
            
            .macro-item {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 15px;
                padding: 10px;
                background: rgba(255, 255, 255, 0.02);
                border-radius: 2px;
            }}
            
            .macro-label {{
                font-size: 12px;
                color: #ffffff;
            }}
            
            .macro-value {{
                font-size: 14px;
                font-weight: bold;
                color: #d4af37;
            }}
            
            .menu-list {{
                list-style: none;
            }}
            
            .menu-item {{
                margin-bottom: 12px;
                padding: 12px;
                background: rgba(255, 255, 255, 0.02);
                border-left: 2px solid #d4af37;
                font-size: 11px;
                line-height: 1.5;
            }}
            
            .menu-meal {{
                font-weight: bold;
                color: #d4af37;
                margin-bottom: 5px;
            }}
            
            .footer {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-top: 40px;
                padding-top: 20px;
                border-top: 1px solid #d4af37;
                font-size: 10px;
                color: #666;
            }}
            
            .footer-logo {{
                color: #d4af37;
            }}
        </style>
    </head>
    <body>
        <div class="page">
            <div class="page-header">
                <div class="page-number">02</div>
                <div class="page-title">/// Nutrición Inteligente</div>
                <div class="page-brand">EDDY PT</div>
            </div>
            
            <div class="content-grid">
                <div class="section">
                    <div class="section-title">Distribución de Macros</div>
                    <div class="macro-item">
                        <div class="macro-label">Proteínas</div>
                        <div class="macro-value">{int(proteina)}g ({pct_p}%)</div>
                    </div>
                    <div class="macro-item">
                        <div class="macro-label">Carbohidratos</div>
                        <div class="macro-value">{int(carbos)}g ({pct_c}%)</div>
                    </div>
                    <div class="macro-item">
                        <div class="macro-label">Grasas</div>
                        <div class="macro-value">{int(grasas)}g ({pct_g}%)</div>
                    </div>
                </div>
                
                <div class="section">
                    <div class="section-title">Distribución Calórica</div>
                    <div class="macro-item">
                        <div class="macro-label">Desayuno</div>
                        <div class="macro-value">{int(cal_obj * 0.20)} kcal</div>
                    </div>
                    <div class="macro-item">
                        <div class="macro-label">Almuerzo</div>
                        <div class="macro-value">{int(cal_obj * 0.35)} kcal</div>
                    </div>
                    <div class="macro-item">
                        <div class="macro-label">Merienda</div>
                        <div class="macro-value">{int(cal_obj * 0.15)} kcal</div>
                    </div>
                    <div class="macro-item">
                        <div class="macro-label">Cena</div>
                        <div class="macro-value">{int(cal_obj * 0.30)} kcal</div>
                    </div>
                </div>
            </div>
            
            <div class="section" style="margin-top: 40px;">
                <div class="section-title">Menú Asignado del Día</div>
                <div class="menu-list">
{html_menus_dinamicos}
                </div>
            </div>
            
            <div class="footer">
                <span class="footer-logo">© EDDY PERSONAL TRAINER</span>
                <span>Página 02</span>
            </div>
        </div>
    </body>
    </html>
    """
    
    # ==========================================
    # PÁGINA 3: ENTRENAMIENTO ELITE
    # ==========================================
    html_pagina3 = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            @page {{
                size: A4;
                margin: 0;
            }}
            
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: #0a0a0a;
                color: #ffffff;
            }}
            
            .page {{
                width: 100%;
                height: 100vh;
                background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
                padding: 40px;
                page-break-after: always;
            }}
            
            .page-header {{
                display: flex;
                align-items: center;
                margin-bottom: 30px;
                border-bottom: 2px solid #d4af37;
                padding-bottom: 20px;
            }}
            
            .page-number {{
                font-size: 48px;
                font-weight: bold;
                color: #d4af37;
                margin-right: 20px;
            }}
            
            .page-title {{
                font-size: 18px;
                font-weight: bold;
                color: #ffffff;
                text-transform: uppercase;
                letter-spacing: 2px;
                flex: 1;
            }}
            
            .page-brand {{
                font-size: 10px;
                color: #d4af37;
                text-align: right;
            }}
            
            .workout-grid {{
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 20px;
                margin-bottom: 30px;
            }}
            
            .workout-day {{
                background: rgba(212, 175, 55, 0.08);
                border: 1px solid #d4af37;
                padding: 20px;
                text-align: center;
                border-radius: 2px;
            }}
            
            .day-icon {{
                font-size: 32px;
                margin-bottom: 10px;
            }}
            
            .day-label {{
                font-size: 10px;
                color: #aaa;
                text-transform: uppercase;
                letter-spacing: 1px;
                margin-bottom: 8px;
            }}
            
            .day-title {{
                font-size: 13px;
                font-weight: bold;
                color: #ffffff;
            }}
            
            .exercises-section {{
                background: rgba(212, 175, 55, 0.08);
                border: 1px solid #d4af37;
                padding: 25px;
                border-radius: 2px;
            }}
            
            .exercises-title {{
                font-size: 13px;
                font-weight: bold;
                color: #d4af37;
                text-transform: uppercase;
                letter-spacing: 1px;
                margin-bottom: 20px;
                padding-bottom: 10px;
                border-bottom: 1px solid #d4af37;
            }}
            
            .exercise-item {{
                display: grid;
                grid-template-columns: auto 1fr auto auto auto;
                gap: 15px;
                margin-bottom: 12px;
                padding: 12px;
                background: rgba(255, 255, 255, 0.02);
                border-left: 2px solid #d4af37;
                align-items: center;
            }}
            
            .exercise-name {{
                font-size: 11px;
                font-weight: bold;
                color: #ffffff;
            }}
            
            .exercise-meta {{
                font-size: 9px;
                color: #aaa;
            }}
            
            .footer {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-top: 40px;
                padding-top: 20px;
                border-top: 1px solid #d4af37;
                font-size: 10px;
                color: #666;
            }}
            
            .footer-logo {{
                color: #d4af37;
            }}
        </style>
    </head>
    <body>
        <div class="page">
            <div class="page-header">
                <div class="page-number">03</div>
                <div class="page-title">/// Entrenamiento Elite</div>
                <div class="page-brand">EDDY PT</div>
            </div>
            
            <div class="workout-grid">
                <div class="workout-day">
                    <div class="day-icon">💪</div>
                    <div class="day-label">DÍA 1</div>
                    <div class="day-title">PUSH</div>
                </div>
                <div class="workout-day">
                    <div class="day-icon">🦵</div>
                    <div class="day-label">DÍA 2</div>
                    <div class="day-title">PULL</div>
                </div>
                <div class="workout-day">
                    <div class="day-icon">🏃</div>
                    <div class="day-label">DÍA 3</div>
                    <div class="day-title">LEGS</div>
                </div>
                <div class="workout-day">
                    <div class="day-icon">💪</div>
                    <div class="day-label">DÍA 4</div>
                    <div class="day-title">UPPER</div>
                </div>
                <div class="workout-day">
                    <div class="day-icon">🦵</div>
                    <div class="day-label">DÍA 5</div>
                    <div class="day-title">LOWER</div>
                </div>
                <div class="workout-day">
                    <div class="day-icon">🧘</div>
                    <div class="day-label">DÍA 6-7</div>
                    <div class="day-title">DESCANSO</div>
                </div>
            </div>
            
            <div class="exercises-section">
                <div class="exercises-title">Rutina Destacada - Día PUSH</div>
                <div class="exercise-item">
                    <div style="font-weight: bold; color: #d4af37;">1</div>
                    <div>
                        <div class="exercise-name">Press de Banca Plano</div>
                        <div class="exercise-meta">Pecho - Ejercicio Principal</div>
                    </div>
                    <div class="exercise-meta">4 series</div>
                    <div class="exercise-meta">6-12 reps</div>
                    <div class="exercise-meta">90s</div>
                </div>
                <div class="exercise-item">
                    <div style="font-weight: bold; color: #d4af37;">2</div>
                    <div>
                        <div class="exercise-name">Press Inclinado Mancuernas</div>
                        <div class="exercise-meta">Pecho - Variación</div>
                    </div>
                    <div class="exercise-meta">3 series</div>
                    <div class="exercise-meta">8-12 reps</div>
                    <div class="exercise-meta">90s</div>
                </div>
                <div class="exercise-item">
                    <div style="font-weight: bold; color: #d4af37;">3</div>
                    <div>
                        <div class="exercise-name">Aperturas en Peck Deck</div>
                        <div class="exercise-meta">Pecho - Aislamiento</div>
                    </div>
                    <div class="exercise-meta">3 series</div>
                    <div class="exercise-meta">13-15 reps</div>
                    <div class="exercise-meta">60s</div>
                </div>
            </div>
            
            <div class="footer">
                <span class="footer-logo">© EDDY PERSONAL TRAINER</span>
                <span>Página 03</span>
            </div>
        </div>
    </body>
    </html>
    """
    
    # ==========================================
    # CONVERTIR HTML A PDF
    # ==========================================
    
    try:
        # Página 1
        pdf1 = HTML(string=html_pagina1).write_pdf()
        
        # Página 2
        pdf2 = HTML(string=html_pagina2).write_pdf()
        
        # Página 3
        pdf3 = HTML(string=html_pagina3).write_pdf()
        
        # Combinar PDFs
        from PyPDF2 import PdfMerger
        merger = PdfMerger()
        
        merger.append(BytesIO(pdf1))
        merger.append(BytesIO(pdf2))
        merger.append(BytesIO(pdf3))
        
        output = BytesIO()
        merger.write(output)
        merger.close()
        output.seek(0)
        
        return output.getvalue()
        
    except Exception as e:
        # En vez de hacer un print silencioso y devolver None, lanzamos el error
        # para que app_nutricion.py lo atrape y te lo muestre en rojo en la pantalla.
        raise Exception(f"Falla interna al fusionar el PDF: {e}")