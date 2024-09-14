from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "postgresql://username:password@localhost/mydatabase"

class DB:
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url, echo=True)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.Base = declarative_base()

    def get_session(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

# データベースのインスタンスを作成
db = DB(DATABASE_URL)
