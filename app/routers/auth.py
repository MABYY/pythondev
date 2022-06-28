from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from .. import database ,schemas, models, utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(prefix='/auth', tags=['Authentication'])


@router.post('/login', response_model=schemas.Token)
# def login_user(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):
def login_user(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
 
#    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
#    username --> email

    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()

    print('user', user)

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                                detail=f"Invalid credentials ")
                                
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                                detail=f"Invalid credentials ")

    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}

