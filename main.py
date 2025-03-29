from fastapi import FastAPI
from src.database import init_db
from src.routes import router

app = FastAPI()

app.include_router(router)

@app.on_event("startup")
async def startup():
    await init_db()
