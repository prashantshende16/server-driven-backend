from sqlalchemy import Column, String, Integer, Boolean, JSON
from app.models.base import BaseModel

class Page(BaseModel):
    __tablename__ = "pages"
    name = Column(String, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)
    title = Column(String)
    description = Column(String)
    route = Column(String)
    layout_type = Column(String)
    status = Column(String, default="draft") # draft, published, archived
    version = Column(Integer, default=1)
    is_published = Column(Boolean, default=False)
    components = Column(JSON, default=list) # Array of component configs

