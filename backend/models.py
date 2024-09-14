from sqlalchemy import Column, Integer, String
from DB import db

class User(db.Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "email": self.email}