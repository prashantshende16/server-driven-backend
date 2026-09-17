from pydantic import BaseModel, UUID4
from typing import Optional, List, Dict, Any
from datetime import datetime

class NavigationBase(BaseModel):
    name: str
    slug: str
    nav_type: str = "bottom_tabs"
    items: List[Dict[str, Any]] = []
    is_active: bool = False

class NavigationCreate(NavigationBase):
    pass

class NavigationUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    nav_type: Optional[str] = None
    items: Optional[List[Dict[str, Any]]] = None
    is_active: Optional[bool] = None

class NavigationResponse(NavigationBase):
    id: UUID4
    version: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
