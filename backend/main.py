import os
from typing import Annotated

from fastapi import (
    Body,
    Depends,
    FastAPI,
    File,
    Form,
    HTTPException,
    Query,
    UploadFile,
    status,
)
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

import crud
from auth import jwt
from DB import db
from load_env import IMG_PATH

app = FastAPI()

if not os.path.exists(str(IMG_PATH)):
    os.mkdir(str(IMG_PATH))


@app.get("/welcome")
async def welcom() -> dict:
    return {"message": "welcome"}


# auth
@app.post("/register", tags=["auth"])
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


@app.post("/login", tags=["auth"])
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
@app.post("/mindmaps", tags=["mindmap"])
def create_mindmap(
    title: Annotated[str, Body()],
    description: Annotated[str, Body()],
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


@app.get("/mindmaps", tags=["mindmap"])
def get_mindmaps(
    skip: int = 0, limit: int = 100, db: Session = Depends(db.get_session)
):
    return crud.get_mindmaps(db, skip, limit)


@app.get("/mindmaps/{mindmap_id}", tags=["mindmap"])
def get_mindmap(mindmap_id: int, db: Session = Depends(db.get_session)):
    db_mindmap = crud.get_mindmap(db, mindmap_id)
    if db_mindmap is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="マインドマップが見つかりません",
        )
    return db_mindmap


@app.put("/mindmaps", tags=["mindmap"])
def update_mindmap(
    mindmap_id: int,
    title: Annotated[str | None, Body()] = None,
    description: Annotated[str | None, Body()] = None,
    user_id: int = Depends(jwt.get_user_id),
    db: Session = Depends(db.get_session),
):
    db_mindmap = crud.update_mindmap(db, mindmap_id, user_id, title, description)
    if db_mindmap is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="アクセス権がありません"
        )
    return db_mindmap


# project
@app.post("/projects", tags=["project"])
def create_project(
    title: Annotated[str, Form()],
    mindmap_id: Annotated[int, Form()],
    description: Annotated[str, Form()],
    images: Annotated[list[UploadFile], File()],
    user_id: int = Depends(jwt.get_user_id),
    db: Session = Depends(db.get_session),
):
    db_project = crud.create_project(
        db, user_id, mindmap_id, title, description, images
    )
    return {"info": db_project, "img": len(images)}


@app.get("/projects", tags=["project"])
def read_projects(
    skip: int = 0,
    limit: int = 100,
    mindmap_id: Annotated[int | None, Query(description="mindmap id")] = None,
    db: Session = Depends(db.get_session),
):
    if mindmap_id is None:
        projects = crud.get_projects(db, skip=skip, limit=limit)
    else:
        projects = crud.get_projects_by_mindmap_id(
            db, skip=skip, limit=limit, mindmap_id=mindmap_id
        )
    return projects


@app.get("/projects/{project_id}", tags=["project"])
def get_project(project_id: int, db: Session = Depends(db.get_session)):
    db_project = crud.get_project(db, project_id)
    if db_project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="マインドマップが見つかりません",
        )
    return db_project


@app.get("/projects/image/{image_id}", tags=["project"])
def get_project_image(image_id: str, db: Session = Depends(db.get_session)):
    path = crud.get_project_image_path(db, image_id)
    if path is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="画像が見つかりません"
        )
    return FileResponse(path)


@app.post("/projects/{project_id}/comments", tags=["project"])
def post_comment(
    project_id: int,
    body: str,
    user_id: int = Depends(jwt.get_user_id),
    db: Session = Depends(db.get_session),
):
    crud.post_comment(db, project_id, user_id, body)


@app.put("/projects", tags=["project"])
def update_project(
    project_id: Annotated[int, Body()],
    title: Annotated[str | None, Body()] = None,
    description: Annotated[str | None, Body()] = None,
    user_id: int = Depends(jwt.get_user_id),
    db: Session = Depends(db.get_session),
):
    db_project = crud.update_project(db, project_id, user_id, title, description)
    if db_project is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="アクセス権がありません"
        )
    return db_project
