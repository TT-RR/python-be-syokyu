import os
from datetime import datetime

from fastapi import FastAPI
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.const import TodoItemStatusCode

from app.dependencies import get_db
from app.models.item_model import ItemModel
from app.models.list_model import ListModel

router = APIRouter(
	prefix="/lists",
	tags=["TODOリスト"],
)

class NewTodoList(BaseModel):
    """TODOリスト新規作成時のスキーマ."""

    title: str = Field(title="Todo List Title", min_length=1, max_length=100)
    description: str | None = Field(default=None, title="Todo List Description", min_length=1, max_length=200)

class UpdateTodoList(BaseModel):
    """TODOリスト更新時のスキーマ."""

    title: str | None = Field(default=None, title="Todo List Title", min_length=1, max_length=100)
    description: str | None = Field(default=None, title="Todo List Description", min_length=1, max_length=200)

class ResponseTodoList(BaseModel):
    """TODOリストのレスポンススキーマ."""

    id: int
    title: str = Field(title="Todo List Title", min_length=1, max_length=100)
    description: str | None = Field(default=None, title="Todo List Description", min_length=1, max_length=200)
    created_at: datetime = Field(title="datetime that the item was created")
    updated_at: datetime = Field(title="datetime that the item was updated")

# Station6	Todoリスト取得
@router.get("/lists/{todo_list_id}", tags=["Todoリスト"])
def get_todo_list(todo_list_id: int, db: Session = Depends(get_db)):
    db_item = db.query(ListModel).filter(ListModel.id == todo_list_id).first()
    return db_item

# Station7	Todoリスト新規作成
@router.post("/lists", tags=["Todoリスト"])
def post_todo_list(new_data: NewTodoList, db: Session = Depends(get_db)):
    post_date = ListModel(
        title=new_data.title,
        description=new_data.description
    )
    db.add(post_date)
    db.commit()
    db.refresh(post_date)
    return post_date

# Station8	Todoリスト更新
@router.put("/lists/{todo_list_id}", tags=["Todoリスト"], response_model=ResponseTodoList)
def put_todo_list(todo_list_id: int, data: UpdateTodoList, db: Session = Depends(get_db)):
    update_data = db.query(ListModel).filter(ListModel.id == todo_list_id).first()
    if not update_data:
        raise HTTPException(status_code=404, detail="指定のIDのデータは見つかりませんでした")

    if data.title:
        update_data.title = data.title
    if data.description:
        update_data.description = data.description
    db.add(update_data)
    db.commit()
    db.refresh(update_data)
    return update_data

# Station9	Todoリスト削除
@router.delete("/lists/{todo_list_id}", tags=["Todoリスト"])
def delete_todo_list(todo_list_id: int, db: Session = Depends(get_db)):
    db_item = db.get(ListModel, todo_list_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(db_item)
    db.commit()
    return {}