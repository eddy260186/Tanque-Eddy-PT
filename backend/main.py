from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from utils.logger import obtener_logger

# Router WhatsApp
from backend.webhooks.whatsapp_webhook import (
    router as whatsapp_router
)

# Scheduler de automatizaciones
from automation.scheduler import iniciar_scheduler

logger = obtener_logger("BackendPrincipal")

# =========================================================
# FASTAPI
# =========================================================

app = FastAPI(
    title="Eddy PT - Motor Backend SaaS",
    description="API profesional para IA, WhatsApp y automatizaciones",
    version="2.0.0"
)

# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================================================
# ROUTERS
# =========================================================

app.include_router(
    whatsapp_router,
    prefix="/webhooks",
    tags=["WhatsApp"]
)

# =========================================================
# STARTUP: ENCENDER EL RELOJ MAESTRO
# =========================================================

@app.on_event("startup")
def startup_event():

    logger.info("🚀 Backend iniciando...")

    try:

        iniciar_scheduler()

    except Exception as e:

        logger.error(
            f"❌ Error iniciando scheduler: {str(e)}"
        )

# =========================================================
# ROOT
# =========================================================

@app.get("/")
def root():

    logger.info("Root endpoint OK")

    return {
        "backend": "online",
        "status": "active",
        "service": "Eddy PT SaaS"
    }

# =========================================================
# HEALTHCHECK
# =========================================================

@app.get("/health")
def health():

    logger.info("Healthcheck OK")

    return {
        "status": "ok",
        "message": "Backend funcionando correctamente"
    }

# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )