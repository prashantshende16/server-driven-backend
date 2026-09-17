from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import get_db
from app.models.page import Page
from app.models.app_config import AppConfig
from app.models.form import Form
from app.models.model_definition import ModelDefinition
from app.models.navigation import Navigation
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

    # Fetch active navigation (e.g., bottom_tabs)
    nav_result = await db.execute(select(Navigation).filter(Navigation.is_active == True))
    active_navs = nav_result.scalars().all()
    nav_dict = {}
    for n in active_navs:
        nav_dict[n.nav_type] = {
            "name": n.name,
            "type": n.nav_type,
            "items": n.items
        }
    
    base_config = {
        "schema_version": 1,
        "app": {
            "name": "FlowForge",
            "minimum_version": "1.0.0"
        },
        "theme": config.theme if config else {},
        "navigation": nav_dict or (config.navigation if config else {}),
        "pages": [{"id": str(p.id), "slug": p.slug, "title": p.title, "route": p.route} for p in pages]
    }
    return success_response(data=base_config)

@router.get("/navigation")
async def get_mobile_navigation(db: AsyncSession = Depends(get_db)):
    nav_result = await db.execute(select(Navigation).filter(Navigation.is_active == True))
    active_navs = nav_result.scalars().all()
    return success_response(data=[{
        "id": str(n.id),
        "name": n.name,
        "slug": n.slug,
        "type": n.nav_type,
        "items": n.items
    } for n in active_navs])

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

@router.get("/forms/{slug}")
async def get_published_form(slug: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Form).filter(Form.slug == slug, Form.is_published == True))
    form_obj = result.scalar_one_or_none()
    
    if not form_obj:
        return error_response(message="Form not found or not published")
        
    return success_response(data={
        "id": str(form_obj.id),
        "name": form_obj.name,
        "slug": form_obj.slug,
        "title": form_obj.title,
        "description": form_obj.description,
        "fields": form_obj.fields,
        "validation_rules": form_obj.validation_rules,
        "submit": form_obj.submit_action,
        "success_message": form_obj.success_message,
        "failure_message": form_obj.failure_message
    })

@router.get("/models/{slug}")
async def get_published_model(slug: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ModelDefinition).filter(ModelDefinition.slug == slug, ModelDefinition.is_published == True))
    model_obj = result.scalar_one_or_none()
    
    if not model_obj:
        return error_response(message="Model definition not found or not published")
        
    return success_response(data={
        "id": str(model_obj.id),
        "name": model_obj.name,
        "slug": model_obj.slug,
        "label": model_obj.label,
        "description": model_obj.description,
        "fields": model_obj.fields,
        "version": model_obj.version
    })
