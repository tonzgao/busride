from fastapi import APIRouter, Depends

from ..models.orm.api import Api as ORMApi
from ..models.pydantic.api import Api, ApiCreateIn
from ..models.pydantic.user import User

from .auth import manager

router = APIRouter()


@router.post("/apis", tags=["Apis"], response_model=Api)
async def create_api(
    request: ApiCreateIn, current_user: User = Depends(manager)
):
    new_api: ORMApi = await ORMApi.create(
        **request.dict(), user_id=current_user.id
    )
    return Api.from_orm(new_api)


@router.delete("/apis/{id}", tags=["Apis"], response_model=Api)
async def delete_api(id: int):
    api: ORMApi = await ORMApi.get(id)
    return await api.delete()
