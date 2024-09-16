from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy import relationship

from DB import db


class User(db.Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)

    services = relationship("Service", back_populates="owner")

    def to_dict(self):
        return {"id": self.id, "name": self.name, "email": self.email}


class Service(db.Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    title = Column(String, unique=True)
    description = Column(String)
    like_count = Column(Integer)

    owner = relationship("User", back_populates="services")

    comments = relationship("Comment", back_populates="owner")


class Comment(db.Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    service_id = Column(Integer, ForeignKey("services.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    body = Column(String)

    owner = relationship("Service", back_populates="comments")


class UserLikeService(db.Base):
    __tablename__ = "user_like_services"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    service_id = Column(Integer, ForeignKey("comments.id"), primary_key=True)
