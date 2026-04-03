import os

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.routers import about, auth, blog, contact, partners, projects, services, site_settings, team, upload

app = FastAPI(
    title="NeonSoft API",
    version="1.0.0",
    description="NeonSoft.uz — IT kompaniyasi backend API",
)

# ─── CORS ─────────────────────────────────────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Global exception handlers ────────────────────────────────────────────────

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(status_code=422, content={"detail": str(exc)})

# ─── Media static files ───────────────────────────────────────────────────────

os.makedirs(settings.MEDIA_DIR, exist_ok=True)
app.mount(settings.MEDIA_URL, StaticFiles(directory=settings.MEDIA_DIR), name="media")

# ─── Routers ──────────────────────────────────────────────────────────────────

# Auth + User management
app.include_router(auth.router)
app.include_router(auth.users_router)

# Services
app.include_router(services.public_router)
app.include_router(services.admin_router)

# Projects
app.include_router(projects.public_router)
app.include_router(projects.admin_router)

# Team
app.include_router(team.public_router)
app.include_router(team.admin_router)

# Blog
app.include_router(blog.public_router)
app.include_router(blog.admin_router)

# Contact
app.include_router(contact.public_router)
app.include_router(contact.admin_router)

# Site Settings
app.include_router(site_settings.public_router)
app.include_router(site_settings.admin_router)

# About
app.include_router(about.public_router)
app.include_router(about.admin_router)

# Partners
app.include_router(partners.public_router)
app.include_router(partners.admin_router)

# Upload
app.include_router(upload.router)


# ─── Health check ─────────────────────────────────────────────────────────────

@app.get("/", tags=["Health"])
async def root():
    return {"status": "ok", "app": "NeonSoft API", "docs": "/docs"}
