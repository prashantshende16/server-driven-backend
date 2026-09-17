from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from app.api import pages, mobile, auth, forms, model_definitions, navigation, app_config
from app.core.config import settings
from app.core.database import engine
from app.models.base import Base
# Import all models so they are registered with Base.metadata
from app.models import User, Page, Form, AppConfig, ModelDefinition, Navigation
from app.core.seed import seed_initial_data

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

@app.on_event("startup")
async def startup():
    # Create all tables automatically on startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        # Auto-migrate any newly added columns
        await conn.execute(text("ALTER TABLE forms ADD COLUMN IF NOT EXISTS is_published BOOLEAN DEFAULT FALSE;"))
        await conn.execute(text("ALTER TABLE forms ADD COLUMN IF NOT EXISTS version INTEGER DEFAULT 1;"))
    # Seed default templates and mobile navigation if empty
    await seed_initial_data()

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(pages.router, prefix="/api/v1/admin/pages", tags=["admin-pages"])
app.include_router(forms.router, prefix="/api/v1/admin/forms", tags=["admin-forms"])
app.include_router(model_definitions.router, prefix="/api/v1/admin/models", tags=["admin-models"])
app.include_router(navigation.router, prefix="/api/v1/admin/navigation", tags=["admin-navigation"])
app.include_router(app_config.router, prefix="/api/v1/admin/config", tags=["admin-config"])
app.include_router(mobile.router, prefix="/api/v1/mobile", tags=["mobile"])

@app.get("/health")
def health():
    return {"status": "ok"}
