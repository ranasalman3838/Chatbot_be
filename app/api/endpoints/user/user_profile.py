from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from app.core.sqlalchemy_connection import get_db
from app.db.models.user import User
from app.schemas.user.user_profile import UserProfileUpdate, UserProfileResponse
from app.utils.user_utils import get_current_user

user_profile_router = APIRouter()


@user_profile_router.get("/profile", response_model=UserProfileResponse)
def get_user_profile(current_user: User = Depends(get_current_user)):
    """
    Retrieve the profile of the currently authenticated user.
    """
    return current_user


@user_profile_router.put("/profile", response_model=UserProfileResponse)
def update_user_profile(
        profile_data: UserProfileUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    """
    Update the profile of the currently authenticated user.
    """
    if profile_data.username:
        existing_user = db.query(User).filter(User.username == profile_data.username).first()
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken",
            )

    current_user.username = profile_data.username or current_user.username
    current_user.email = profile_data.email or current_user.email

    db.commit()
    db.refresh(current_user)

    return current_user
