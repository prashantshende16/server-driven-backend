from sqlalchemy import Column, String, JSON
from app.models.base import BaseModel

class Form(BaseModel):
    __tablename__ = "forms"
    name = Column(String, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)
    title = Column(String)
    description = Column(String)
    fields = Column(JSON, default=list)
    validation_rules = Column(JSON, default=dict)
    submit_action = Column(JSON, default=dict)
    success_message = Column(String)
    failure_message = Column(String)

