from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import get_db
from app.models.form import Form
from app.schemas.form import FormCreate, FormUpdate, FormResponse
from app.utils.response import success_response, error_response
import uuid

router = APIRouter()

@router.get("/")
async def list_forms(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Form))
    forms = result.scalars().all()
    return success_response(data=[FormResponse.model_validate(f).model_dump() for f in forms])

@router.post("/")
async def create_form(form_in: FormCreate, db: AsyncSession = Depends(get_db)):
    # Check if slug exists
    existing = await db.execute(select(Form).filter(Form.slug == form_in.slug))
    if existing.scalar_one_or_none():
        return error_response(message="Form with this slug already exists")

    db_form = Form(**form_in.model_dump())
    db.add(db_form)
    await db.commit()
    await db.refresh(db_form)
    return success_response(data=FormResponse.model_validate(db_form).model_dump())

@router.get("/{id}")
async def get_form(id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Form).filter(Form.id == id))
    form_obj = result.scalar_one_or_none()
    if not form_obj:
        return error_response(message="Form not found")
    return success_response(data=FormResponse.model_validate(form_obj).model_dump())

@router.put("/{id}")
async def update_form(id: uuid.UUID, form_update: FormUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Form).filter(Form.id == id))
    form_obj = result.scalar_one_or_none()
    if not form_obj:
        return error_response(message="Form not found")

    for key, value in form_update.model_dump(exclude_unset=True).items():
        setattr(form_obj, key, value)

    form_obj.version += 1
    await db.commit()
    await db.refresh(form_obj)
    return success_response(data=FormResponse.model_validate(form_obj).model_dump())

@router.delete("/{id}")
async def delete_form(id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Form).filter(Form.id == id))
    form_obj = result.scalar_one_or_none()
    if not form_obj:
        return error_response(message="Form not found")

    await db.delete(form_obj)
    await db.commit()
    return success_response(message="Form deleted")

@router.post("/{id}/publish")
async def publish_form(id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Form).filter(Form.id == id))
    form_obj = result.scalar_one_or_none()
    if not form_obj:
        return error_response(message="Form not found")

    form_obj.is_published = True
    await db.commit()
    await db.refresh(form_obj)
    return success_response(data=FormResponse.model_validate(form_obj).model_dump())
