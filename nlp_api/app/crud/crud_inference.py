from app.crud.base_sqlmodel import CRUDBase
from sqlmodel.ext.asyncio.session import AsyncSession

from app.schemas.inference import IInferenceCreate, IInferenceUpdate
from app.models.inference import Inference
from datetime import datetime


class CRUDInference(CRUDBase[Inference, IInferenceCreate, IInferenceUpdate]):
    async def create_inference(
        self, db_session: AsyncSession, *, obj_in: IInferenceCreate, user_id: int
    ) -> Inference:
        db_obj = Inference.from_orm(obj_in)
        db_obj.created_at = datetime.utcnow()
        db_obj.updated_at = datetime.utcnow()
        db_obj.created_by_id = user_id
        db_session.add(db_obj)
        await db_session.commit()
        await db_session.refresh(db_obj)
        return db_obj


inference = CRUDInference(Inference)
