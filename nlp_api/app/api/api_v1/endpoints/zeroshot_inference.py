from select import select
from app.schemas.common import (
    IGetResponseBase,
    IPostResponseBase,
    IDeleteResponseBase,
)
from app.utils.zeroshot_nlp import analyze_text
from app.schemas.zeroshot_inference import (
    ZeroShotInferenceCreate,
    ZeroShotInferenceRead,
)
from fastapi_pagination import Page, Params
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, Query
from app.api import deps
from app import crud
from app.models import ZeroShotInference
from app.models import ZeroShotInferenceBase
from app.models.user import User
from sqlmodel import select

router = APIRouter()


@router.get(
    "/zero-shot-classification-inferences/",
    response_model=IGetResponseBase[Page[ZeroShotInference]],
)
async def get_zero_shot_classification_inferences(
    params: Params = Depends(),
    db_session: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    inferences = await crud.zeroshot_inference.get_multi_paginated(
        db_session, params=params
    )
    return IGetResponseBase[Page[ZeroShotInference]](data=inferences)


@router.get(
    "/zero-shot-classification-inferences/order_by_created_at/",
    response_model=IGetResponseBase[Page[ZeroShotInference]],
)
async def zero_shot_classification_inferences_order_by_created_at(
    params: Params = Depends(),
    db_session: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    query = select(ZeroShotInference).order_by(ZeroShotInference.created_at)
    inferences = await crud.zeroshot_inference.get_multi_paginated(
        db_session, query=query, params=params
    )
    return IGetResponseBase[Page[ZeroShotInferenceRead]](data=inferences)


@router.post(
    "/zero-shot-classification-predict/",
    response_model=IPostResponseBase[ZeroShotInferenceRead],
)
async def predict(
    request: ZeroShotInferenceBase,
    db_session: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
):
    text = request.text
    labels = request.candidate_labels

    result = await analyze_text(text, labels)
    text = result[0]
    candidate_labels = result[1]
    res = result[2]

    inference = ZeroShotInferenceCreate(
        text=text, candidate_labels=candidate_labels, result=res
    )

    my_inference = await crud.zeroshot_inference.create_inference(
        db_session, obj_in=inference, user_id=current_user.id
    )

    return IPostResponseBase(data=ZeroShotInferenceRead.from_orm(my_inference))
