# =========================================================
# PDF GENERATOR ELITE v8.0 - DISEÑO PREMIUM + IA MACROS
# Motor Original (PyPDF2) + Logos Dinámicos + Compras Mensuales
# =========================================================

from weasyprint import HTML, CSS
from io import BytesIO
import base64
from datetime import datetime
from PyPDF2 import PdfMerger
import os
import re

def img_to_b64(path):
    if path and os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

def build_pdf_elite_design(data, logo_path=None, genero="m", grafico_b64=""):
    
    # 1. SISTEMA DINÁMICO DE COLORES Y LOGO
    if genero == "f":
        ACCENT = "#FF2D75"
        texto_edicion = "✦ EDICIÓN ELITE PINK ✦"
        logo_img = "logo_rosa.png"
    else:
        ACCENT = "#d4af37"
        texto_edicion = "✦ EDICIÓN ELITE GOLD ✦"
        logo_img = "logo_dorado.png"
        
    if not os.path.exists(logo_img):
        logo_img = "logo_tanque.png"
        
    logo_b64 = img_to_b64(logo_img)
    qr_b64 = img_to_b64("qr_code.png")

    # Extraer datos
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
    
    # Cálculos para gráficos
    total_macros = proteina + carbos + grasas
    if total_macros == 0: total_macros = 1
    pct_p = (proteina / total_macros) * 100
    pct_c = (carbos / total_macros) * 100
    pct_g = (grasas / total_macros) * 100
    
    # ==========================================
    # PÁGINA 1: PORTADA + PERFIL
    # ==========================================
    html_pagina1 = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            @page {{ size: A4; margin: 0; }}
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0a0a0a; color: #ffffff; }}
            .page {{ width: 100%; height: 100vh; background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%); display: flex; page-break-after: always; position: relative; }}
            
            .qr-corner {{ position: absolute; top: 40px; right: 40px; width: 75px; background: white; padding: 5px; border-radius: 8px; border: 2px solid {ACCENT}; z-index: 10; }}
            
            .portada {{ width: 50%; background: radial-gradient(circle at center, #2a2a2a 0%, #0a0a0a 100%); display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 40px; border-right: 3px solid {ACCENT}; position: relative; overflow: hidden; }}
            .portada::before {{ content: ''; position: absolute; top: -50%; right: -50%; width: 300px; height: 300px; background: radial-gradient(circle, {ACCENT} 0%, transparent 70%); opacity: 0.1; border-radius: 50%; }}
            .portada-content {{ position: relative; z-index: 1; text-align: center; }}
            
            .logo-img {{ width: 180px; margin: 0 auto 30px; display: block; filter: drop-shadow(0 0 15px {ACCENT}); }}
            
            .edicion {{ font-size: 12px; color: {ACCENT}; letter-spacing: 2px; margin-bottom: 20px; text-transform: uppercase; font-weight: bold; }}
            .titulo-principal {{ font-size: 42px; font-weight: bold; color: {ACCENT}; letter-spacing: 3px; margin: 20px 0; text-shadow: 0 0 10px rgba(212, 175, 55, 0.3); }}
            .subtitulo {{ font-size: 28px; color: #ffffff; letter-spacing: 2px; margin: 10px 0; }}
            .descripcion {{ font-size: 14px; color: #aaa; margin: 30px 0; letter-spacing: 1px; }}
            .atleta-name {{ font-size: 32px; color: #ffffff; font-weight: bold; margin: 20px 0; text-transform: uppercase; }}
            .level {{ font-size: 12px; color: {ACCENT}; letter-spacing: 1px; }}
            
            .metadata {{ display: flex; justify-content: space-around; margin-top: 40px; padding-top: 30px; border-top: 1px solid {ACCENT}; width: 100%; }}
            .meta-item {{ text-align: center; font-size: 11px; color: #aaa; }}
            .meta-item-value {{ color: {ACCENT}; font-size: 12px; font-weight: bold; margin-top: 5px; }}
            
            .perfil {{ width: 50%; padding: 40px; display: flex; flex-direction: column; justify-content: space-between; }}
            .perfil-header {{ color: {ACCENT}; font-size: 12px; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 20px; }}
            .perfil-number {{ font-size: 48px; font-weight: bold; color: {ACCENT}; margin-bottom: 10px; }}
            .perfil-title {{ font-size: 20px; font-weight: bold; color: #ffffff; margin-bottom: 30px; letter-spacing: 1px; }}
            
            .biometria-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 40px; }}
            .bio-card {{ background: rgba(255, 255, 255, 0.03); border-left: 3px solid {ACCENT}; padding: 12px 15px; border-radius: 2px; }}
            .bio-label {{ font-size: 10px; color: #aaa; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px; }}
            .bio-value {{ font-size: 16px; font-weight: bold; color: {ACCENT}; }}
            
            .objetivos-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 30px; }}
            .objetivo-box {{ background: rgba(255, 255, 255, 0.03); border: 1px solid {ACCENT}; padding: 12px; text-align: center; border-radius: 2px; }}
            .objetivo-label {{ font-size: 9px; color: #aaa; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 5px; }}
            .objetivo-value {{ font-size: 13px; color: #ffffff; font-weight: bold; }}
            
            .balance-section {{ background: rgba(255, 255, 255, 0.03); border: 1px solid {ACCENT}; padding: 20px; border-radius: 2px; }}
            .balance-title {{ font-size: 11px; color: {ACCENT}; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 15px; }}
            .balance-grid {{ display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 15px; }}
            .balance-item {{ text-align: center; }}
            .balance-value {{ font-size: 18px; font-weight: bold; color: #ffffff; margin-top: 5px; }}
            .balance-label {{ font-size: 9px; color: #aaa; text-transform: uppercase; margin-top: 3px; }}
            
            .water-section {{ display: flex; align-items: center; margin-top: 15px; padding-top: 15px; border-top: 1px solid rgba(255, 255, 255, 0.1); }}
            .water-label {{ font-size: 9px; color: #aaa; text-transform: uppercase; }}
            .water-value {{ font-size: 24px; font-weight: bold; color: {ACCENT}; }}
            .footer-logo {{ text-align: center; margin-top: 30px; font-size: 10px; color: #666; letter-spacing: 1px; }}
        </style>
    </head>
    <body>
        <div class="page">
            <img src="data:image/png;base64,{qr_b64}" class="qr-corner">
            <div class="portada">
                <div class="portada-content">
                    <div class="edicion">{texto_edicion}</div>
                    <img src="data:image/png;base64,{logo_b64}" class="logo-img">
                    <div class="titulo-principal">EDDY</div>
                    <div class="subtitulo">PERSONAL TRAINER</div>
                    <div class="descripcion">PLAN ELITE INTEGRAL<br>HIGH PERFORMANCE PHYSIQUE</div>
                    <div class="atleta-name">{nombre.upper()}</div>
                    <div class="level">ATLETA NIVEL: ELITE</div>
                    <div class="metadata">
                        <div class="meta-item"><div>FECHA</div><div class="meta-item-value">{datetime.now().strftime('%d %b %Y')}</div></div>
                        <div class="meta-item"><div>VERSIÓN</div><div class="meta-item-value">v100.0</div></div>
                        <div class="meta-item"><div>COACH</div><div class="meta-item-value">EDDY PT</div></div>
                    </div>
                </div>
            </div>
            
            <div class="perfil">
                <div>
                    <div class="perfil-header">01 /// Perfil y Resumen</div>
                    <div class="perfil-number">01</div>
                    <div class="perfil-title">Perfil Físico</div>
                    <div class="biometria-grid">
                        <div class="bio-card"><div class="bio-label">Edad</div><div class="bio-value">{edad} años</div></div>
                        <div class="bio-card"><div class="bio-label">Estatura</div><div class="bio-value">{estatura} cm</div></div>
                        <div class="bio-card"><div class="bio-label">Peso</div><div class="bio-value">{peso} kg</div></div>
                        <div class="bio-card"><div class="bio-label">Cintura</div><div class="bio-value">{cintura} cm</div></div>
                        <div class="bio-card"><div class="bio-label">Índice RCC</div><div class="bio-value">{rcc:.2f}</div></div>
                        <div class="bio-card"><div class="bio-label">Grasa Est.</div><div class="bio-value">{rfm:.1f} %</div></div>
                    </div>
                    <div class="objetivos-grid">
                        <div class="objetivo-box"><div class="objetivo-label">Objetivo</div><div class="objetivo-value">{tipo_objetivo}</div></div>
                        <div class="objetivo-box"><div class="objetivo-label">Nivel</div><div class="objetivo-value">{nivel}</div></div>
                    </div>
                </div>
                
                <div class="balance-section">
                    <div class="balance-title">Balance Nutricional Diario</div>
                    <div class="balance-grid">
                        <div class="balance-item"><div class="balance-value">{int(cal_obj)}</div><div class="balance-label">Kcal</div></div>
                        <div class="balance-item"><div class="balance-value">{int(proteina)}g</div><div class="balance-label">Prot</div></div>
                        <div class="balance-item"><div class="balance-value">{int(carbos)}g</div><div class="balance-label">Carbs</div></div>
                        <div class="balance-item"><div class="balance-value">{int(grasas)}g</div><div class="balance-label">Grasas</div></div>
                    </div>
                    <div class="water-section">
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
    # PÁGINA 2: NUTRICIÓN Y GRÁFICOS
    # ==========================================
    html_menus_dinamicos = ""
    if menus:
        for comida, opciones in menus.items():
            texto_opcion = str(opciones[0] if isinstance(opciones, list) and opciones else "Sin datos")
            texto_limpio = texto_opcion.replace("Opcion 1: ", "")
            html_menus_dinamicos += f'''
                    <li class="menu-item">
                        <div class="menu-meal">🍽️ {comida.upper()}</div>
                        {texto_limpio}
                    </li>'''

    offset_p = 25
    offset_c = 25 - pct_p
    offset_g = 25 - pct_p - pct_c

    html_pagina2 = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            @page {{ size: A4; margin: 0; }}
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0a0a0a; color: #ffffff; }}
            .page {{ width: 100%; height: 100vh; background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%); padding: 40px; page-break-after: always; }}
            .page-header {{ display: flex; align-items: center; margin-bottom: 30px; border-bottom: 2px solid {ACCENT}; padding-bottom: 20px; }}
            .page-number {{ font-size: 48px; font-weight: bold; color: {ACCENT}; margin-right: 20px; }}
            .page-title {{ font-size: 18px; font-weight: bold; color: #ffffff; text-transform: uppercase; letter-spacing: 2px; flex: 1; }}
            .page-brand {{ font-size: 10px; color: {ACCENT}; text-align: right; }}
            
            .section {{ background: rgba(255, 255, 255, 0.03); border: 1px solid {ACCENT}; padding: 25px; border-radius: 2px; margin-bottom: 20px; }}
            .section-title {{ font-size: 13px; font-weight: bold; color: {ACCENT}; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 20px; padding-bottom: 10px; border-bottom: 1px solid {ACCENT}; }}
            
            .graphics-grid {{ display: flex; gap: 30px; align-items: center; justify-content: center; }}
            .chart-box {{ width: 50%; text-align: center; }}
            .chart-title {{ font-size: 11px; color: #aaa; text-transform: uppercase; margin-bottom: 15px; letter-spacing: 1px; }}
            
            .menu-list {{ list-style: none; }}
            .menu-item {{ margin-bottom: 12px; padding: 12px; background: rgba(255, 255, 255, 0.02); border-left: 2px solid {ACCENT}; font-size: 11px; line-height: 1.5; }}
            .menu-meal {{ font-weight: bold; color: {ACCENT}; margin-bottom: 5px; }}
            .footer {{ display: flex; justify-content: space-between; align-items: center; margin-top: 40px; padding-top: 20px; border-top: 1px solid {ACCENT}; font-size: 10px; color: #666; }}
        </style>
    </head>
    <body>
        <div class="page">
            <div class="page-header">
                <div class="page-number">02</div>
                <div class="page-title">/// Nutrición & Analítica</div>
                <div class="page-brand">EDDY PT</div>
            </div>
            
            <div class="section">
                <div class="section-title">Evolución y Macros (AI Data)</div>
                <div class="graphics-grid">
                    <div class="chart-box">
                        <div class="chart-title">MACROS AI 3D</div>
                        <svg viewBox="0 0 42 42" style="width: 100%; max-width: 150px; margin: 0 auto; display: block;">
                            <circle cx="21" cy="21" r="15.915" fill="transparent" stroke="#222" stroke-width="5" />
                            <circle cx="21" cy="21" r="15.915" fill="transparent" stroke="{ACCENT}" stroke-width="5" stroke-dasharray="{pct_p} {100-pct_p}" stroke-dashoffset="{offset_p}" />
                            <circle cx="21" cy="21" r="15.915" fill="transparent" stroke="#00D9FF" stroke-width="5" stroke-dasharray="{pct_c} {100-pct_c}" stroke-dashoffset="{offset_c}" />
                            <circle cx="21" cy="21" r="15.915" fill="transparent" stroke="#FF9800" stroke-width="5" stroke-dasharray="{pct_g} {100-pct_g}" stroke-dashoffset="{offset_g}" />
                        </svg>
                        <div style="margin-top: 15px; font-size: 10px; color: #ddd; font-weight:bold;">
                            <span style="color:{ACCENT}">■</span> {pct_p:.0f}% Prot &nbsp; 
                            <span style="color:#00D9FF">■</span> {pct_c:.0f}% Carb &nbsp; 
                            <span style="color:#FF9800">■</span> {pct_g:.0f}% Gras
                        </div>
                    </div>
                    <div class="chart-box">
                        <div class="chart-title">PROYECCIÓN ALTA PRECISIÓN</div>
                        <img src="data:image/png;base64,{grafico_b64}" style="width: 100%; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1);">
                    </div>
                </div>
            </div>
            
            <div class="section">
                <div class="section-title">Menú Asignado del Día</div>
                <div class="menu-list">
{html_menus_dinamicos}
                </div>
            </div>
            
            <div class="footer">
                <span style="color:{ACCENT};">© EDDY PERSONAL TRAINER</span>
                <span>Página 02</span>
            </div>
        </div>
    </body>
    </html>
    """
    
    # ==========================================
    # ALGORITMO COMPRAS MENSUALES (EXTRAE GRAMOS Y * 30)
    # ==========================================
    compras_dict = {}
    if isinstance(menus, dict):
        for comidas in menus.values():
            if comidas and isinstance(comidas, list):
                texto = str(comidas[0])
                partes = texto.split('+')
                for p in partes:
                    match = re.search(r'(\d+)\s*g', p)
                    if match:
                        g_diarios = int(match.group(1))
                        p_clean = p.split('|')[0]
                        p_clean = re.sub(r'(?i)Opcion\s*\d+:\s*', '', p_clean)
                        p_clean = re.sub(r'\d+\s*g\s*', '', p_clean).strip().capitalize()
                        if p_clean and "infusion" not in p_clean.lower() and "infusión" not in p_clean.lower():
                            if p_clean in compras_dict:
                                compras_dict[p_clean] += g_diarios
                            else:
                                compras_dict[p_clean] = g_diarios

    html_compras = ""
    for item, daily_g in sorted(compras_dict.items()):
        monthly_g = daily_g * 30
        if monthly_g >= 1000:
            html_compras += f'<div class="exercise-item"><div style="font-weight: bold; color: {ACCENT};">🛒</div><div><div class="exercise-name">{item}</div></div><div style="font-weight:bold; color:white;">{monthly_g/1000:.1f} KG / Mes</div></div>'
        else:
            html_compras += f'<div class="exercise-item"><div style="font-weight: bold; color: {ACCENT};">🛒</div><div><div class="exercise-name">{item}</div></div><div style="font-weight:bold; color:white;">{monthly_g} Gramos / Mes</div></div>'

    if not html_compras:
        html_compras = f'<div class="exercise-item"><div style="font-weight: bold; color: {ACCENT};">🛒</div><div><div class="exercise-name">Fuentes de Proteína Magra</div></div><div style="font-weight:bold; color:white;">15 KG / Mes</div></div>'

    # ==========================================
    # RUTINA DINÁMICA
    # ==========================================
    html_rutinas_dinamicas = ""
    if rutina:
        for dia, ejercicios in rutina.items():
            html_rutinas_dinamicas += f'<div class="exercises-title" style="margin-top:20px;">{dia.upper()}</div>'
            for i, e in enumerate(ejercicios, 1):
                html_rutinas_dinamicas += f'''
                <div class="exercise-item">
                    <div style="font-weight: bold; color: {ACCENT};">{i}</div>
                    <div><div class="exercise-name">{e}</div></div>
                </div>'''
    else:
        html_rutinas_dinamicas = '<div class="exercise-item"><div class="exercise-name">Planificación en proceso...</div></div>'

    # ==========================================
    # PÁGINA 3: ENTRENAMIENTO Y COMPRAS
    # ==========================================
    html_pagina3 = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            @page {{ size: A4; margin: 0; }}
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0a0a0a; color: #ffffff; }}
            .page {{ width: 100%; min-height: 100vh; background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%); padding: 40px; page-break-after: always; }}
            .page-header {{ display: flex; align-items: center; margin-bottom: 30px; border-bottom: 2px solid {ACCENT}; padding-bottom: 20px; }}
            .page-number {{ font-size: 48px; font-weight: bold; color: {ACCENT}; margin-right: 20px; }}
            .page-title {{ font-size: 18px; font-weight: bold; color: #ffffff; text-transform: uppercase; letter-spacing: 2px; flex: 1; }}
            .page-brand {{ font-size: 10px; color: {ACCENT}; text-align: right; }}
            
            .exercises-section {{ background: rgba(255, 255, 255, 0.03); border: 1px solid {ACCENT}; padding: 25px; border-radius: 2px; margin-bottom: 20px; }}
            .exercises-title {{ font-size: 13px; font-weight: bold; color: {ACCENT}; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 15px; padding-bottom: 5px; border-bottom: 1px solid rgba(255,255,255,0.1); }}
            
            .exercise-item {{ display: grid; grid-template-columns: auto 1fr auto; gap: 15px; margin-bottom: 10px; padding: 12px; background: rgba(255, 255, 255, 0.02); border-left: 2px solid {ACCENT}; align-items: center; }}
            .exercise-name {{ font-size: 11px; font-weight: bold; color: #ffffff; }}
            
            .footer {{ display: flex; justify-content: space-between; align-items: center; margin-top: 40px; padding-top: 20px; border-top: 1px solid {ACCENT}; font-size: 10px; color: #666; }}
        </style>
    </head>
    <body>
        <div class="page">
            <div class="page-header">
                <div class="page-number">03</div>
                <div class="page-title">/// Entrenamiento & Abastecimiento</div>
                <div class="page-brand">EDDY PT</div>
            </div>
            
            <div class="exercises-section">
                <div class="exercises-title" style="color:white; font-size:15px;">PROTOCOLO DE ABASTECIMIENTO (MES: 30 DÍAS)</div>
                {html_compras}
            </div>

            <div class="exercises-section">
                <div class="exercises-title" style="color:white; font-size:15px;">RUTINA ASIGNADA: {tipo_entreno}</div>
                {html_rutinas_dinamicas}
            </div>
            
            <div class="footer">
                <span style="color:{ACCENT};">© EDDY PERSONAL TRAINER</span>
                <span>Página 03</span>
            </div>
        </div>
    </body>
    </html>
    """
    
    # ==========================================
    # CONVERTIR HTML A PDF (USANDO TU LÓGICA DE PYPDF2)
    # ==========================================
    try:
        pdf1 = HTML(string=html_pagina1).write_pdf()
        pdf2 = HTML(string=html_pagina2).write_pdf()
        pdf3 = HTML(string=html_pagina3).write_pdf()
        
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
        raise Exception(f"Falla interna al fusionar el PDF: {e}")