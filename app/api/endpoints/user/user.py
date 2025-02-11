from fastapi import Depends, HTTPException, status, APIRouter
from datetime import timedelta
from app.core.sqlalchemy_connection import SessionLocal, get_db
from app.db.models.user import User
from app.schemas.user.user_schema import LoginData, SignupData, Token
from app.utils.user_utils import (
    authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token,
    get_user, get_password_hash
)
from fastapi.responses import JSONResponse

auth_router = APIRouter()


@auth_router.post("/login", response_model=Token)
def login_for_access_token(login_data: LoginData, db: SessionLocal = Depends(get_db)):
    user = authenticate_user(db, login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)

    response_data = {
        "succeeded": True,
        "status_code": 200,
        "message": "Login successful.",
        "data": {"access_token": access_token, "token_type": "bearer"}
    }
    return JSONResponse(content=response_data, status_code=200)


@auth_router.post("/signup")
def signup_user(signup_data: SignupData, db: SessionLocal = Depends(get_db)):
    # Check if username already exists
    existing_user = get_user(db, signup_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already taken"
        )

    # Hash the password and create a new user
    hashed_password = get_password_hash(signup_data.password)
    new_user = User(email=signup_data.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    response_data = {
        "succeeded": True,
        "status_code": 201,
        "message": "User registered successfully.",
        "data": {"id": str(new_user.id), "email": new_user.email}
    }
    return JSONResponse(content=response_data, status_code=201)


@auth_router.post("/logout")
def logout():
    """
    Informs the client that logout is successful. The client should remove the token.
    """
    response_data = {
        "succeeded": True,
        "status_code": 200,
        "message": "Logged out successfully.",
        "data": None
    }
    return JSONResponse(content=response_data, status_code=200)
