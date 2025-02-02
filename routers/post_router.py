from fastapi import APIRouter, Depends, File, Form, Request, UploadFile, status
from sqlalchemy.orm import Session
from dependencies.database import get_db
from schemas.post_schema import PostResponse
from services.post_service import PostService

router = APIRouter(prefix="/posts", tags=["posts"])

@router.post("/create", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def register_post(
    request:Request,
    caption: str = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    return PostService.create_post(
        db=db,
        user_id=request.state.user.id,
        caption=caption,
        image=image
    )