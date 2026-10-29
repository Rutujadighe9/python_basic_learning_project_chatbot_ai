import hashlib
import hmac
import secrets
from datetime import datetime, timedelta, timezone
from uuid import UUID

from fastapi import HTTPException, status
import jwt
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.user import User
from app.repositories.user_repository import create_user, get_user_by_email
from app.schemas.auth_schema import LoginRequest, RegisterRequest

_HASH_ITERATIONS = 600_000
_ACCESS_TOKEN_LIFETIME = timedelta(minutes=30)


def _hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        _HASH_ITERATIONS,
    )
    return f"pbkdf2_sha256${_HASH_ITERATIONS}${salt.hex()}${password_hash.hex()}"


def _verify_password(password: str, encoded_hash: str) -> bool:
    algorithm, iterations, salt_hex, expected_hash = encoded_hash.split("$")
    if algorithm != "pbkdf2_sha256":
        raise ValueError("Unsupported password hash algorithm")

    actual_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        bytes.fromhex(salt_hex),
        int(iterations),
    )
    return hmac.compare_digest(actual_hash.hex(), expected_hash)


def authenticate_user(payload: LoginRequest, db: Session) -> User:
    user = get_user_by_email(db, payload.email)
    if user is None or not _verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def create_access_token(user_id: UUID) -> str:
    now = datetime.now(timezone.utc)
    return jwt.encode(
        {"sub": str(user_id), "iat": now, "exp": now + _ACCESS_TOKEN_LIFETIME},
        settings.JWT_SECRET_KEY,
        algorithm="HS256",
    )


def register_user(payload: RegisterRequest, db: Session) -> User:
    email = payload.email.lower()
    if get_user_by_email(db, email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists",
        )

    try:
        return create_user(
            db,
            name=payload.name.strip(),
            email=email,
            password_hash=_hash_password(payload.password),
        )
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists",
        ) from None