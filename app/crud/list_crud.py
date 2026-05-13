from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.list_model import ListModel
from app.schemas.list_schema import NewTodoList, UpdateTodoList, ResponseTodoList


def get_todo_lists(per_page: int, page: int, db: Session):
	# Station 18 オフセットページネーションの追加
	return db.query(ListModel).order_by(ListModel.id.asc()) \
		.limit(per_page).offset((page - 1) * per_page).all()

def get_todo_list(todo_list_id: int, db: Session):
    return db.query(ListModel).filter(ListModel.id == todo_list_id).first()

def post_todo_list(new_data: NewTodoList, db: Session):
	post_date = ListModel(
        title=new_data.title,
        description=new_data.description
    )
	db.add(post_date)
	db.commit()
	db.refresh(post_date)
	return post_date

def put_todo_list(todo_list_id: int, data: UpdateTodoList, db: Session):
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

def delete_todo_list(todo_list_id: int, db: Session):
	db_item = db.get(ListModel, todo_list_id)
	if not db_item:
		return False

	db.delete(db_item)
	db.commit()
	return True