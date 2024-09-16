from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

HOST = os.getenv("HOST")
USER_NAME = os.getenv("USER_NAME")
DB_NAME = os.getenv("DB_NAME")
PASSWORD = os.getenv("PASSWORD")

DATABASE_URL = f"postgresql://{USER_NAME}:{PASSWORD}@{HOST}/{DB_NAME}"


class DB:
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url, echo=True)
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )
        self.Base = declarative_base()

    def get_session(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()


# データベースのインスタンスを作成
db = DB(DATABASE_URL)
