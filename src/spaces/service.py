from ..models.shared_space import SharedSpace
from ..models.shared_space_user import SharedSpaceUser
from src.models.database import SessionLocal


def get_spaces_list():
    with SessionLocal() as session:
        spaces = session.query(SharedSpace).all()
        if not spaces:
            return []
        return spaces
    
def get_space(space_id: int):
    with SessionLocal() as session:
        space = session.query(SharedSpace).filter(SharedSpace.id == space_id).first()
        if not space:
            return None
        return space
    
def create_space(name: str, is_public: bool):
    with SessionLocal() as session:
        max_id = session.query(SharedSpace.id).order_by(SharedSpace.id.desc()).first()
        new_id = (max_id[0] + 1) if max_id else 1
        new_space = SharedSpace(id=new_id, name=name, is_public=is_public)
        session.add(new_space)
        session.commit()
        session.refresh(new_space)
        return new_space
    
def update_space(space_id: int, name: str = None, is_public: bool = None):
    with SessionLocal() as session:
        space = session.query(SharedSpace).filter(SharedSpace.id == space_id).first()
        if not space:
            return None
        if name is not None:
            space.name = name
        if is_public is not None:
            space.is_public = is_public
        session.commit()
        session.refresh(space)
        return space
    
def invite_user_to_space(space_id: int, user_id: int):
    with SessionLocal() as session:
        existing_invitation = session.query(SharedSpaceUser).filter(
            SharedSpaceUser.shared_space_id == space_id,
            SharedSpaceUser.user_id == user_id
        ).first()
        
        if existing_invitation:
            return existing_invitation
        
        new_invitation = SharedSpaceUser(shared_space_id=space_id, user_id=user_id)
        session.add(new_invitation)
        session.commit()
        return new_invitation
