from app.schemas.common import (
    IGetResponseBase,
    IPostResponseBase,
    IDeleteResponseBase,
)
from app.utils.nlp import analyze_text
from app.schemas.inference import (
    IInferenceCreate,
    IInferenceRead,
    IInferenceReadWithUsers,
    IInferenceUpdate,
)
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, Query
from app.api import deps
from app import crud
from app.models import Inference
from app.models import InferenceBase
from app.utils.map_schema import map_models_schema
from app.models.user import User

router = APIRouter()


@router.post("/predict/", response_model=IPostResponseBase[IInferenceRead])
async def predict(
    request: InferenceBase,
    # inference: IInferenceCreate,
    db_session: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    # nlp_model=Depends(analyze_text),
):
    text = request.text
    labels = request.candidate_labels

    result = await analyze_text(text, labels)
    text = result[0]
    candidate_labels = result[1]
    res = result[2]

    print("ACA")
    print(type(text))
    inference = IInferenceCreate(
        text=text, candidate_labels=candidate_labels, result=res
    )

    print("HAST AQUI LLEGO", inference)
    print(type(inference))

    my_inference = await crud.inference.create_inference(
        db_session, obj_in=inference, user_id=current_user.id
    )

    print("POR AQUI", my_inference)
    print(type(my_inference))
  
    return IPostResponseBase(data=IInferenceRead.from_orm(my_inference))
    # return IInferenceRead(text=text, candidate_labels=candidate_labels, result=res)
