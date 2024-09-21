from typing import Annotated

from fastapi import Body, Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

import crud
from auth import jwt
from DB import db

app = FastAPI()


@app.get("/welcome")
async def welcom() -> dict:
    return {"message": "welcome"}


# auth
@app.post("/register")
def register(
    name: Annotated[str, Body()],
    password: Annotated[str, Body()],
    db: Session = Depends(db.get_session),
) -> dict:
    db_user = crud.create_user(db, name, password)
    if db_user is None:
        raise HTTPException(
            status_code=400, detail="メールアドレスが既に登録されています"
        )
    token = jwt.create_token(db_user.id)
    return {"token": token, "user_id": db_user.id}


@app.post("/login")
def login(
    name: Annotated[str, Body()],
    password: Annotated[str, Body()],
    db: Session = Depends(db.get_session),
) -> dict:
    db_user = crud.verify_user(db, name, password)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="名前かパスワードが間違っています",
        )
    token = jwt.create_token(db_user.id)
    return {"token": token, "user_id": db_user.id}
