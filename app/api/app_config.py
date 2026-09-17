from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel
from typing import Dict, Any, Optional
from app.core.database import get_db
from app.models.app_config import AppConfig
from app.utils.response import success_response

router = APIRouter()

class AppConfigUpdate(BaseModel):
    schema_version: Optional[Dict[str, Any]] = None
    theme: Optional[Dict[str, Any]] = None
    navigation: Optional[Dict[str, Any]] = None

@router.get("/")
async def get_app_config(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(AppConfig).limit(1))
    config = result.scalar_one_or_none()
    if not config:
        config = AppConfig(
            schema_version={"version": 1},
            theme={"primary_color": "#2563eb", "dark_mode": False},
            navigation={}
        )
        db.add(config)
        await db.commit()
        await db.refresh(config)

    return success_response(data={
        "id": str(config.id),
        "schema_version": config.schema_version,
        "theme": config.theme,
        "navigation": config.navigation
    })

@router.put("/")
async def update_app_config(config_in: AppConfigUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(AppConfig).limit(1))
    config = result.scalar_one_or_none()
    if not config:
        config = AppConfig(
            schema_version=config_in.schema_version or {"version": 1},
            theme=config_in.theme or {},
            navigation=config_in.navigation or {}
        )
        db.add(config)
    else:
        if config_in.schema_version is not None:
            config.schema_version = config_in.schema_version
        if config_in.theme is not None:
            config.theme = config_in.theme
        if config_in.navigation is not None:
            config.navigation = config_in.navigation

    await db.commit()
    await db.refresh(config)
    return success_response(data={
        "id": str(config.id),
        "schema_version": config.schema_version,
        "theme": config.theme,
        "navigation": config.navigation
    })
