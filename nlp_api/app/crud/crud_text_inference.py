from app.crud.base_sqlmodel import CRUDBase
from sqlmodel.ext.asyncio.session import AsyncSession
from app.schemas.text_inference import TextInferenceCreate, TextInferenceUpdate
from app.models.text_inference import TextInference
from datetime import datetime


class CRUDInference(CRUDBase[TextInference, TextInferenceCreate, TextInferenceUpdate]):
    async def create_inference(
        self, db_session: AsyncSession, *, obj_in: TextInferenceCreate, user_id: int
    ) -> TextInference:
        db_obj = TextInference.from_orm(obj_in)
        db_obj.created_at = datetime.utcnow()
        db_obj.updated_at = datetime.utcnow()
        db_obj.created_by_id = user_id
        db_session.add(db_obj)
        await db_session.commit()
        await db_session.refresh(db_obj)
        return db_obj


text_inference = CRUDInference(TextInference)
