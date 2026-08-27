import os
import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from app.api.v1.routes import tarjetas, tramites, notificaciones

app = FastAPI(
    title="Microservicio Tarjetas Digitales y Notificaciones",
    description="API Gateway Multitenant para Tarjetas Digitales, Trámites y Emisión de Notificaciones",
    version="1.0.0",
    docs_url=None,
    redoc_url=None,
    openapi_url="/tardigitales/openapi.json"
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Documentación Swagger personalizada detrás del Gateway
@app.get("/tardigitales/docs", include_in_schema=False)
async def custom_swagger_ui():
    return get_swagger_ui_html(
        openapi_url="/apig/tardigitales/openapi.json",
        title="Tarjetas Digitales API - Swagger Docs"
    )

# -------------------------------------------------------------
# ROUTER ADMINISTRATIVO CENTRAL: /tardigitales/admin
# -------------------------------------------------------------
admin_router = APIRouter(prefix="/tardigitales/admin")

admin_router.include_router(notificaciones.router, prefix="/notificaciones", tags=["Admin - Notificaciones"])
admin_router.include_router(tramites.router, prefix="/tramites", tags=["Admin - Trámites"])
admin_router.include_router(tarjetas.router, prefix="/tarjetas", tags=["Admin - Tarjetas Digitales"])

app.include_router(admin_router)

# Ruta informativa raíz
@app.get("/", include_in_schema=False)
@app.get("/tardigitales", include_in_schema=False)
async def root():
    return {
        "status": "online",
        "service": "Microservicio Tarjetas Digitales y Notificaciones",
        "architecture": "Layered (Controller - Service - Repository - Schema)",
        "admin_prefix": "/tardigitales/admin",
        "docs": "/apig/tardigitales/docs"
    }

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
