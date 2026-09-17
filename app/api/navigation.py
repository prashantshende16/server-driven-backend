from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import get_db
from app.models.navigation import Navigation
from app.schemas.navigation import NavigationCreate, NavigationUpdate, NavigationResponse
from app.utils.response import success_response, error_response
import uuid

router = APIRouter()

@router.get("/")
async def list_navigations(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Navigation))
    navs = result.scalars().all()
    return success_response(data=[NavigationResponse.model_validate(n).model_dump() for n in navs])

@router.post("/")
async def create_navigation(nav_in: NavigationCreate, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(select(Navigation).filter(Navigation.slug == nav_in.slug))
    if existing.scalar_one_or_none():
        return error_response(message="Navigation with this slug already exists")

    if nav_in.is_active:
        # Deactivate all others of this type if making this one active
        all_navs = await db.execute(select(Navigation).filter(Navigation.nav_type == nav_in.nav_type))
        for n in all_navs.scalars().all():
            n.is_active = False

    db_nav = Navigation(**nav_in.model_dump())
    db.add(db_nav)
    await db.commit()
    await db.refresh(db_nav)
    return success_response(data=NavigationResponse.model_validate(db_nav).model_dump())

@router.get("/{id}")
async def get_navigation(id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Navigation).filter(Navigation.id == id))
    nav_obj = result.scalar_one_or_none()
    if not nav_obj:
        return error_response(message="Navigation not found")
    return success_response(data=NavigationResponse.model_validate(nav_obj).model_dump())

@router.put("/{id}")
async def update_navigation(id: uuid.UUID, nav_update: NavigationUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Navigation).filter(Navigation.id == id))
    nav_obj = result.scalar_one_or_none()
    if not nav_obj:
        return error_response(message="Navigation not found")

    update_dict = nav_update.model_dump(exclude_unset=True)
    if update_dict.get("is_active"):
        nav_type = update_dict.get("nav_type") or nav_obj.nav_type
        all_navs = await db.execute(select(Navigation).filter(Navigation.nav_type == nav_type, Navigation.id != id))
        for n in all_navs.scalars().all():
            n.is_active = False

    for key, value in update_dict.items():
        setattr(nav_obj, key, value)

    nav_obj.version += 1
    await db.commit()
    await db.refresh(nav_obj)
    return success_response(data=NavigationResponse.model_validate(nav_obj).model_dump())

@router.delete("/{id}")
async def delete_navigation(id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Navigation).filter(Navigation.id == id))
    nav_obj = result.scalar_one_or_none()
    if not nav_obj:
        return error_response(message="Navigation not found")

    await db.delete(nav_obj)
    await db.commit()
    return success_response(message="Navigation deleted")

@router.post("/{id}/activate")
async def activate_navigation(id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Navigation).filter(Navigation.id == id))
    nav_obj = result.scalar_one_or_none()
    if not nav_obj:
        return error_response(message="Navigation not found")

    all_navs = await db.execute(select(Navigation).filter(Navigation.nav_type == nav_obj.nav_type))
    for n in all_navs.scalars().all():
        n.is_active = False

    nav_obj.is_active = True
    await db.commit()
    await db.refresh(nav_obj)
    return success_response(data=NavigationResponse.model_validate(nav_obj).model_dump())
