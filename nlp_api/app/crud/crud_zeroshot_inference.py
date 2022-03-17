from app.crud.base_sqlmodel import CRUDBase
from sqlmodel.ext.asyncio.session import AsyncSession
from app.schemas.zeroshot_inference import (
    ZeroShotInferenceCreate,
    ZeroShotInferenceUpdate,
)
from app.models.zeroshot_inference import ZeroShotInference
from datetime import datetime


class CRUDInference(
    CRUDBase[ZeroShotInference, ZeroShotInferenceCreate, ZeroShotInferenceUpdate]
):
    async def create_inference(
        self, db_session: AsyncSession, *, obj_in: ZeroShotInferenceCreate, user_id: int
    ) -> ZeroShotInference:
        db_obj = ZeroShotInference.from_orm(obj_in)
        db_obj.created_at = datetime.utcnow()
        db_obj.updated_at = datetime.utcnow()
        db_obj.created_by_id = user_id
        db_session.add(db_obj)
        await db_session.commit()
        await db_session.refresh(db_obj)
        return db_obj


zeroshot_inference = CRUDInference(ZeroShotInference)
