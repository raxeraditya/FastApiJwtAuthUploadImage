from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from starlette.status import HTTP_401_UNAUTHORIZED
from jose import JWTError, jwt
from dependencies.database import get_db, engine, Base
from services.user_service import get_user_by_username
from core.config import settings
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles
from routers import user_router, post_router
from exceptions.handler import add_exception_handlers

Base.metadata.create_all(bind=engine)

app = FastAPI()
add_exception_handlers(app)

# Mount static files and include routers
app.mount("/static", StaticFiles(directory="uploads"), name="static")
app.include_router(user_router.router)
app.include_router(post_router.router)

# Updated EXCLUDED_ROUTES without the root route "/"
EXCLUDED_ROUTES = ["/api/users/login", "/api/users/register","/docs","openapi.json"]

@app.middleware("http")
async def authentication_middleware(request: Request, call_next):
    # Exclude specified routes using an exact match or startswith for other paths
    if any(request.url.path.startswith(route) for route in EXCLUDED_ROUTES):
        return await call_next(request)
    
    # Prepare a custom JSON response for authentication errors
    custom_error_response = JSONResponse(
        status_code=HTTP_401_UNAUTHORIZED,
        content={"detail": "Custom Error: You must be authenticated to access this resource. Please log in."}
    )

    # Get the Authorization header
    authorization_header = request.headers.get("Authorization")
    if not authorization_header or not authorization_header.startswith("Bearer "):
        return custom_error_response

    token = authorization_header.split(" ")[1]
    try:
        # Decode the token
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return custom_error_response

        # Retrieve a DB session and verify the user exists
        db: Session = next(get_db())
        user = get_user_by_username(db=db, username=username)
        if user is None:
            return custom_error_response

        # Store the authenticated user in request.state for later use
        request.state.user = user

    except JWTError:
        return custom_error_response

    # Continue processing the request
    response = await call_next(request)
    return response

@app.get("/", tags=["Home"])
async def read_home():
    """
    Home route that is accessible to everyone.
    """
    return {"message": "Welcome to the home page! This route is open to everyone."}
