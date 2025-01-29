from fastapi import APIRouter, HTTPException, Depends, status
from src.categories.service import get_categories_list, get_category_by_id_in_db, create_category_in_db, update_category_in_db, delete_category_in_db
from src.models.category import CategoryModel, CategoryEdit
from src.auth import service as auth_service
from src.models.results import PostModelResponse, PutModelResponse, DeleteModelResponse

categories_router = APIRouter()

@categories_router.get("/categories", tags=["categories"], response_model=list[CategoryModel], status_code=status.HTTP_200_OK)
def get_categories(offset: int = 0, limit: int = 10, current_user: dict = Depends(auth_service.get_current_user)):
    result = get_categories_list(offset, limit)
    return result

@categories_router.get("/categories/{category_id}", tags=["categories"], response_model=CategoryModel, status_code=status.HTTP_200_OK)
def get_category_by_id(category_id: int, current_user: dict = Depends(auth_service.get_current_user)):
    result = get_category_by_id_in_db(category_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return result

@categories_router.post("/categories", tags=["categories"], status_code=status.HTTP_201_CREATED, response_model=PostModelResponse)
def create_category(category: CategoryModel, current_user: dict = Depends(auth_service.get_current_user)):
    # TODO: Add authentication and check if user is admin
    result = create_category_in_db(category)
    if result is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category already exists")
    return {"message": "Category created"}

@categories_router.put("/categories/{category_id}", tags=["categories"], response_model=PutModelResponse, status_code=status.HTTP_200_OK)
def update_category(category_id: int, category: CategoryEdit, current_user: dict = Depends(auth_service.get_current_user)):
    result = update_category_in_db(category_id, category)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found or name already exists")
    return {"message": "Category updated"}

@categories_router.delete("/categories/{category_id}", tags=["categories"], response_model=DeleteModelResponse, status_code=status.HTTP_200_OK)
def delete_category(category_id: int, current_user: dict = Depends(auth_service.get_current_user)):
    # TODO: Add authentication and check if user is admin
    result = delete_category_in_db(category_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return {"message": "Category deleted"}