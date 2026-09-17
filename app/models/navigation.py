from sqlalchemy import Column, String, JSON, Integer, Boolean
from app.models.base import BaseModel

class Navigation(BaseModel):
    __tablename__ = "navigations"
    name = Column(String, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)
    nav_type = Column(String, default="bottom_tabs")  # bottom_tabs, drawer, stack, menu
    items = Column(JSON, default=list)
    is_active = Column(Boolean, default=False)
    version = Column(Integer, default=1)

