from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from app.core.sqlalchemy_connection import get_db
from app.db.models.user import User
from app.schemas.user.user_profile import UserProfileResponse, UserProfileUpdate
from app.utils.user_utils import get_current_user

user_profile_router = APIRouter()


@user_profile_router.get("/profile", response_model=UserProfileResponse)
def get_user_profile(current_user: User = Depends(get_current_user)):
    """
    Retrieve the profile of the currently authenticated user.
    """
    user_data = UserProfileResponse(
        id=str(current_user.id),  # Convert UUID to string here
        username=current_user.username,
        email=current_user.email
    )

    response_data = {
        "succeeded": True,
        "status_code": 200,
        "message": "User profile retrieved successfully.",
        "data": user_data.dict()
    }

    return JSONResponse(content=response_data, status_code=200)

@user_profile_router.put("/profile", response_model=UserProfileResponse)
def update_user_profile(
        profile_data: UserProfileUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    """
    Update user profile.
    """
    if profile_data.username:
        existing_user = db.query(User).filter(User.username == profile_data.username).first()
        if existing_user and existing_user.id != current_user.id:
            return JSONResponse(
                content={
                    "succeeded": False,
                    "status_code": 400,
                    "message": "Username already taken",
                },
                status_code=400
            )

    current_user.username = profile_data.username or current_user.username
    current_user.email = profile_data.email or current_user.email

    db.commit()
    db.refresh(current_user)
    user_data = UserProfileResponse(
        id=str(current_user.id),  # Convert UUID to string here
        username=current_user.username,
        email=current_user.email
    )
    response_data = {
        "data": user_data.dict()
    }


    return JSONResponse(content=response_data, status_code=200)
