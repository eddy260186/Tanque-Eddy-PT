from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils.logger import obtener_logger
from backend.webhooks.whatsapp_webhook import router as whatsapp_router

logger = obtener_logger("BackendPrincipal")

# Inicializar la API SaaS
app = FastAPI(
    title="Eddy PT - Motor Backend SaaS",
    description="API de alta velocidad para automatizaciones, IA y WhatsApp CRM",
    version="1.0.0"
)

# Configuración de CORS (Permite que Streamlit y servicios externos se conecten de forma segura)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, cambia esto por tu dominio específico
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusión de Routers (Módulos independientes de rutas)
app.include_router(whatsapp_router, prefix="/webhooks", tags=["Webhooks"])

@app.get("/")
def verificar_estado_servidor():
    logger.info("Consulta de estado del servidor recibida.")
    return {"status": "online", "message": "Motor Elite de FastAPI operando al 100%"}

if __name__ == "__main__":
    import uvicorn
    # Le decimos a Uvicorn la ruta exacta del módulo desde la raíz
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)