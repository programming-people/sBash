import uuid
from typing import List

from sqlalchemy import Column, ForeignKey, Integer, String, Uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32), index=True)
    hashed_password: Mapped[str]

    projects: Mapped[List["Project"]] = relationship(back_populates="user")
    mindmaps: Mapped[List["Mindmap"]] = relationship(back_populates="user")

    def to_dict(self):
        return {"id": self.id, "name": self.name}


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    mindmap_id: Mapped[int] = mapped_column(ForeignKey("mindmaps.id"))

    title: Mapped[str] = mapped_column(String(32))
    description: Mapped[str] = mapped_column(String(256))

    user: Mapped[User] = relationship(back_populates="projects")
    mindmap: Mapped["Mindmap"] = relationship(back_populates="projects")
    images: Mapped[List["ProjectImage"]] = relationship(
        back_populates="project", lazy="selectin"
    )
    comments: Mapped[List["Comment"]] = relationship(lazy="selectin")


class ProjectImage(Base):
    __tablename__ = "project_images"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4
    )
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    order: Mapped[int]
    ext: Mapped[str]

    project: Mapped["Project"] = relationship(back_populates="images")


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    body: Mapped[str]


class Mindmap(Base):
    __tablename__ = "mindmaps"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    # top_node_id: Mapped[int] = mapped_column(ForeignKey("nodes.id"))

    title: Mapped[str] = mapped_column(String(32))
    description: Mapped[str] = mapped_column(String(256))

    user: Mapped["User"] = relationship(back_populates="mindmaps")
    projects: Mapped[List["Project"]] = relationship(back_populates="mindmap")
    nodes: Mapped[List["Node"]] = relationship(back_populates="mindmap")


class Node(Base):
    __tablename__ = "nodes"

    id: Mapped[int] = mapped_column(primary_key=True)
    mindmap_id: Mapped[int] = mapped_column(ForeignKey("mindmaps.id"))
    parent_node_id: Mapped[int] = mapped_column(ForeignKey("nodes.id"), nullable=True)

    title: Mapped[str] = mapped_column(String(32))

    mindmap: Mapped["Mindmap"] = relationship(back_populates="nodes")
    # parent: Mapped["Node"] = relationship(back_populates="children")
    # children: Mapped[List["Node"]] = relationship(back_populates="parent")
