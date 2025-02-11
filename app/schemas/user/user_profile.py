from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID
class UserProfileResponse(BaseModel):
    id: UUID
    username: Optional[str] = None
    email: EmailStr

    class Config:
        from_attributes = True


class UserProfileUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
