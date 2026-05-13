from fastapi import FastAPI
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.crud import item_crud
from app.schemas.item_schema import NewTodoItem, UpdateTodoItem, ResponseTodoItem


router = APIRouter(
	prefix="/lists/{todo_list_id}/items",
	tags=["Todo項目"],
)

# Station15	Todoアイテム全件取得
@router.get("/", response_model=list[ResponseTodoItem])
def get_todo_items(db: Session = Depends(get_db)):
    all_item_data = item_crud.get_todo_items(db)
    return all_item_data

# Station10	Todoアイテム取得
@router.get("/{todo_item_id}", response_model=ResponseTodoItem)
def get_todo_item(todo_list_id: int, todo_item_id: int, db: Session = Depends(get_db)):
    todo_item = item_crud.get_todo_item(todo_list_id, todo_item_id, db)
    if not todo_item:
        raise HTTPException(status_code=404, detail="Todo Item not found")
    return todo_item


# Station11	Todoアイテム新規作成
@router.post("/", response_model=ResponseTodoItem)
def post_todo_item(todo_list_id:int, new_data: NewTodoItem, db: Session = Depends(get_db)):
    post_data = item_crud.post_todo_item(todo_list_id, new_data, db)
    return post_data


# Station12	Todoアイテム更新
@router.put("/{todo_item_id}", response_model=ResponseTodoItem)
def put_todo_item(todo_list_id: int,
				todo_item_id: int,
                data: UpdateTodoItem,
                db: Session = Depends(get_db)):
    update_data = item_crud.put_todo_item(todo_list_id, todo_item_id, data, db)
    return update_data


# Station13	Todoアイテム削除
@router.delete("/{todo_item_id}")
def delete_todo_item(todo_list_id: int,
				todo_item_id: int,
                db: Session = Depends(get_db)):
    item_flag = item_crud.delete_todo_item(todo_list_id, todo_item_id, db)
    if item_flag == False:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {}