from app.schemas.common import (
    IGetResponseBase,
    IPostResponseBase,
    IDeleteResponseBase,
)
from app.utils.text_nlp import analyze_text
from app.schemas.text_inference import (
    TextInferenceCreate,
    TextInferenceRead,
)
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, Query
from app.api import deps
from app import crud
from app.models import TextInference
from app.models import TextInferenceBase
from app.models.user import User

router = APIRouter()


@router.post(
    "/text-classification-predict/", response_model=IPostResponseBase[TextInferenceRead]
)
async def predict(
    request: TextInferenceBase,
    db_session: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    text = request.text

    result = await analyze_text(text)
    text = result[0]
    res = result[1]

    inference = TextInferenceCreate(text=text, result=res)

    my_inference = await crud.text_inference.create_inference(
        db_session, obj_in=inference, user_id=current_user.id
    )

    return IPostResponseBase(data=TextInferenceRead.from_orm(my_inference))
