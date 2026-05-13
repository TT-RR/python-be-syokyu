from fastapi import FastAPI
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models.list_model import ListModel
from app.crud import list_crud
from app.schemas.list_schema import NewTodoList, UpdateTodoList, ResponseTodoList

router = APIRouter(
	prefix="/lists",
	tags=["TODOリスト"],
)

# Station6	Todoリスト取得
@router.get("/lists/{todo_list_id}", tags=["Todoリスト"])
def get_todo_list(todo_list_id: int, db: Session = Depends(get_db)):
    db_item = list_crud.get_todo_list(todo_list_id, db)
    return db_item

# Station7	Todoリスト新規作成
@router.post("/lists", tags=["Todoリスト"])
def post_todo_list(new_data: NewTodoList, db: Session = Depends(get_db)):
    post_date = list_crud.post_todo_list(new_data, db)
    return post_date

# Station8	Todoリスト更新
@router.put("/lists/{todo_list_id}", tags=["Todoリスト"], response_model=ResponseTodoList)
def put_todo_list(todo_list_id: int, data: UpdateTodoList, db: Session = Depends(get_db)):
    update_data = list_crud.put_todo_list(todo_list_id, data, db)
    return update_data

# Station9	Todoリスト削除
@router.delete("/lists/{todo_list_id}", tags=["Todoリスト"])
def delete_todo_list(todo_list_id: int, db: Session = Depends(get_db)):
	item_flag = list_crud.delete_todo_list(todo_list_id, db)
	
	if item_flag == False:
		HTTPException(status_code=404, detail="Todo not found")
	return {}
		