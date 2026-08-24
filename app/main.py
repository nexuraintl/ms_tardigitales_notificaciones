import os
from fastapi import FastAPI
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Importar enrutadores de la API
from app.api.v1.routes.notificaciones import router as notificaciones_router
from app.api.v1.routes.tramites import router as tramites_router
from app.api.v1.routes.tarjetas import router as tarjetas_router

app = FastAPI(
    title="JCC Notifications & Tramites API",
    description="Microservicio en Python FastAPI modular para la gestión de notificaciones y trámites de la Junta Central de Contadores",
    version="1.0.0",
    root_path=os.getenv("ROOT_PATH", "/apig/tardigitales")
)

# Registrar rutas sin prefijo /api
app.include_router(notificaciones_router)
app.include_router(tramites_router)
app.include_router(tarjetas_router)

@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "JCC Notifications & Tramites API",
        "documentation": "/docs"
    }

@app.get("/health")
def health():
    return {
        "status": "ok"
    }
