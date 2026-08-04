import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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
    version="1.0.0"
)

# Configurar CORS (Cross-Origin Resource Sharing)
# Esto permite que la aplicación de Angular (puerto 4300) consuma esta API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://local-jcc.ng.nexura.com:4300",
        "http://localhost:4300"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar rutas con el prefijo /api
app.include_router(notificaciones_router, prefix="/api")
app.include_router(tramites_router, prefix="/api")
app.include_router(tarjetas_router, prefix="/api")

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
