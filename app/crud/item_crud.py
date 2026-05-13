from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.const import TodoItemStatusCode

from app.models.item_model import ItemModel
from app.models.list_model import ListModel
from app.schemas.item_schema import NewTodoItem, UpdateTodoItem, ResponseTodoItem


def get_todo_items(per_page: int, page: int, db: Session):
    # Station 18 オフセットページネーションの追加
    return db.query(ItemModel).order_by(ItemModel.id.asc()) \
        .limit(per_page).offset((page-1)*per_page).all()

def get_todo_item(todo_list_id: int, todo_item_id: int, db: Session):
    return db.query(ItemModel).filter(
        ItemModel.id == todo_item_id,
        ItemModel.todo_list_id == todo_list_id
    ).first()

def post_todo_item(todo_list_id:int, new_data: NewTodoItem, db: Session):
    todo_list = db.query(ListModel).filter(ListModel.id == todo_list_id).first()
    if not todo_list:
        raise HTTPException(status_code=404, detail="Todo List (ID: {todo_list_id}) not found")
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

def put_todo_item(todo_list_id: int, todo_item_id: int, data: UpdateTodoItem, db: Session):
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

def delete_todo_item(todo_list_id: int, todo_item_id: int, db: Session):
    todo_list = db.query(ListModel).filter(ListModel.id == todo_list_id).first()
    if not todo_list:
       return False

    db_item = db.get(ItemModel, todo_item_id)
    if not db_item:
        return False

    db.delete(db_item)
    db.commit()
    return True