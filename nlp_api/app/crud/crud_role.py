from typing import List
from app.schemas.role import IRoleCreate, IRoleUpdate
from app.models.role import Role
from app.models.user import User
from app.crud.base_sqlmodel import CRUDBase
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import datetime
from sqlmodel import select

class CRUDRole(CRUDBase[Role, IRoleCreate, IRoleUpdate]):
    async def get_role_by_name(self, db_session: AsyncSession, *, name: str) -> Role:
        role = await db_session.exec(select(Role).where(Role.name == name))
        return role.first()
        
    async def create_role(self, db_session: AsyncSession, *, obj_in: IRoleCreate, user_id: int) -> Role:        
        db_obj = Role.from_orm(obj_in)
        db_obj.created_by_id = user_id
        db_obj.created_at = datetime.utcnow()
        db_obj.updated_at = datetime.utcnow()        
        db_session.add(db_obj)
        await db_session.commit()
        await db_session.refresh(db_obj)
        return db_obj

    async def add_role_to_user(self, db_session: AsyncSession, *, user: User, role_id: int) -> Role:
        role = await super().get(db_session, role_id)
        role.users.append(user)        
        db_session.add(role)
        await db_session.commit()
        await db_session.refresh(role)
        return role


role = CRUDRole(Role)
