from fastapi import APIRouter
from src.schemas import ItemSchema

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Сервер работает"}

# На момент 1 лабы без фактического сохранения в бд
@router.post("/items/")
async def add_item(item: ItemSchema, db):
    return {"name": item.name, "description": item.description}