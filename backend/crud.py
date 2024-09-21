import os
import shutil
import uuid
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

import models
from auth.password import get_password_hash, verify_password
from load_env import IMG_PATH


# auth
def create_user(db: Session, name: str, password: str):
    hashed_password = get_password_hash(password)
    db_user = models.User(name=name, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def verify_user(db: Session, name: str, password: str) -> models.User | None:
    try:
        user = db.scalars(select(models.User).where(models.User.name == name)).one()
    except:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user


# mindmap
def create_mindmap(
    db: Session, title: str, description: str, user_id: int
) -> models.Mindmap | None:
    db_mindmap = models.Mindmap(user_id=user_id, title=title, description=description)
    db.add(db_mindmap)
    db.commit()
    db.refresh(db_mindmap)
    return db_mindmap


def get_mindmaps(
    db: Session,
    skip: int = 0,
    limit: int = 100,
) -> Sequence[models.Mindmap]:
    mindmaps = db.scalars(select(models.Mindmap).offset(skip).limit(limit)).all()
    return mindmaps


def get_mindmap(
    db: Session,
    mindmap_id: int,
) -> models.Mindmap | None:
    db_mindmap = db.scalars(
        select(models.Mindmap).where(models.Mindmap.id == mindmap_id)
    ).one_or_none()
    return db_mindmap


def update_mindmap(
    db: Session,
    mindmap_id: int,
    user_id: int,
    title: str | None,
    description: str | None,
) -> models.Mindmap | None:
    db_mindmap = get_mindmap(db, mindmap_id)
    if db_mindmap is None:
        return None
    if db_mindmap.user_id != user_id:
        return None

    if title:
        db_mindmap.title = title
    if description:
        db_mindmap.description = description
    db.commit()
    db.refresh(db_mindmap)
    return db_mindmap


# projects
def create_project(
    db: Session,
    user_id: int,
    mindmap_id: int,
    title: str,
    description: str,
    images: list,
) -> models.Project:
    uuids: list[uuid.UUID] = [uuid.uuid4() for _ in range(len(images))]
    exts: list[str] = [(os.path.splitext(image.filename))[1] for image in images]
    for uuid_, image, ext in zip(uuids, images, exts):
        id: str = str(uuid_)
        file_path = os.path.join(str(IMG_PATH), id + ext)
        with open(file_path, mode="wb") as f:
            shutil.copyfileobj(image.file, f)

    db_project = models.Project(
        user_id=user_id, mindmap_id=mindmap_id, title=title, description=description
    )
    for i, (uuid_, ext) in enumerate(zip(uuids, exts)):
        db_project.images.append(models.ProjectImage(id=uuid_, order=i, ext=ext))
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def get_projects(
    db: Session, skip: int = 0, limit: int = 100
) -> Sequence[models.Project]:
    return db.scalars(select(models.Project).offset(skip).limit(limit)).all()


def get_project(
    db: Session,
    project_id: int,
) -> models.Project | None:
    db_project = db.scalars(
        select(models.Project).where(models.Project.id == project_id)
    ).one_or_none()
    return db_project


def update_project(
    db: Session,
    project_id: int,
    user_id: int,
    title: str | None,
    description: str | None,
) -> models.Project | None:
    db_project = get_project(db, project_id)
    if db_project is None:
        return None
    if db_project.user_id != user_id:
        return None

    if title:
        db_project.title = title
    if description:
        db_project.description = description
    db.commit()
    db.refresh(db_project)
    return db_project
