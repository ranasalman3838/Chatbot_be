from pydantic import BaseModel, EmailStr
from typing import Optional



class UserProfileResponse(BaseModel):
    id: str  # Convert UUID to string
    username: Optional[str] = None
    email: EmailStr

    class Config:
        from_attributes = True

class UserProfileUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
