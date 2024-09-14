from models import User
from sqlalchemy.orm import Session
from fastapi import Depends
from DB import db

def read_users(db: Session):
    users = db.query(User).all()
    return users