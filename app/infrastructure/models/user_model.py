from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    public_id = Column(String(64), unique=True, nullable=False, index=True)

    name = Column(String(64), nullable= False)
    email = Column(String(255), unique=True, nullable= False, index=True)
    password = Column(String(256), nullable=False)

    sessions = relationship(
        "SessionModel",
        back_populates="user",
        cascade="all, delete-orphan"
    )
