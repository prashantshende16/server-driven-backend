from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import pages, mobile, auth
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Backend-driven UI API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(pages.router, prefix="/api/v1/admin/pages", tags=["admin-pages"])
app.include_router(mobile.router, prefix="/api/v1/mobile", tags=["mobile"])

@app.get("/health")
def health():
    return {"status": "ok"}

