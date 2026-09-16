from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import get_db
from app.core.security import verify_password, create_access_token, get_password_hash
from app.models.user import User

router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login")
async def login(req: LoginRequest, db: AsyncSession = Depends(get_db)):
    # simple mock for creation if empty for testing
    result = await db.execute(select(User).filter(User.email == req.email))
    user = result.scalar_one_or_none()
    
    if not user:
        # Auto-create super admin for dev purposes if no users exist
        count = await db.execute(select(User))
        if len(count.scalars().all()) == 0:
            user = User(email=req.email, hashed_password=get_password_hash(req.password), role="super_admin")
            db.add(user)
            await db.commit()
            await db.refresh(user)
        else:
            raise HTTPException(status_code=400, detail="Incorrect email or password")
            
    if not verify_password(req.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
        
    access_token = create_access_token(data={"sub": user.email, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}

