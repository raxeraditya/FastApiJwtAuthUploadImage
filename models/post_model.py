from sqlalchemy import Column, Integer, String, ForeignKey
from dependencies.database import Base
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    caption = Column(String, nullable=False)
    image_path = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))  # Foreign key linking to User table

    # Define relationship
    owner = relationship("User", back_populates="posts")