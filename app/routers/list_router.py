from fastapi import FastAPI
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.crud import list_crud
from app.schemas.list_schema import NewTodoList, UpdateTodoList, ResponseTodoList

router = APIRouter(
	prefix="/lists",
	tags=["TODOリスト"],
)

# Station15	Todoリスト全件取得
@router.get("/", response_model=list[ResponseTodoList])
def get_todo_lists(db: Session = Depends(get_db)):
    all_list_data = list_crud.get_todo_lists(db)
    return all_list_data

# Station6	Todoリスト取得
@router.get("/{todo_list_id}", response_model=ResponseTodoList)
def get_todo_list(todo_list_id: int, db: Session = Depends(get_db)):
    db_item = list_crud.get_todo_list(todo_list_id, db)
    if db_item is None:
         raise HTTPException(status_code=404, detail="TODO List not found")
    return db_item

# Station7	Todoリスト新規作成
@router.post("/", response_model=ResponseTodoList)
def post_todo_list(new_data: NewTodoList, db: Session = Depends(get_db)):
    post_date = list_crud.post_todo_list(new_data, db)
    return post_date

# Station8	Todoリスト更新
@router.put("/{todo_list_id}", response_model=ResponseTodoList)
def put_todo_list(todo_list_id: int, data: UpdateTodoList, db: Session = Depends(get_db)):
    update_data = list_crud.put_todo_list(todo_list_id, data, db)
    return update_data

# Station9	Todoリスト削除
@router.delete("/{todo_list_id}")
def delete_todo_list(todo_list_id: int, db: Session = Depends(get_db)):
	item_flag = list_crud.delete_todo_list(todo_list_id, db)
	
	if item_flag == False:
		raise HTTPException(status_code=404, detail="Todo not found")
	return {}
		