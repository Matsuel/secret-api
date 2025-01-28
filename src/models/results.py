from pydantic import BaseModel

class LoginModelResponse(BaseModel):
    token: str
    token_type: str
    
class PostModelResponse(BaseModel):
    message: str
    
class DeleteModelResponse(BaseModel):
    message: str
    
class PutModelResponse(BaseModel):
    message: str
    
class SecretModel(BaseModel):
    id: int
    text: str
    user_id: int
    category_id: int
    is_public: bool
    likesCount: int
    anonymous: bool
    shared_space_id: int
    
    
class UserInfosModel(BaseModel):
    id: int
    username: str
    followersCount: int
    followsCount: int
    followers: str
    follows: str
    secrets: list[SecretModel]
    
class SpaceModel(BaseModel):
    id: int
    name: str
    is_public: bool