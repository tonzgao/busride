from fastapi import APIRouter, Depends
from fastapi_login.exceptions import InvalidCredentialsException

from ..models.orm.interest import Interest as ORMInterest
from ..models.pydantic.interest import Interest, InterestCreateIn
from ..models.pydantic.user import User
from .auth import manager

router = APIRouter()


@router.post("/interests", tags=["Interests"], response_model=Interest)
async def create_interest(
    request: InterestCreateIn, current_user: User = Depends(manager)
):
    new_interest: ORMInterest = await ORMInterest.create(
        **request.dict(), user_id=current_user.id
    )
    return Interest.from_orm(new_interest)


@router.delete("/interests/{id}", tags=["Interests"], response_model=Interest)
async def delete_interest(id: int, current_user: User = Depends(manager)):
    interest: ORMInterest = await ORMInterest.get(id)
    if interest.user_id != current_user.id:
        raise InvalidCredentialsException()
    return await interest.delete()
