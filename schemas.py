from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    nama: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=128)


class UserUpdate(BaseModel):
    nama: str | None = Field(None, min_length=1, max_length=100)
    email: EmailStr | None = None
    password: str | None = Field(None, min_length=6, max_length=128)


class UserResponse(BaseModel):
    id: int
    nama: str
    email: EmailStr

    model_config = {"from_attributes": True}


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1, max_length=128)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
