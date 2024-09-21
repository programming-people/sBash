from typing import Annotated

from fastapi import Body, Depends, FastAPI, HTTPException, status
from pydantic import HttpUrl
from sqlalchemy.orm import Session, raiseload

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


# mindmap
@app.post("/mindmaps")
def create_mindmap(
    title: Annotated[str, Body],
    description: Annotated[str, Body],
    user_id: int = Depends(jwt.get_user_id),
    db: Session = Depends(db.get_session),
):
    db_mindmap = crud.create_mindmap(db, title, description, user_id)
    if db_mindmap is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="少ししてから試してください",
        )
    return db_mindmap


@app.get("/mindmaps")
def get_mindmaps(
    skip: int = 0, limit: int = 100, db: Session = Depends(db.get_session)
):
    return crud.get_mindmaps(db, skip, limit)


@app.get("/mindmaps/{mindmap_id}")
def get_mindmap(mindmap_id: int, db: Session = Depends(db.get_session)):
    db_mindmap = crud.get_mindmap(db, mindmap_id)
    if db_mindmap is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="マインドマップが見つかりません",
        )
    return db_mindmap


@app.put("/mindmaps")
def update_mindmap(
    mindmap_id: int,
    title: Annotated[str | None, Body] = None,
    description: Annotated[str | None, Body] = None,
    user_id: int = Depends(jwt.get_user_id),
    db: Session = Depends(db.get_session),
):
    db_mindmap = crud.update_mindmap(db, mindmap_id, user_id, title, description)
    if db_mindmap is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="アクセス権がありません"
        )
    return db_mindmap
