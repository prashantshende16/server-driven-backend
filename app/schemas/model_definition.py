from pydantic import BaseModel, UUID4
from typing import Optional, List, Dict, Any
from datetime import datetime

class ModelDefinitionBase(BaseModel):
    name: str
    slug: str
    label: Optional[str] = None
    description: Optional[str] = None
    fields: List[Dict[str, Any]] = []
    is_published: bool = False

class ModelDefinitionCreate(ModelDefinitionBase):
    pass

class ModelDefinitionUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    label: Optional[str] = None
    description: Optional[str] = None
    fields: Optional[List[Dict[str, Any]]] = None
    is_published: Optional[bool] = None

class ModelDefinitionResponse(ModelDefinitionBase):
    id: UUID4
    version: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
