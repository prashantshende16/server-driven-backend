from pydantic import BaseModel, UUID4
from typing import Optional, List, Dict, Any
from datetime import datetime

class PageBase(BaseModel):
    name: str
    slug: str
    title: Optional[str] = None
    description: Optional[str] = None
    route: Optional[str] = None
    layout_type: Optional[str] = None
    status: str = "draft"
    is_published: bool = False
    components: List[Dict[str, Any]] = []

class PageCreate(PageBase):
    pass

class PageUpdate(PageBase):
    name: Optional[str] = None
    slug: Optional[str] = None
    status: Optional[str] = None
    is_published: Optional[bool] = None

class PageResponse(PageBase):
    id: UUID4
    version: int
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

