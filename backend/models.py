from typing import List

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from DB import db


class User(db.Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    hashed_password: Mapped[str]

    projects: Mapped[List["Project"]] = relationship(back_populates="user")
    mindmaps: Mapped[List["Mindmap"]] = relationship(back_populates="user")

    def to_dict(self):
        return {"id": self.id, "name": self.name, "email": self.email}


class Project(db.Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    mindmap_id: Mapped[int] = mapped_column(ForeignKey("mindmaps.id"))

    title: Mapped[str] = mapped_column(String(32))
    description: Mapped[str] = mapped_column(String(256))

    user: Mapped[User] = relationship(back_populates="projects")
    mindmap: Mapped["Mindmap"] = relationship(back_populates="projects")


class Mindmap(db.Base):
    __tablename__ = "mindmaps"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    # top_node_id: Mapped[int] = mapped_column(ForeignKey("nodes.id"))

    title: Mapped[str] = mapped_column(String(32))
    description: Mapped[str] = mapped_column(String(256))

    user: Mapped["User"] = relationship(back_populates="mindmaps")
    projects: Mapped[List["Project"]] = relationship(back_populates="mindmap")
    nodes: Mapped[List["Node"]] = relationship(back_populates="mindmap")


class Node(db.Base):
    __tablename__ = "nodes"

    id: Mapped[int] = mapped_column(primary_key=True)
    mindmap_id: Mapped[int] = mapped_column(ForeignKey("mindmaps.id"))
    parent_node_id: Mapped[int] = mapped_column(ForeignKey("nodes.id"), nullable=True)

    title: Mapped[str] = mapped_column(String(32))

    mindmap: Mapped["Mindmap"] = relationship(back_populates="nodes")
    # parent: Mapped["Node"] = relationship(back_populates="children")
    # children: Mapped[List["Node"]] = relationship(back_populates="parent")
