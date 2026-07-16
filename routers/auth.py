from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from auth_utils import create_access_token, verify_password
from database import get_db
from models import User
from schemas import LoginRequest, TokenResponse

router = APIRouter(tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Email atau password salah")

    token = create_access_token(user.email)
    return TokenResponse(access_token=token, user=user)
