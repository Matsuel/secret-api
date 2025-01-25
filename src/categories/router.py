from fastapi import APIRouter, HTTPException, Depends
from src.categories.service import get_categories_list, get_category_by_id_in_db, create_category_in_db, update_category_in_db, delete_category_in_db
from src.models.category import CategoryModel, CategoryEdit
from src.auth import service as auth_service

categories_router = APIRouter()

@categories_router.get("/categories", tags=["categories"])
def get_categories(offset: int = 0, limit: int = 10, current_user: dict = Depends(auth_service.get_current_user)):
    result = get_categories_list(offset, limit)
    if not result:
        raise HTTPException(status_code=404, detail="No categories found")
    return result

@categories_router.get("/categories/{category_id}", tags=["categories"])
def get_category_by_id(category_id: int, current_user: dict = Depends(auth_service.get_current_user)):
    result = get_category_by_id_in_db(category_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return result

@categories_router.post("/categories", tags=["categories"])
def create_category(category: CategoryModel, current_user: dict = Depends(auth_service.get_current_user)):
    # TODO: Add authentication and check if user is admin
    result = create_category_in_db(category)
    if result is None:
        raise HTTPException(status_code=400, detail="Category already exists")
    return {"message": "Category created"}

@categories_router.put("/categories/{category_id}", tags=["categories"])
def update_category(category_id: int, category: CategoryEdit, current_user: dict = Depends(auth_service.get_current_user)):
    result = update_category_in_db(category_id, category)
    if not result:
        raise HTTPException(status_code=404, detail="Category not found or name already exists")
    return {"message": "Category updated"}

@categories_router.delete("/categories/{category_id}", tags=["categories"])
def delete_category(category_id: int, current_user: dict = Depends(auth_service.get_current_user)):
    # TODO: Add authentication and check if user is admin
    result = delete_category_in_db(category_id)
    if not result:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Category deleted"}