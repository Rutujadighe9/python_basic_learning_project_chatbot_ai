from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.controllers.auth_controller import login, register
from app.core.database import get_db
from app.schemas.auth_schema import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    UserResponse,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(payload: RegisterRequest, db: Session = Depends(get_db)):
    return register(payload, db)


@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
)
def login_user(payload: LoginRequest, db: Session = Depends(get_db)) -> LoginResponse:
    return login(payload, db)


# @router.put("/forgot",
#       response_model=
#       status_code= status.HTTP_200_OK,    
#             )
# def forgot_password(payload:forgot_password,db:Session =Depends(get_db))-> forgotResponse:
#     return forgot_password(payload)