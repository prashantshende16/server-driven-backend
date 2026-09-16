from pydantic import BaseModel, UUID4
from typing import Optional, List, Dict, Any
from datetime import datetime

class FormBase(BaseModel):
    name: str
    slug: str
    title: Optional[str] = None
    description: Optional[str] = None
    fields: List[Dict[str, Any]] = []
    validation_rules: Dict[str, Any] = {}
    submit_action: Dict[str, Any] = {}
    success_message: Optional[str] = None
    failure_message: Optional[str] = None

class FormCreate(FormBase):
    pass

class FormUpdate(FormBase):
    name: Optional[str] = None
    slug: Optional[str] = None

class FormResponse(FormBase):
    id: UUID4
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

