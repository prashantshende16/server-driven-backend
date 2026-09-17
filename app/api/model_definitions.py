from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import get_db
from app.models.model_definition import ModelDefinition
from app.schemas.model_definition import ModelDefinitionCreate, ModelDefinitionUpdate, ModelDefinitionResponse
from app.utils.response import success_response, error_response
import uuid

router = APIRouter()

@router.get("/")
async def list_model_definitions(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ModelDefinition))
    models = result.scalars().all()
    return success_response(data=[ModelDefinitionResponse.model_validate(m).model_dump() for m in models])

@router.post("/")
async def create_model_definition(model_in: ModelDefinitionCreate, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(select(ModelDefinition).filter(ModelDefinition.slug == model_in.slug))
    if existing.scalar_one_or_none():
        return error_response(message="Model with this slug already exists")

    db_model = ModelDefinition(**model_in.model_dump())
    db.add(db_model)
    await db.commit()
    await db.refresh(db_model)
    return success_response(data=ModelDefinitionResponse.model_validate(db_model).model_dump())

@router.get("/{id}")
async def get_model_definition(id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ModelDefinition).filter(ModelDefinition.id == id))
    model_obj = result.scalar_one_or_none()
    if not model_obj:
        return error_response(message="Model definition not found")
    return success_response(data=ModelDefinitionResponse.model_validate(model_obj).model_dump())

@router.put("/{id}")
async def update_model_definition(id: uuid.UUID, model_update: ModelDefinitionUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ModelDefinition).filter(ModelDefinition.id == id))
    model_obj = result.scalar_one_or_none()
    if not model_obj:
        return error_response(message="Model definition not found")

    for key, value in model_update.model_dump(exclude_unset=True).items():
        setattr(model_obj, key, value)

    model_obj.version += 1
    await db.commit()
    await db.refresh(model_obj)
    return success_response(data=ModelDefinitionResponse.model_validate(model_obj).model_dump())

@router.delete("/{id}")
async def delete_model_definition(id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ModelDefinition).filter(ModelDefinition.id == id))
    model_obj = result.scalar_one_or_none()
    if not model_obj:
        return error_response(message="Model definition not found")

    await db.delete(model_obj)
    await db.commit()
    return success_response(message="Model definition deleted")

@router.post("/{id}/publish")
async def publish_model_definition(id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ModelDefinition).filter(ModelDefinition.id == id))
    model_obj = result.scalar_one_or_none()
    if not model_obj:
        return error_response(message="Model definition not found")

    model_obj.is_published = True
    await db.commit()
    await db.refresh(model_obj)
    return success_response(data=ModelDefinitionResponse.model_validate(model_obj).model_dump())
