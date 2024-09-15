from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from DB import db
import crud

app = FastAPI()

@app.get("/welcome")
async def welcom() -> dict:
    return {"message": "welcome"}

@app.get("/hello")
async def hello() -> dict:
    return {"message": "hello"}

@app.post("/users/")
def create_user(name: str, email: str, db: Session = Depends(db.get_session)):
    db_user = crud.get_user_by_email(db, email=email)
    if db_user:
        raise HTTPException(status_code=400, detail="メールアドレスが既に登録されています")
    return crud.create_user(db=db, name=name, email=email)

@app.get("/users/")
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(db.get_session)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(db.get_session)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="ユーザーが見つかりません")
    return db_user

@app.put("/users/{user_id}")
def update_user(user_id: int, name: str = None, email: str = None, db: Session = Depends(db.get_session)):
    db_user = crud.update_user(db, user_id=user_id, name=name, email=email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="ユーザーが見つかりません")
    return db_user

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(db.get_session)):
    db_user = crud.delete_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="ユーザーが見つかりません")
    return {"message": "ユーザーが削除されました"}