from select import select
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
from fastapi_pagination import Page, Params
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, Query
from app.api import deps
from app import crud
from app.models import TextInference
from app.models import TextInferenceBase
from app.models.user import User
from sqlmodel import select

router = APIRouter()


@router.get(
    "/text-classification-inferences/",
    response_model=IGetResponseBase[Page[TextInferenceRead]],
)
async def get_text_classification_inferences(
    params: Params = Depends(),
    db_session: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    inferences = await crud.text_inference.get_multi_paginated(
        db_session, params=params
    )
    return IGetResponseBase[Page[TextInferenceRead]](data=inferences)


@router.get(
    "/text-classification-inferences/order_by_created_at/",
    response_model=IGetResponseBase[Page[TextInferenceRead]],
)
async def text_classification_inferences_order_by_created_at(
    params: Params = Depends(),
    db_session: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    query = select(TextInference).order_by(TextInference.created_at)
    inferences = await crud.text_inference.get_multi_paginated(
        db_session, query=query, params=params
    )
    return IGetResponseBase[Page[TextInferenceRead]](data=inferences)


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
