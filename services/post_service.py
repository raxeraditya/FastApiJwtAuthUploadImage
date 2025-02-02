import os
import uuid
from fastapi import HTTPException, UploadFile, status
from pathlib import Path
from sqlalchemy.orm import Session
from models.post_model import Post
from schemas.post_schema import PostResponse

class PostService:
    @staticmethod
    def create_post(
        db: Session, 
        user_id: int, 
        caption: str, 
        image: UploadFile,
        upload_dir: Path = Path("uploads")
    ) -> PostResponse:
        # Validate and process image only once
        try:
            # Validate image type
            allowed_types = ["image/jpeg", "image/png"]
            if image.content_type not in allowed_types:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only JPEG and PNG images are allowed"
                )

            # Generate unique filename
            file_ext = os.path.splitext(image.filename)[1]
            filename = f"{uuid.uuid4()}{file_ext}"
            file_path = upload_dir / filename

            # Single file save operation
            with open(file_path, "wb") as buffer:
                buffer.write(image.file.read())

            # Create database record
            db_post = Post(
                caption=caption,
                image_path=str(filename),  # Store only filename
                owner_id=user_id
            )

            db.add(db_post)
            db.commit()
            db.refresh(db_post)

            return PostResponse(
                id=db_post.id,
                caption=db_post.caption,
                image_url=f"/static/{filename}",  # URL path
                user_id=user_id  # Assuming relationship is set up
            )

        except Exception as e:
            # Cleanup file if any error occurs
            if file_path.exists():
                os.remove(file_path)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )