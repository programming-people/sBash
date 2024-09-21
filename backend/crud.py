from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

import models
from auth.password import get_password_hash, verify_password


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
