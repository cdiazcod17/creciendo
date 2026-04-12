from fastapi import APIRouter,HTTPException,status,Depends
from app.schemas.users import UserRead
from app.db.session import get_db
from app.models.user import User
from app.schemas.users import UserRegister
from sqlalchemy.orm import Session
from app.core.security import get_password_hash

router = APIRouter()


@router.post("/register",response_model = UserRead,status_code = status.HTTP_201_CREATED)
def register(payload: UserRegister, db: Session = Depends(get_db)):
    user =db.query(User).filter(User.email == payload.email).first()
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    new_user = User(full_name=payload.full_name,email=payload.email,hashed_password=get_password_hash(payload.password))
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user