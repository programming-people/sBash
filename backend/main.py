from fastapi import FastAPI

app = FastAPI()


@app.get("/welcome")
async def welcom() -> dict:
    return {"message": "welcome"}
