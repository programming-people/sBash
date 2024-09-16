from sqlalchemy.orm import Session
import models


def get_service(db: Session, service_id: int):
    return db.query(models.Service).filter(models.Service.id == service_id).first()


def get_services(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Service).offset(skip).limit(limit).all()


def create_service(db: Session, user_id: int, title: str, description: str):
    db_service = models.Service(
        user_id=user_id, title=title, description=description, like_count=0
    )
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service


def update_service(
    db: Session,
    service_id: int,
    title: str | None = None,
    description: str | None = None,
    adding_like_count: int | None = None,
):
    db_service = (
        db.query(models.Service).filter(models.Service.id == service_id).first()
    )
    if db_service:
        if title:
            db_service.title = title
        if description:
            db_service.description = description
        if adding_like_count:
            db_service.like_count += adding_like_count
    return db_service


def delete_service(db: Session, service_id: int):
    db_service = (
        db.query(models.Service).filter(models.Service.id == service_id).first()
    )
    if db_service:
        db.delete(db_service)
        db.commit()
    return db_service


def create_comment(db: Session, service_id: int, user_id: int, body: str):
    db_comment = models.Comment(service_id=service_id, user_id=user_id, body=body)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def create_user_like_service(db: Session, user_id: int, service_id: int):
    db_user_lke_service = models.UserLikeService(user_id=user_id, service_id=service_id)
    db.add(db_user_lke_service)
    db.commit()
    db.refresh(db_user_lke_service)


def delete_user_like_service(db: Session, user_id: int, service_id: int):
    db_user_like_service = (
        db.query(models.UserLikeService)
        .filter(models.UserLikeService.service_id == service_id)
        .filter(models.UserLikeService.user_id == user_id)
        .first()
    )
    if db_user_like_service:
        db.delete(db_user_like_service)
        db.commit()
    return db_user_like_service
