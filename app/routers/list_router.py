from fastapi import FastAPI
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models.list_model import ListModel
from app.schemas.list_schema import NewTodoList, UpdateTodoList, ResponseTodoList

router = APIRouter(
	prefix="/lists",
	tags=["TODOリスト"],
)

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