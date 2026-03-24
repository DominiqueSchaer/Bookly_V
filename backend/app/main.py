from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .routers import bookings, health
from .settings import settings

ROOT_DIR = Path(__file__).resolve().parents[2]
PUBLIC_DIR = ROOT_DIR / "public"
FRONTEND_DIR = ROOT_DIR / "frontend-htmx"


def _resolve_frontend_file(filename: str) -> Path:
    public_path = PUBLIC_DIR / filename
    if public_path.exists():
        return public_path

    source_path = FRONTEND_DIR / filename
    if source_path.exists():
        return source_path

    raise HTTPException(status_code=404, detail=f"Frontend asset '{filename}' is not available")


def _resolve_static_dir() -> Path:
    for candidate in (PUBLIC_DIR / "static", FRONTEND_DIR / "static"):
        if candidate.exists():
            return candidate

    raise RuntimeError("No static asset directory found")

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(bookings.router)
app.mount("/static", StaticFiles(directory=_resolve_static_dir()), name="static")


@app.get("/", include_in_schema=False)
async def read_root() -> FileResponse:
    return FileResponse(_resolve_frontend_file("index.html"))


@app.get("/index.html", include_in_schema=False)
async def read_index() -> FileResponse:
    return FileResponse(_resolve_frontend_file("index.html"))


@app.get("/index_approval.html", include_in_schema=False)
async def read_approval_index() -> FileResponse:
    return FileResponse(_resolve_frontend_file("index_approval.html"))
