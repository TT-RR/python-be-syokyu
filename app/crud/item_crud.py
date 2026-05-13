from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.const import TodoItemStatusCode

from app.models.item_model import ItemModel
from app.schemas.item_schema import NewTodoItem, UpdateTodoItem, ResponseTodoItem

def get_todo_item(todo_list_id: int, todo_item_id: int, db: Session):
    todo_item = db.query(ItemModel).filter(
        ItemModel.id == todo_item_id,
        ItemModel.todo_list_id == todo_list_id
    ).first()
    if not todo_item:
        raise HTTPException(status_code=404, detail="Todo Item not found")
        
    return todo_item

def post_todo_item(todo_list_id:int, new_data: NewTodoItem, db: Session):
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
    db_item = db.get(ItemModel, todo_item_id)
    
    if not db_item or db_item.todo_list_id != todo_list_id:
        return False
        raise HTTPException(status_code=404, detail="Todo Item not found")

    db.delete(db_item)
    db.commit()
    return True