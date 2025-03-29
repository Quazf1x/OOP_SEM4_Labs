from pydantic import BaseModel
from typing import List, Optional


class ItemCreateSchema(BaseModel):
    name: str
    description: Optional[str] = None
    is_done: bool = False


class ItemSchema(ItemCreateSchema):
    id: int
    todo_list_id: int

    class Config:
        from_attributes = True


class TodoListCreateSchema(BaseModel):
    name: str


class TodoListSchema(TodoListCreateSchema):
    id: int
    items: List[ItemSchema] = []

    class Config:
        from_attributes = True