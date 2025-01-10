from src.models.category import Category, CategoryModel, CategoryEdit
from src.models.database import SessionLocal
from sqlalchemy import insert, update

def get_categories_list(offset: int = 0, limit: int = 10):
    with SessionLocal() as session:
        categories = session.query(Category).offset(offset).limit(limit).all()
        if not categories:
            return []
        return [category for category in categories]
    
def get_category_by_id_in_db(category_id: int):
    with SessionLocal() as session:
        category = session.query(Category).filter(Category.id == category_id).first()
        return category if category else None
    
def check_if_category_name_exists(category_name: str):
    with SessionLocal() as session:
        category = session.query(Category).filter(Category.name == category_name).first()
        if category is None:
            return False
        return True
    
def create_category_in_db(category: CategoryModel):
    if check_if_category_name_exists(category.name):
        return None
    with SessionLocal() as session:
        stmt = insert(Category).values(name=category.name)
        session.execute(stmt)
        session.commit()
        return True
    
def update_category_in_db(category_id: int, category: CategoryEdit):
    if not get_category_by_id_in_db(category_id):
        return False
    if check_if_category_name_exists(category.name):
        return False
    with SessionLocal() as session:
        stmt = (
            update(Category)
            .where(Category.id == category_id)
            .values(name=category.name)
        )
        session.execute(stmt)
        session.commit()
    return True

def delete_category_in_db(category_id: int):
    if not get_category_by_id_in_db(category_id):
        return False
    with SessionLocal() as session:
        stmt = session.query(Category).filter(Category.id == category_id).first()
        session.delete(stmt)
        session.commit()
    return True