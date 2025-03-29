from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

Base: DeclarativeMeta = declarative_base()


class TodoList(Base,):
    __tablename__ = "todo_lists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)

    items = relationship("Item", back_populates="todo_list", cascade="all, delete-orphan", lazy="selectin")

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    is_done = Column(Boolean, default=False)
    todo_list_id = Column(Integer, ForeignKey("todo_lists.id", ondelete="CASCADE"))

    todo_list = relationship("TodoList", back_populates="items", lazy="selectin")