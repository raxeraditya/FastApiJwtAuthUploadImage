from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from schemas.user_schema import UserResponse

class PostBase(BaseModel):
    caption: Optional[str] = None

class PostCreate(PostBase):
    image: str  # This will be the file path after upload

class PostResponse(BaseModel):
    id:int
    caption: str
    image_url: str  # This will contain the file path or URL
    user_id: int

    class Config:
        from_attribute=True