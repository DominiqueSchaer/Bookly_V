from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SOURCE_DIR = ROOT / "frontend-htmx"
PUBLIC_DIR = ROOT / "public"
STATIC_SOURCE_DIR = SOURCE_DIR / "static"
STATIC_TARGET_DIR = PUBLIC_DIR / "static"
INDEX_SOURCE = SOURCE_DIR / "index.html"
INDEX_TARGET = PUBLIC_DIR / "index.html"
APPROVAL_SOURCE = SOURCE_DIR / "index_approval.html"
APPROVAL_TARGET = PUBLIC_DIR / "index_approval.html"
LOCAL_API_BASE = "http://localhost:8000/api"
VERCEL_API_BASE = "/api"


def copy_static_assets() -> None:
    if STATIC_TARGET_DIR.exists():
        shutil.rmtree(STATIC_TARGET_DIR)
    shutil.copytree(STATIC_SOURCE_DIR, STATIC_TARGET_DIR)


def write_index(source: Path, target: Path) -> None:
    html = source.read_text(encoding="utf-8")
    html = html.replace(LOCAL_API_BASE, VERCEL_API_BASE, 1)
    target.write_text(html, encoding="utf-8")


def main() -> None:
    PUBLIC_DIR.mkdir(exist_ok=True)
    copy_static_assets()
    write_index(INDEX_SOURCE, INDEX_TARGET)
    if APPROVAL_SOURCE.exists():
        write_index(APPROVAL_SOURCE, APPROVAL_TARGET)


if __name__ == "__main__":
    main()
