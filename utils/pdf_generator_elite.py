# =========================================================
# PDF GENERATOR ELITE v8.5 - WEASYPRINT SAFE EDITION
# Motor Original (PyPDF2) + CSS Optimizado para PDF
# =========================================================

from weasyprint import HTML
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
    
    total_macros = proteina + carbos + grasas
    if total_macros == 0: total_macros = 1
    pct_p = (proteina / total_macros) * 100
    pct_c = (carbos / total_macros) * 100
    pct_g = (grasas / total_macros) * 100

    # ==========================================
    # PÁGINA 1: PORTADA + PERFIL (CSS CORREGIDO)
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
            
            .page {{ width: 100%; height: 297mm; position: relative; background: #0a0a0a; }}
            .qr-corner {{ position: absolute; top: 30px; right: 30px; width: 70px; background: white; padding: 4px; border-radius: 8px; border: 2px solid {ACCENT}; z-index: 10; }}
            
            /* Usamos float para simular columnas exactas que WeasyPrint entiende */
            .portada {{ width: 45%; height: 100%; float: left; background: #111; padding: 40px; text-align: center; border-right: 3px solid {ACCENT}; }}
            .perfil {{ width: 55%; height: 100%; float: left; padding: 40px 30px; background: #0a0a0a; }}
            
            .logo-img {{ width: 160px; margin-top: 50px; margin-bottom: 20px; }}
            .edicion {{ font-size: 11px; color: {ACCENT}; letter-spacing: 2px; margin-bottom: 20px; text-transform: uppercase; font-weight: bold; }}
            .titulo-principal {{ font-size: 40px; font-weight: bold; color: {ACCENT}; letter-spacing: 3px; margin-top: 10px; margin-bottom: 5px; }}
            .subtitulo {{ font-size: 22px; color: #ffffff; letter-spacing: 2px; margin-bottom: 30px; }}
            .atleta-name {{ font-size: 28px; color: #ffffff; font-weight: bold; margin-top: 40px; text-transform: uppercase; }}
            .level {{ font-size: 12px; color: {ACCENT}; letter-spacing: 1px; margin-top: 10px; }}
            
            .perfil-header {{ color: {ACCENT}; font-size: 12px; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 15px; }}
            .perfil-title {{ font-size: 20px; font-weight: bold; color: #ffffff; margin-bottom: 25px; border-bottom: 1px solid #333; padding-bottom: 10px; }}
            
            /* Reemplazo de Grid por Inline-Block para biometria */
            .bio-card {{ display: inline-block; width: 48%; background: #161616; border-left: 3px solid {ACCENT}; padding: 12px; margin-bottom: 15px; margin-right: 1%; vertical-align: top; }}
            .bio-label {{ font-size: 10px; color: #aaa; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px; }}
            .bio-value {{ font-size: 16px; font-weight: bold; color: {ACCENT}; }}
            
            .objetivo-box {{ display: inline-block; width: 48%; background: #111; border: 1px solid {ACCENT}; padding: 12px; text-align: center; margin-bottom: 15px; margin-right: 1%; vertical-align: top; }}
            .objetivo-label {{ font-size: 9px; color: #aaa; text-transform: uppercase; margin-bottom: 5px; }}
            .objetivo-value {{ font-size: 12px; color: #ffffff; font-weight: bold; }}
            
            .balance-section {{ background: #111; border: 1px solid {ACCENT}; padding: 20px; margin-top: 20px; }}
            .balance-title {{ font-size: 11px; color: {ACCENT}; text-transform: uppercase; margin-bottom: 15px; }}
            
            /* Reemplazo de Grid por Tabla para balance */
            .balance-table {{ width: 100%; text-align: center; }}
            .balance-table td {{ padding: 10px 0; }}
            .balance-value {{ font-size: 18px; font-weight: bold; color: #ffffff; }}
            .balance-label {{ font-size: 9px; color: #aaa; text-transform: uppercase; margin-top: 3px; }}
        </style>
    </head>
    <body>
        <div class="page">
            <img src="data:image/png;base64,{qr_b64}" class="qr-corner">
            
            <div class="portada">
                <div class="edicion">{texto_edicion}</div>
                <img src="data:image/png;base64,{logo_b64}" class="logo-img">
                <div class="titulo-principal">EDDY</div>
                <div class="subtitulo">PERSONAL TRAINER</div>
                <div style="font-size: 12px; color: #888; margin-top: 20px; line-height: 1.8;">INGENIERÍA CORPORAL<br>DE ALTO RENDIMIENTO</div>
                <div class="atleta-name">{nombre.upper()}</div>
                <div class="level">NIVEL: {nivel.upper()}</div>
                <div style="margin-top: 50px; font-size: 10px; color: #666;">FECHA: {datetime.now().strftime('%d %b %Y')}</div>
            </div>
            
            <div class="perfil">
                <div class="perfil-header">01 /// Analítica Corporal</div>
                <div class="perfil-title">Perfil Físico del Atleta</div>
                
                <div>
                    <div class="bio-card"><div class="bio-label">Edad</div><div class="bio-value">{edad} años</div></div>
                    <div class="bio-card"><div class="bio-label">Estatura</div><div class="bio-value">{estatura} cm</div></div>
                    <div class="bio-card"><div class="bio-label">Peso</div><div class="bio-value">{peso} kg</div></div>
                    <div class="bio-card"><div class="bio-label">Grasa (RFM)</div><div class="bio-value">{rfm:.1f} %</div></div>
                </div>
                
                <div style="margin-top: 20px;">
                    <div class="objetivo-box"><div class="objetivo-label">Objetivo</div><div class="objetivo-value">{tipo_objetivo}</div></div>
                    <div class="objetivo-box"><div class="objetivo-label">Hidratación</div><div class="objetivo-value">{agua} LITROS / DÍA</div></div>
                </div>
                
                <div class="balance-section">
                    <div class="balance-title">Balance Nutricional Diario</div>
                    <table class="balance-table">
                        <tr>
                            <td><div class="balance-value">{int(cal_obj)}</div><div class="balance-label">Kcal</div></td>
                            <td><div class="balance-value">{int(proteina)}g</div><div class="balance-label">Prot</div></td>
                            <td><div class="balance-value">{int(carbos)}g</div><div class="balance-label">Carbs</div></td>
                            <td><div class="balance-value">{int(grasas)}g</div><div class="balance-label">Grasas</div></td>
                        </tr>
                    </table>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    # ==========================================
    # PÁGINA 2: NUTRICIÓN Y GRÁFICOS (TABLAS SEGURAS)
    # ==========================================
    html_menus_dinamicos = ""
    if menus:
        for comida, opciones in menus.items():
            texto_opcion = str(opciones[0] if isinstance(opciones, list) and opciones else "Sin datos")
            texto_limpio = texto_opcion.replace("Opcion 1: ", "")
            html_menus_dinamicos += f'''
                    <div style="background: #111; border-left: 3px solid {ACCENT}; padding: 15px; margin-bottom: 12px;">
                        <div style="color: {ACCENT}; font-size: 12px; font-weight: bold; margin-bottom: 8px;">🍽️ {comida.upper()}</div>
                        <div style="font-size: 12px; color: #ddd; line-height: 1.6;">{texto_limpio}</div>
                    </div>'''

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
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0a0a0a; color: #ffffff; padding: 40px; }}
            
            .page-header {{ border-bottom: 2px solid {ACCENT}; padding-bottom: 15px; margin-bottom: 30px; }}
            .page-title {{ font-size: 18px; font-weight: bold; color: {ACCENT}; text-transform: uppercase; }}
            
            .section-title {{ font-size: 14px; font-weight: bold; color: #fff; text-transform: uppercase; margin-bottom: 20px; border-bottom: 1px solid #333; padding-bottom: 5px; }}
            
            /* Gráficos en Tabla para que WeasyPrint no los desalinee */
            .chart-table {{ width: 100%; margin-bottom: 30px; }}
            .chart-table td {{ vertical-align: middle; background: #111; padding: 20px; border: 1px solid #222; }}
        </style>
    </head>
    <body>
        <div class="page-header">
            <div class="page-title">02 /// Nutrición & Evolución</div>
        </div>
        
        <div class="section-title">Evolución y Macros (AI Data)</div>
        <table class="chart-table">
            <tr>
                <td style="width: 35%; text-align: center;">
                    <div style="font-size: 11px; color: #aaa; margin-bottom: 15px;">MACROS AI 3D</div>
                    <svg viewBox="0 0 42 42" style="width: 130px; display: block; margin: 0 auto;">
                        <circle cx="21" cy="21" r="15.915" fill="transparent" stroke="#222" stroke-width="5" />
                        <circle cx="21" cy="21" r="15.915" fill="transparent" stroke="{ACCENT}" stroke-width="5" stroke-dasharray="{pct_p} {100-pct_p}" stroke-dashoffset="{offset_p}" />
                        <circle cx="21" cy="21" r="15.915" fill="transparent" stroke="#00D9FF" stroke-width="5" stroke-dasharray="{pct_c} {100-pct_c}" stroke-dashoffset="{offset_c}" />
                        <circle cx="21" cy="21" r="15.915" fill="transparent" stroke="#FF9800" stroke-width="5" stroke-dasharray="{pct_g} {100-pct_g}" stroke-dashoffset="{offset_g}" />
                    </svg>
                    <div style="margin-top: 15px; font-size: 10px; font-weight:bold;">
                        <span style="color:{ACCENT}">■</span> {pct_p:.0f}% Prot <br>
                        <span style="color:#00D9FF">■</span> {pct_c:.0f}% Carb <br>
                        <span style="color:#FF9800">■</span> {pct_g:.0f}% Gras
                    </div>
                </td>
                <td style="width: 65%; text-align: center;">
                    <div style="font-size: 11px; color: #aaa; margin-bottom: 15px;">PROYECCIÓN DE PESO</div>
                    <img src="data:image/png;base64,{grafico_b64}" style="width: 100%; max-width: 400px;">
                </td>
            </tr>
        </table>
        
        <div class="section-title">Menú Asignado del Día</div>
        {html_menus_dinamicos}
    </body>
    </html>
    """
    
    # ==========================================
    # ALGORITMO COMPRAS MENSUALES (EXTRAE GRAMOS Y * 30)
    # ==========================================
    compras_dict = {}
    if isinstance(menus, dict):
        for comidas in menus.items():
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
            html_compras += f'<div style="background: #111; border-left: 2px solid {ACCENT}; padding: 10px; margin-bottom: 8px; font-size: 12px;"><span style="color:{ACCENT}; font-weight:bold;">🛒 {item}</span> <span style="float:right;">{monthly_g/1000:.1f} KG</span></div>'
        else:
            html_compras += f'<div style="background: #111; border-left: 2px solid {ACCENT}; padding: 10px; margin-bottom: 8px; font-size: 12px;"><span style="color:{ACCENT}; font-weight:bold;">🛒 {item}</span> <span style="float:right;">{monthly_g} Gr</span></div>'

    if not html_compras:
        html_compras = f'<div style="background: #111; border-left: 2px solid {ACCENT}; padding: 10px; font-size: 12px;">Lista de mercado en proceso...</div>'

    # ==========================================
    # RUTINA DINÁMICA
    # ==========================================
    html_rutinas_dinamicas = ""
    if rutina:
        for dia, ejercicios in rutina.items():
            html_rutinas_dinamicas += f'<div style="color: {ACCENT}; font-size: 13px; font-weight: bold; margin-top: 20px; margin-bottom: 10px; border-bottom: 1px solid #333; padding-bottom: 5px;">{dia.upper()}</div>'
            for i, e in enumerate(ejercicios, 1):
                html_rutinas_dinamicas += f'''
                <div style="background: #161616; padding: 10px; margin-bottom: 6px; font-size: 11px; color: #ddd;">
                    <span style="color: {ACCENT}; font-weight: bold; margin-right: 10px;">{i}.</span> {e}
                </div>'''

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
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0a0a0a; color: #ffffff; padding: 40px; }}
            
            .page-header {{ border-bottom: 2px solid {ACCENT}; padding-bottom: 15px; margin-bottom: 30px; }}
            .page-title {{ font-size: 18px; font-weight: bold; color: {ACCENT}; text-transform: uppercase; }}
            
            .section-title {{ font-size: 14px; font-weight: bold; color: #fff; text-transform: uppercase; margin-bottom: 15px; margin-top: 30px; }}
        </style>
    </head>
    <body>
        <div class="page-header">
            <div class="page-title">03 /// Protocolos Finales</div>
        </div>
        
        <div class="section-title">Lista de Abastecimiento (30 Días)</div>
        {html_compras}

        <div class="section-title">Entrenamiento: {tipo_entreno}</div>
        {html_rutinas_dinamicas}
    </body>
    </html>
    """
    
    # ==========================================
    # CONVERTIR HTML A PDF (PYPDF2 MERGER)
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