import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from src.crud import crud
from src.models import base
from src.models.users import create_new_user
from src.schemas import schemas
from src.database.database import SessionLocal, engine
from src.schemas.schemas import UserCreate

base.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/")
def create_user(user : UserCreate,db: Session = Depends(get_db)):
    user = create_new_user(user=user,db=db)
    return user





if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)