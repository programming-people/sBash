from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from load_env import DB_URL


class DB:
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url, echo=True)
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

    def get_session(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()


# データベースのインスタンスを作成
db = DB(DB_URL)
