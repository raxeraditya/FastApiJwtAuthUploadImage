from sqlalchemy import Column, Integer, String
from dependencies.database import Base
from sqlalchemy.orm import relationship
# In your User model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(128))
    posts = relationship("Post", back_populates="owner")