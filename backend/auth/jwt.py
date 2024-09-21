from datetime import datetime, timedelta, timezone
from typing import Annotated, Any

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import InvalidTokenError

SECRET_KEY = "secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 8

USER_ID = "user_id"

security = HTTPBearer()


def get_user_id(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> int:
    token = credentials.credentials
    try:
        claimes = verify_token(token)
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return claimes[USER_ID]


def verify_token(token: str) -> dict:
    claimes = jwt.decode(
        token, SECRET_KEY, algorithms=[ALGORITHM], requires=["exp", USER_ID]
    )
    return claimes


def create_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    claimes: dict[str, Any] = {
        "exp": expire,
        USER_ID: user_id,
    }
    token = jwt.encode(claimes, SECRET_KEY, algorithm=ALGORITHM)
    return token
