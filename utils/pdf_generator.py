# ==========================================
# 8. MOTOR PDF BLINDADO 
# ==========================================
import streamlit as st
from weasyprint import HTML
import base64

# ... aquí abajo sigue tu función def build_pdf_v60_7 ...

def build_pdf_v60_7(d, grafico_b64, ruta_img, gen):
    is_f = (gen == "f")
    c_bg = "#1A1A1A" if is_f else "#121212"
    c_card = "#2A2A2A" if is_f else "#1a1a1a"
    c_accent = "#FFB6C1" if is_f else "#d4af37"
    c_txt = "#ffffff"
    
    logo_td = ""
    if ruta_img:
        with open(ruta_img, "rb") as image_file:
            logo_base64 = base64.b64encode(image_file.read()).decode("utf-8")
            logo_td = f'<img src="data:image/png;base64,{logo_base64}" style="height: 70px; border: 2px solid {c_accent}; border-radius: 8px; padding: 5px; background: #000;">'

    html = f"""
    <html><head><style>
        @page {{ size: A4; margin: 15mm; background-color: {c_bg}; }}
        body {{ font-family: 'Helvetica'; color: {c_txt}; background-color: {c_bg}; line-height: 1.5; }}
        
        .header-table {{ width: 100%; background: #000000; border-bottom: 5px solid {c_accent}; border-radius: 10px 10px 0 0; border-collapse: collapse; }}
        .header-table td {{ padding: 20px; border-bottom: none; }}
        .header-logo-td {{ text-align: right; vertical-align: middle; width: 120px; }}
        
        .profile-box {{ background: {c_card}; padding: 15px; margin: 20px 0; border: 2px solid {c_accent}; border-radius: 8px; color: {c_txt}; }}
        .stats-box {{ background: {c_card}; padding: 15px; margin: 20px 0; border-left: 10px solid {c_accent}; color: {c_txt}; border-radius: 4px; }}
        .graph-box {{ text-align: center; margin: 20px 0; padding: 10px; border: 2px solid {c_accent}; background: #000000; border-radius: 8px; }}
        .water-box {{ background: #000000; padding: 10px; border: 2px dashed {c_accent}; border-radius: 5px; color: {c_accent}; font-weight: bold; margin-top: 10px; text-align: center; font-size: 14px; }}
        
        table.data-table {{ width: 100%; border-collapse: collapse; margin-top: 10px; background-color: {c_card}; }}
        table.data-table td {{ padding: 10px; border-bottom: 1px dashed {c_accent}; font-size: 11px; color: {c_txt}; }}
        
        h1, h2, h3 {{ color: {c_accent}; }}
        b, strong {{ color: {c_accent}; }}
        li {{ color: {c_txt}; margin-bottom: 5px; }}
    </style></head>
    <body>
        <table class="header-table">
            <tr>
                <td>
                    <h1 style="margin: 0;">EDDY PERSONAL TRAINER</h1>
                    <p style="margin: 5px 0 0 0; color: #fff;">PLAN ELITE INTEGRAL - {"EDICIÓN SOFT PINK" if is_f else "EDICIÓN GOLD"}</p>
                </td>
                <td class="header-logo-td">{logo_td}</td>
            </tr>
        </table>
        
        <div class="profile-box">
            <h2 style="margin-top: 0;">👤 PERFIL FÍSICO Y BIOMÉTRICO</h2>
            <p><b>NOMBRE:</b> {d['n'].upper()} | <b>NIVEL:</b> {d['nivel'].upper()}</p>
            <p><b>EDAD:</b> {d['edad']} años | <b>ESTATURA:</b> {d['estatura']} cm | <b>PESO ACTUAL:</b> {d['peso']} kg</p>
            <p><b>CINTURA:</b> {d['cintura']} cm | <b>CADERA:</b> {d['cadera']} cm | <b>ÍNDICE RCC:</b> {d['rcc']} | <b>GRASA EST.:</b> {d['rfm']}%</p>
            <hr style="border-color: {c_accent};">
            <p><b>ENTRENAMIENTO:</b> {d['entreno']} | <b>FRECUENCIA:</b> {d['dias']} días/sem.</p>
            <p><b>META PRINCIPAL:</b> {d['meta']} | <b>ESTILO DE DIETA:</b> {d['dt']}</p>
        </div>

        <div class="stats-box">
            <h2>📊 BALANCE NUTRICIONAL KATCH-MCARDLE</h2>
            <p><b>CALORÍAS OBJETIVO:</b> {d['k']:.0f} kcal</p>
            <p><b>SUMATORIA TOTAL DEL MENÚ:</b> {d['k']:.0f} kcal ✅</p>
            <p>Macros Diarios: <b>Proteína:</b> {d['p']:.0f}g | <b>Carbohidratos:</b> {d['c']:.0f}g | <b>Grasas:</b> {d['g']:.0f}g</p>
            <div class="water-box">💧 OBJETIVO DE HIDRATACIÓN DIARIA: {d['w']} LITROS</div>
        </div>

        <div class="graph-box">
            <h3 style="margin-top: 0;">📈 PROYECCIÓN DE PESO ESTIMADA</h3>
            <img src="data:image/png;base64,{grafico_b64}" style="width: 100%; max-width: 600px; border-radius: 5px;">
        </div>

        <h2 style="margin-top: 20px; text-transform: uppercase; letter-spacing: 2px; border: 1px solid {c_accent}; padding: 10px; background: #000; text-align: center;">📢 MENÚ DE LAS COMIDAS</h2>
    """
    for c, ops in d['m'].items():
        html += f"<h3>🍴 {c}</h3><table class='data-table'>"
        for o in ops:
            html += f"<tr><td>{o}</td></tr>"
        html += "</table>"
    
    html += f"""
    <div class="stats-box" style="margin-top: 30px;">
        <h2 style="margin-top: 0;">💊 SUPLEMENTACIÓN Y MICRONUTRIENTES</h2>
        <ul>"""
    for s in d['s']:
        html += f"<li>{s}</li>"
        
    html += f"""</ul>
    </div>
    
    <div style="page-break-before: always;"></div>
    
    <table class="header-table">
        <tr>
            <td>
                <h1 style="margin: 0;">🏋️‍♂️ PLAN DE ENTRENAMIENTO</h1>
                <p style="margin: 5px 0 0 0; color: #fff;">DISTRIBUCIÓN {d['nivel'].upper()}</p>
            </td>
            <td class="header-logo-td">{logo_td}</td>
        </tr>
    </table>
    <br>
    """
    
    for dia, ejercicios in d['rutina'].items():
        html += f"<h3>📅 {dia}</h3><table class='data-table'>"
        for e in ejercicios:
            html += f"<tr><td>{e}</td></tr>"
        html += "</table>"
        
    html += f"""
    <div style="page-break-before: always;"></div>
    
    <table class="header-table">
        <tr>
            <td>
                <h1 style="margin: 0;">🛒 TICKET DE COMPRA MENSUAL</h1>
                <p style="margin: 5px 0 0 0; color: #fff;">LISTA AUTOMATIZADA</p>
            </td>
            <td class="header-logo-td">{logo_td}</td>
        </tr>
    </table>
    <p style="text-align: center; color: {c_accent}; margin-top: 20px;"><i>Cantidades estimadas para 30 días de rotación completa del menú.</i></p>
    <table class='data-table'>"""
    
    for item, cant in d['compras'].items():
        if "Huevo" in item or "Claras" in item:
            unidades = int(cant / 50)
            res = f"{unidades} Unidades (~{round(unidades/12, 1)} Docenas)"
        elif any(x in item for x in ["Café", "Mate", "Té", "Infusión"]):
            res = f"{int(cant)} Porciones/Tazas"
        else:
            if cant >= 1000:
                res = f"{round(cant/1000, 2)} KG"
            else:
                res = f"{int(cant)} g"
        html += f"<tr><td><b>{item}</b></td><td style='text-align: right;'>{res}</td></tr>"
    
    html += f"""</table>
        <div style="margin-top: 40px; text-align: center; font-size: 10px; color: {c_accent};">
            Diseñado por Eddy Personal Trainer - Instagram: @eddy_personal_trainer | Moreno, Buenos Aires
        </div>
    </body></html>"""
    
    return HTML(string=html).write_pdf()