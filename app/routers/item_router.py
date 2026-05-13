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
	prefix="/items",
	tags=["Todo項目"],
)

class NewTodoItem(BaseModel):
    """TODO項目新規作成時のスキーマ."""

    title: str = Field(title="Todo Item Title", min_length=1, max_length=100)
    description: str | None = Field(default=None, title="Todo Item Description", min_length=1, max_length=200)
    due_at: datetime | None = Field(default=None, title="Todo Item Due")

class UpdateTodoItem(BaseModel):
    """TODO項目更新時のスキーマ."""

    title: str | None = Field(default=None, title="Todo Item Title", min_length=1, max_length=100)
    description: str | None = Field(default=None, title="Todo Item Description", min_length=1, max_length=200)
    due_at: datetime | None = Field(default=None, title="Todo Item Due")
    complete: bool | None = Field(default=None, title="Set Todo Item status as completed")

class ResponseTodoItem(BaseModel):
    id: int
    todo_list_id: int
    title: str = Field(title="Todo Item Title", min_length=1, max_length=100)
    description: str | None = Field(default=None, title="Todo Item Description", min_length=1, max_length=200)
    status_code: TodoItemStatusCode = Field(title="Todo Status Code")
    due_at: datetime | None = Field(default=None, title="Todo Item Due")
    created_at: datetime = Field(title="datetime that the item was created")
    updated_at: datetime = Field(title="datetime that the item was updated")

# Station10	Todoアイテム取得
@router.get("/lists/{todo_list_id}/items/{todo_item_id}", 
			tags=["Todo項目"],
            response_model=ResponseTodoItem)
def get_todo_item(todo_list_id: int, todo_item_id: int, db: Session = Depends(get_db)):
    todo_item = db.query(ItemModel).filter(
        ItemModel.id == todo_item_id,
        ItemModel.todo_list_id == todo_list_id
    ).first()
    if not todo_item:
        raise HTTPException(status_code=404, detail="Todo Item not found")
        
    return todo_item

# Station11	Todoアイテム新規作成
@router.post("/lists/{todo_list_id}/items",
			tags=["Todo項目"],
            response_model=ResponseTodoItem)
def post_todo_item(todo_list_id:int, new_data: NewTodoItem, db: Session = Depends(get_db)):
    post_date = ItemModel(
        # title=new_data.title,
        # description=new_data.description,
        # due_at=new_data.due_at
        # model_dumpを使って辞書展開するとコードがスッキリ
        **new_data.model_dump(),
        todo_list_id=todo_list_id,
    )
    post_date.status_code = TodoItemStatusCode.NOT_COMPLETED.value
    db.add(post_date)
    db.commit()
    db.refresh(post_date)
    return post_date

# Station12	Todoアイテム更新
@router.put("/lists/{todo_list_id}/items/{todo_item_id}",
			tags=["Todo項目"],
            response_model=ResponseTodoItem)
def put_todo_item(todo_list_id: int,
				todo_item_id: int,
                data: UpdateTodoItem,
                db: Session = Depends(get_db)):
    update_data = db.query(ItemModel).filter(
        ItemModel.id == todo_item_id,
        ItemModel.todo_list_id == todo_list_id
    ).first()
    if not update_data:
        raise HTTPException(status_code=404, detail="指定のIDのデータは見つかりませんでした")
    
    if data.complete is not None:
        if data.complete:
            update_data.status_code = TodoItemStatusCode.COMPLETED.value
        else:
            update_data.status_code = TodoItemStatusCode.NOT_COMPLETED.value
            
    update_dict = data.model_dump(exclude_unset=True, exclude={"complete"})
    for key, value in update_dict.items():
        setattr(update_data, key, value)
    
    db.add(update_data)
    db.commit()
    db.refresh(update_data)
    return update_data

# Station13	Todoアイテム削除
@router.delete("/lists/{todo_list_id}/items/{todo_item_id}", tags=["Todo項目"])
def delete_todo_item(todo_list_id: int,
				todo_item_id: int,
                db: Session = Depends(get_db)):
    db_item = db.get(ItemModel, todo_item_id)
    
    if not db_item or db_item.todo_list_id != todo_list_id:
        raise HTTPException(status_code=404, detail="Todo Item not found")

    db.delete(db_item)
    db.commit()
    return {}