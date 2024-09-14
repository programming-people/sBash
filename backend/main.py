from fastapi import FastAPI

app = FastAPI()


@app.get("/welcome")
async def welcom() -> dict:
    return {"message": "welcome"}


@app.get("/hello")
async def hello() -> dict:
    return {"message": "hello"}
