from fastapi import APIRouter, HTTPException
from src.categories.service import get_categories_list, get_category_by_id_in_db, create_category_in_db, update_category_in_db, delete_category_in_db
from src.models.category import CategoryModel, CategoryEdit

categories_router = APIRouter()

@categories_router.get("/categories", tags=["categories"])
def get_categories(offset: int = 0, limit: int = 10):
    result = get_categories_list(offset, limit)
    return result

@categories_router.get("/categories/{category_id}", tags=["categories"])
def get_category_by_id(category_id: int):
    result = get_category_by_id_in_db(category_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return result

@categories_router.post("/categories", tags=["categories"])
def create_category(category: CategoryModel):
    result = create_category_in_db(category)
    if result is None:
        raise HTTPException(status_code=400, detail="Category already exists")
    return {"message": "Category created"}

@categories_router.put("/categories/{category_id}", tags=["categories"])
def update_category(category_id: int, category: CategoryEdit):
    result = update_category_in_db(category_id, category)
    if not result:
        raise HTTPException(status_code=404, detail="Category not found or name already exists")
    return {"message": "Category updated"}

@categories_router.delete("/categories/{category_id}", tags=["categories"])
def delete_category(category_id: int):
    result = delete_category_in_db(category_id)
    if not result:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Category deleted"}