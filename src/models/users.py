from src.core.hashing import Hasher
from src.models.models import User
from src.schemas.schemas import UserCreate
from sqlalchemy.orm import Session



def create_new_user(user: UserCreate, db: Session):
    user = User(
        username=user.username,
        email=user.email,
        hashed_password=bytes(user.password,'ascii'),
        is_active=True,
        is_superuser=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_email(email: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    return user
