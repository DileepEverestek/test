import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from src.core.hashing import Hasher
from src.core.security import settings, create_access_token
from src.models import base
from src.models.models import User
from src.models.users import create_new_user
from src.schemas import schemas
from src.database.database import SessionLocal, engine
from src.schemas.schemas import create_new_user, user_login, Token

base.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#registration
@app.post("/")
def create_user(request : create_new_user,db: Session = Depends(get_db)):
    query1 = db.query(User).filter(User.email == request.email).first()
    if not query1:
        query = User(
            username= request.username,
            email=request.email,
            hashed_password=Hasher.get_password_hash(request.hashed_password)
        )
        db.add(query)
        db.commit()
        db.refresh(query)
        return {"Details": "Account Created"}

    else:
        return {"Details:" "Email already exists"}



#login
from sqlalchemy.orm import Session

from src.models.users import User


def get_user(username:str,db: Session):
    user = db.query(User).filter(User.email == username).first()
    return user

from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends,APIRouter
from sqlalchemy.orm import Session
from datetime import timedelta
from fastapi import status,HTTPException

router = APIRouter()

def authenticate_user(username: str, password: str,db: Session):
    user = get_user(username=username,db=db)
    print(user)
    if not user:
        return False
    if not Hasher.verify_password(password, user.hashed_password):
        return False
    return user


@app.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),db: Session= Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password,db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}




if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)