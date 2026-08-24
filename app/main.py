# Microservicio de Tarjetas Digitales y Notificaciones - nxPlatform
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.routes import notificaciones, tarjetas, tramites

tags_metadata = [
    {
        "name": "Tarjetas Digitales",
        "description": "Gestión de solicitudes, emisión, credenciales digitales e historial de estados y lecturas QR para Contadores y Sociedades.",
    },
    {
        "name": "Gestión de Trámites",
        "description": "Administración del catálogo oficial de trámites, costos, vigencia y requisitos para la entidad.",
    },
    {
        "name": "Centro de Notificaciones",
        "description": "Emisión masiva y programación de notificaciones push, alertas y comunicados oficiales.",
    },
    {
        "name": "Configuración y Utilidades",
        "description": "Parámetros del validador público QR y consulta de certificados generados.",
    },
]

app = FastAPI(
    title="Microservicio de Tarjetas Digitales y Notificaciones",
    description="API Gateway Backend para la gestión de tarjetas profesionales digitales, trámites, validación QR y centro de notificaciones institucionales de nxPlatform.",
    version="1.0.0",
    openapi_tags=tags_metadata,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tarjetas.router, prefix="", tags=["Tarjetas Digitales"])
app.include_router(tramites.router, prefix="", tags=["Gestión de Trámites"])
app.include_router(notificaciones.router, prefix="", tags=["Centro de Notificaciones"])

@app.get("/", tags=["Configuración y Utilidades"], summary="Estado general del servicio")
def root():
    return {
        "status": "online",
        "service": "ms_tardigitales_notificaciones",
        "version": "1.0.0",
        "documentation": "/docs"
    }

@app.get("/health", tags=["Configuración y Utilidades"], summary="Verificación de salud (Healthcheck)")
def health():
    return {"status": "ok", "healthy": True}
