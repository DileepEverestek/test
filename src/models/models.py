from sqlalchemy import Column,Integer, String,Boolean, ForeignKey
from sqlalchemy.types import LargeBinary
from sqlalchemy.orm import relationship

from src.models.base_class import Base


class User(Base):
    id = Column(Integer,primary_key=True,index=True)
    username = Column(String(30),unique=True,nullable=False)
    email = Column(String(30),nullable=False,unique=True,index=True)
    hashed_password = Column(LargeBinary(200),nullable=False)
    is_active = Column(Boolean(),default=True)
    is_superuser = Column(Boolean(),default=False)
