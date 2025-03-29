from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.database import get_db
from src.model import TodoList, Item
from src.schemas import TodoListCreateSchema, TodoListSchema, ItemCreateSchema, ItemSchema

router = APIRouter()


@router.post("/todolists/", response_model=TodoListSchema)
async def create_todolist(todolist: TodoListCreateSchema, db: AsyncSession = Depends(get_db)):
    new_list =  TodoList(name=todolist.name)
    db.add(new_list)
    await db.commit()
    await db.refresh(new_list)
    return new_list


@router.get("/todolists/", response_model=list[TodoListSchema])
async def get_todolists(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TodoList).order_by(TodoList.id))
    return result.scalars().all()


@router.patch("/todolists/{todolist_id}/", response_model=TodoListSchema)
async def update_todolist(
    todolist_id: int,
    todolist_update: TodoListCreateSchema,
    db: AsyncSession = Depends(get_db)
):
    todolist = await db.get(TodoList, todolist_id)
    if not todolist:
        raise HTTPException(status_code=404, detail="TodoList not found")

    todolist.name = todolist_update.name

    await db.commit()
    await db.refresh(todolist)
    return todolist


@router.delete("/todolists/{todolist_id}/")
async def delete_todolist(todolist_id: int, db: AsyncSession = Depends(get_db)):
    todolist = await db.get(TodoList, todolist_id)
    if not todolist:
        raise HTTPException(status_code=404, detail="TodoList not found")

    await db.delete(todolist)
    await db.commit()
    return {"message": "TodoList deleted"}


@router.get("/todolists/{todolist_id}/items/", response_model=list[ItemSchema])
async def get_items(todolist_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Item).filter_by(todo_list_id=todolist_id))
    return result.scalars().all()


@router.post("/todolists/{todolist_id}/items/", response_model=ItemSchema)
async def add_item(todolist_id: int, item: ItemCreateSchema, db: AsyncSession = Depends(get_db)):
    todolist = await db.get(TodoList, todolist_id)
    if not todolist:
        raise HTTPException(status_code=404, detail="TodoList not found")

    new_item = Item(name=item.name, description=item.description, is_done=item.is_done, todo_list_id=todolist_id)
    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)
    return new_item


@router.patch("/items/{item_id}/", response_model=ItemSchema)
async def update_item(item_id: int, item: ItemCreateSchema, db: AsyncSession = Depends(get_db)):
    db_item = await db.get(Item, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")

    db_item.name = item.name
    db_item.description = item.description
    db_item.is_done = item.is_done

    await db.commit()
    await db.refresh(db_item)
    return db_item


@router.delete("/items/{item_id}/")
async def delete_item(item_id: int, db: AsyncSession = Depends(get_db)):
    item = await db.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    await db.delete(item)
    await db.commit()
    return {"message": "Item deleted"}