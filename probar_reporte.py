# probar_reporte.py — corré esto para ver el reporte AHORA sin esperar al domingo
from dotenv import load_dotenv
load_dotenv()

from automation.reporte_semanal import enviar_reportes_semanales

if __name__ == "__main__":
    print("📊 Generando y enviando reportes semanales de prueba...")
    enviados = enviar_reportes_semanales()
    print(f"✅ Listo. Reportes enviados: {enviados}")