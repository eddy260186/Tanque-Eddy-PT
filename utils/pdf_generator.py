import streamlit as st
from weasyprint import HTML
import base64

def build_pdf_v60_7(d, grafico_b64, ruta_img, gen):
    # ==========================================\
    # LÓGICA DE EDICIONES LUXURY: ALPHA vs RUBY
    # ==========================================\
    # Tu sistema reconoce 'f' (femenino) y 'm' (masculino)
    is_f = (gen == "f")
    
    # --- PALETA BASE PREMIUM (Común para ambos) ---
    c_bg = "#050505"         # Negro Ébano (Fondo absoluto)
    c_card = "#0B0B0B"       # Negro Secundario (Profundidad para tarjetas)
    c_txt = "#F5F5F5"        # Blanco Humo (Texto principal, elegante y no cansa a la vista)
    c_titanio = "#878681"    # Plata Titanio (Para subtítulos y detalles sutiles)
    
    if is_f:
        # --- EDICIÓN RUBY BLACK ELITE (Femenina) ---
        c_accent = "#C0104A"     # Rubí Oscuro Metálico (Elegante, profundo)
        c_bright = "#E0115F"     # Rubí Brillante (Para resaltar números y glow)
        nombre_edicion = "RUBY BLACK ELITE"
    else:
        # --- EDICIÓN BLACK GOLD ALPHA (Masculina) ---
        c_accent = "#D4AF37"     # Dorado Metálico Premium
        c_bright = "#FFD700"     # Dorado Brillante
        nombre_edicion = "BLACK GOLD ALPHA"
    
    # --- LOGO DINÁMICO CON GLOW ---
    logo_img_html = ""
    if ruta_img:
        with open(ruta_img, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
            # El glow toma el color de la edición (Rubí o Dorado)
            logo_img_html = f'<img src="data:image/png;base64,{b64}" style="height: 100px; filter: drop-shadow(0 0 12px {c_accent});">'

    # --- MAQUETADO HTML Y CSS DE LUJO ---
    html = f"""
    <html>
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Montserrat:wght@300;400;700&display=swap" rel="stylesheet">
        <style>
            @page {{ size: A4; margin: 0; background-color: {c_bg}; }}
            body {{ 
                font-family: 'Montserrat', sans-serif; 
                color: {c_txt}; 
                background-color: {c_bg}; 
                margin: 0; padding: 0; 
            }}
            
            /* --- PORTADA CINEMATOGRÁFICA --- */
            .cover {{
                height: 100vh;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                text-align: center;
                background: radial-gradient(circle at center, #111 0%, {c_bg} 100%);
                border-bottom: 2px solid {c_accent};
            }}
            .cover h1 {{ 
                font-family: 'Bebas Neue', cursive; 
                font-size: 65px; 
                letter-spacing: 10px; 
                color: {c_accent};
                margin: 20px 0;
                text-shadow: 0px 4px 15px rgba(0,0,0,0.8);
            }}
            .cover-subtitle {{ letter-spacing: 5px; font-weight: 300; color: {c_titanio}; }}
            .edicion-badge {{ 
                background-color: transparent; 
                color: {c_txt}; 
                border: 1px solid {c_accent};
                padding: 8px 20px; 
                border-radius: 30px; 
                font-family: 'Montserrat', sans-serif;
                font-weight: 700; 
                font-size: 14px;
                letter-spacing: 3px;
                margin-top: -5px;
                box-shadow: 0 0 10px {c_accent}40;
            }}
            
            /* --- CONTENEDORES PREMIUM (CARDS) --- */
            .section {{ padding: 40px; page-break-after: always; }}
            .card-elite {{
                background: {c_card};
                border: 1px solid #1A1A1A;
                border-left: 4px solid {c_accent};
                border-radius: 12px;
                padding: 25px;
                margin-bottom: 25px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.6);
            }}
            
            /* --- TABLAS ESTILO DASHBOARD --- */
            table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
            th {{ 
                background: {c_accent}; 
                color: {c_bg}; 
                font-family: 'Bebas Neue'; 
                padding: 12px; 
                font-size: 18px;
                text-align: left;
                letter-spacing: 1px;
            }}
            td {{ 
                padding: 15px; 
                border-bottom: 1px solid #1a1a1a; 
                background: #080808;
                font-size: 13px;
                color: {c_txt};
            }}

            .accent-text {{ color: {c_accent}; font-weight: bold; }}
            .bright-text {{ color: {c_bright}; font-size: 26px; font-family: 'Bebas Neue'; letter-spacing: 2px; }}
            .glow-border {{ border: 1px solid {c_accent}; box-shadow: 0 0 20px {c_accent}30; }} 
        </style>
    </head>
    <body>
        <div class="cover">
            {logo_img_html}
            <h1>PLAN INTEGRAL ELITE</h1>
            <div class="edicion-badge">{nombre_edicion}</div>
            <p class="cover-subtitle" style="margin-top: 35px;">INGENIERÍA CORPORAL PARA ATLETAS DE ALTO VALOR</p>
            <div style="margin-top: 60px; border-top: 1px solid {c_titanio}; padding-top: 20px; width: 350px;">
                <p style="font-size: 14px; color: {c_titanio};">ATLETA</p>
                <p style="font-size: 22px; margin-top: -10px;" class="accent-text">{d['n'].upper()}</p>
                <p style="font-size: 12px; color: {c_titanio}; margin-top: 15px;">FECHA DE EMISIÓN: {d.get('fecha', '08/05/2026')}</p>
            </div>
        </div>

        <div class="section">
            <h2 style="font-family: 'Bebas Neue'; font-size: 35px; color: {c_accent}; letter-spacing: 2px;">📈 ANALÍTICA BIOMÉTRICA</h2>
            <div class="card-elite">
                <table style="border: none;">
                    <tr>
                        <td><span style="color: {c_titanio}; font-size: 11px;">ESTATURA</span><br><span class="accent-text" style="font-size: 18px;">{d['estatura']} cm</span></td>
                        <td><span style="color: {c_titanio}; font-size: 11px;">PESO ACTUAL</span><br><span class="accent-text" style="font-size: 18px;">{d['peso']} kg</span></td>
                        <td><span style="color: {c_titanio}; font-size: 11px;">ÍNDICE GRASA</span><br><span class="accent-text" style="font-size: 18px;">{d['rfm']}%</span></td>
                    </tr>
                </table>
            </div>

            <div class="card-elite glow-border">
                <h3 style="margin-top:0; color:{c_titanio}; font-size: 12px; letter-spacing: 2px;">OBJETIVO ESTRATÉGICO</h3>
                <p style="font-family: 'Bebas Neue'; font-size: 28px; color: {c_bright}; margin-top: -5px;">{d['meta'].upper()}</p>
                
                <table style="border: none; margin-top: 20px;">
                    <tr>
                        <td style="background: transparent; border: none; padding: 0;">
                            <span style="color: {c_titanio}; font-size: 11px;">ENERGÍA DIARIA</span><br>
                            <span class="bright-text">{d['k']:.0f} KCAL</span>
                        </td>
                        <td style="background: transparent; border: none; padding: 0;">
                            <span style="color: {c_titanio}; font-size: 11px;">HIDRATACIÓN ÓPTIMA</span><br>
                            <span class="bright-text">{d['w']} LTS</span>
                        </td>
                    </tr>
                </table>
            </div>

            <div style="text-align:center; margin-top:40px;">
                <h3 style="font-family: 'Bebas Neue'; color:{c_accent}; letter-spacing: 2px;">PROYECCIÓN DE EVOLUCIÓN</h3>
                <img src="data:image/png;base64,{grafico_b64}" style="width: 100%; border-radius: 12px; border: 1px solid #1A1A1A; box-shadow: 0 5px 15px rgba(0,0,0,0.5);">
            </div>
        </div>

        <div class="section">
             <h2 style="font-family: 'Bebas Neue'; font-size: 35px; color: {c_accent}; letter-spacing: 2px;">🥗 ESTRATEGIA NUTRICIONAL</h2>
             """
    for comida, opciones in d['m'].items():
        html += f"""
        <div class="card-elite">
            <h4 style="margin:0; font-family: 'Bebas Neue'; font-size: 22px; color:{c_bright}; letter-spacing: 1px;">{comida.upper()}</h4>
            <table style="margin-top: 10px;">"""
        for op in opciones:
            html += f"<tr><td>{op}</td></tr>"
        html += "</table></div>"

    html += f"""
        <div style="margin-top: 60px; text-align: center; border-top: 1px solid {c_accent}; padding-top: 30px;">
            <p style="font-family: 'Bebas Neue'; font-size: 24px; color: {c_txt}; letter-spacing: 4px; margin: 0;">EDDY PERSONAL TRAINER ELITE</p>
            <p style="font-size: 11px; color: {c_titanio}; letter-spacing: 1px; margin-top: 5px;">SOFTWARE DE INGENIERÍA CORPORAL • {nombre_edicion}</p>
        </div>
        </div>
    </body>
    </html>
    """
    return HTML(string=html).write_pdf()