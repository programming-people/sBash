from models import User
from sqlalchemy.orm import Session

def read_users(db: Session):
    users = db.query(User).all()
    return users