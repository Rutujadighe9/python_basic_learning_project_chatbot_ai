from sqlalchemy.orm import Session

from app.schemas.auth_schema import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    UserResponse,
)
from app.services.auth_service import (
    authenticate_user,
    create_access_token,
    register_user,
)


def register(payload: RegisterRequest, db: Session) -> UserResponse:
    user = register_user(payload, db)
    return UserResponse(id=user.id, name=user.name, email=user.email)


def login(payload: LoginRequest, db: Session) -> LoginResponse:
    user = authenticate_user(payload, db)
    return LoginResponse(
        message="login user sucessfully",
        access_token=create_access_token(user.id),
        token_type="bearer",
    )
    

