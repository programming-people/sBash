from sqlalchemy import select
from sqlalchemy.orm import Session

import models
from auth.password import get_password_hash, verify_password


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
