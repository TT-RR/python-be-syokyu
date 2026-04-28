import os
from datetime import datetime

from fastapi import FastAPI
from fastapi import HTTPException, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.const import TodoItemStatusCode

from .dependencies import get_db
from .models.item_model import ItemModel
from .models.list_model import ListModel

DEBUG = os.environ.get("DEBUG", "") == "true"

app = FastAPI(
    title="Python Backend Stations",
    debug=DEBUG,
)

if DEBUG:
    from debug_toolbar.middleware import DebugToolbarMiddleware

    # panelsに追加で表示するパネルを指定できる
    app.add_middleware(
        DebugToolbarMiddleware,
        panels=["app.database.SQLAlchemyPanel"],
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
@app.get("/lists/{todo_list_id}", tags=["Todoリスト"])
def get_todo_list(todo_list_id: int, db: Session = Depends(get_db)):
    db_item = db.query(ListModel).filter(ListModel.id == todo_list_id).first()
    return db_item

# Station7	Todoリスト新規作成
@app.post("/lists", tags=["Todoリスト"])
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
@app.put("/lists/{todo_list_id}", tags=["Todoリスト"], response_model=ResponseTodoList)
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
@app.delete("/lists/{todo_list_id}", tags=["Todoリスト"])
def delete_todo_list(todo_list_id: int, db: Session = Depends(get_db)):
    db_item = db.get(ListModel, todo_list_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(db_item)
    db.commit()
    return {}

# Station4
@app.get("/health", tags=["System"])
def get_health():
    return { "status": "ok" }

# Station3
@app.get("/echo")
def get_echo(message, name):
    return {"Message":	message + ' ' + name + '!'}

# Station2
@app.get("/hello", tags=["Hello"])
def get_hello():
    return {"Message": "Hello TechTrain!"}