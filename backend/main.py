from fastapi import Depends, FastAPI
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

@app.get("/users/")
async def get_users(db: Session = Depends(db.get_session)):
    users = crud.read_users(db)
    return [user.to_dict() for user in users]