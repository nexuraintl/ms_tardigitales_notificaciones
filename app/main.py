# Microservicio de Tarjetas Digitales y Notificaciones - nxPlatform
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
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
    docs_url=None,       # Desactivamos los docs por defecto para personalizar la URL del schema
    redoc_url=None,
    openapi_url="/tardigitales/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas bajo el prefijo institucional /tardigitales
app.include_router(tarjetas.router, prefix="/tardigitales", tags=["Tarjetas Digitales"])
app.include_router(tramites.router, prefix="/tardigitales", tags=["Gestión de Trámites"])
app.include_router(notificaciones.router, prefix="/tardigitales", tags=["Centro de Notificaciones"])

@app.get("/", tags=["Configuración y Utilidades"], summary="Estado general del servicio")
@app.get("/tardigitales", tags=["Configuración y Utilidades"], summary="Estado general del servicio")
def root():
    return {
        "status": "online",
        "service": "ms_tardigitales_notificaciones",
        "version": "1.0.0",
        "documentation": "/apig/tardigitales/docs"
    }

@app.get("/health", tags=["Configuración y Utilidades"], summary="Verificación de salud (Healthcheck)")
@app.get("/tardigitales/health", tags=["Configuración y Utilidades"], summary="Verificación de salud (Healthcheck)")
def health():
    return {"status": "ok", "healthy": True}

# Swagger UI enriquecido con la ruta absoluta del Gateway
@app.get("/tardigitales/docs", include_in_schema=False)
@app.get("/docs", include_in_schema=False)
async def swagger_ui():
    return get_swagger_ui_html(
        openapi_url="/apig/tardigitales/openapi.json",
        title="Tarjetas Digitales & Notificaciones - Swagger Docs",
        swagger_favicon_url="https://fastapi.tiangolo.com/img/favicon.png"
    )

# ReDoc
@app.get("/tardigitales/redoc", include_in_schema=False)
@app.get("/redoc", include_in_schema=False)
async def redoc_ui():
    return get_redoc_html(
        openapi_url="/apig/tardigitales/openapi.json",
        title="Tarjetas Digitales & Notificaciones - ReDoc",
        redoc_favicon_url="https://fastapi.tiangolo.com/img/favicon.png"
    )

@app.get("/openapi.json", include_in_schema=False)
def openapi_redirect():
    return RedirectResponse(url="/tardigitales/openapi.json")
