from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.core.database import get_db
from app.models.page import Page
from app.schemas.page import PageCreate, PageUpdate, PageResponse
from app.utils.response import success_response, error_response
import uuid

router = APIRouter()

@router.get("/")
async def list_pages(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Page))
    pages = result.scalars().all()
    return success_response(data=[PageResponse.model_validate(p).model_dump() for p in pages])

@router.post("/")
async def create_page(page: PageCreate, db: AsyncSession = Depends(get_db)):
    db_page = Page(**page.model_dump())
    db.add(db_page)
    await db.commit()
    await db.refresh(db_page)
    return success_response(data=PageResponse.model_validate(db_page).model_dump())

@router.get("/{id}")
async def get_page(id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Page).filter(Page.id == id))
    page = result.scalar_one_or_none()
    if not page:
        return error_response(message="Page not found")
    return success_response(data=PageResponse.model_validate(page).model_dump())

@router.put("/{id}")
async def update_page(id: uuid.UUID, page_update: PageUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Page).filter(Page.id == id))
    page = result.scalar_one_or_none()
    if not page:
        return error_response(message="Page not found")
        
    for key, value in page_update.model_dump(exclude_unset=True).items():
        setattr(page, key, value)
    
    page.version += 1
    await db.commit()
    await db.refresh(page)
    return success_response(data=PageResponse.model_validate(page).model_dump())

@router.delete("/{id}")
async def delete_page(id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Page).filter(Page.id == id))
    page = result.scalar_one_or_none()
    if not page:
        return error_response(message="Page not found")
        
    await db.delete(page)
    await db.commit()
    return success_response(message="Page deleted")

@router.post("/{id}/publish")
async def publish_page(id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Page).filter(Page.id == id))
    page = result.scalar_one_or_none()
    if not page:
        return error_response(message="Page not found")
        
    page.is_published = True
    page.status = "published"
    await db.commit()
    await db.refresh(page)
    return success_response(data=PageResponse.model_validate(page).model_dump())

