from .. import models , schemas , utils, oauth2
from fastapi import FastAPI , Response, status, HTTPException, Depends, APIRouter
from  sqlalchemy.orm import Session
from ..database import engine , get_db

router = APIRouter(prefix='/users',tags = ['Users'])

@router.post("/" , status_code= status.HTTP_201_CREATED, response_model= schemas.UserOut) 
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)): # --> data avlidation is handled by pydantic

# Hash password
    # hashed_password = pwd_context.hash(user.password)
    # hashed_password = sha256_crypt.hash(user.password)

    hashed_password = utils.hash(user.password)
    user.password = hashed_password

# Add new user
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user) # refresh to see the bran new user

    return new_user

@router.get('/{id}', response_model= schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail=f"User id {id} not found ")
    else:
        return user

