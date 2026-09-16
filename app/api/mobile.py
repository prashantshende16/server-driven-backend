from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import get_db
from app.models.page import Page
from app.models.app_config import AppConfig
from app.utils.response import success_response, error_response

router = APIRouter()

@router.get("/config")
async def get_mobile_config(db: AsyncSession = Depends(get_db)):
    # Fetch global config
    result = await db.execute(select(AppConfig).limit(1))
    config = result.scalar_one_or_none()
    
    # Fetch published pages
    pages_result = await db.execute(select(Page).filter(Page.is_published == True, Page.status == "published"))
    pages = pages_result.scalars().all()
    
    base_config = {
        "schema_version": 1,
        "app": {
            "name": "FlowForge",
            "minimum_version": "1.0.0"
        },
        "theme": config.theme if config else {},
        "navigation": config.navigation if config else {},
        "pages": [{"id": str(p.id), "slug": p.slug, "title": p.title, "route": p.route} for p in pages]
    }
    return success_response(data=base_config)

@router.get("/pages/{slug}")
async def get_published_page(slug: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Page).filter(Page.slug == slug, Page.is_published == True))
    page = result.scalar_one_or_none()
    
    if not page:
        return error_response(message="Page not found or not published")
        
    return success_response(data={
        "id": str(page.id),
        "schema_version": 1,
        "version": page.version,
        "title": page.title,
        "layout": {"type": page.layout_type},
        "components": page.components
    })

