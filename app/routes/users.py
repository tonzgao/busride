from fastapi import APIRouter, Depends

from ..models.orm.user import User as ORMUser
from ..models.pydantic.user import User, UserCreateIn, UserUpdateIn
from ..settings.arq import settings as redis_settings
from .auth import manager, pwd_context

router = APIRouter()


@router.post("/users", tags=["Users"], response_model=User)
async def create_user(request: UserCreateIn):
    hashed_password = pwd_context.hash(request.password)
    new_user: ORMUser = await ORMUser.create(
        name=request.name, email=request.email, password=hashed_password
    )
    return User.from_orm(new_user)


@router.get("/users/{id}", tags=["Users"], response_model=User)
async def retrieve_user(id: int):
    user: ORMUser = await ORMUser.get(id)
    return User.from_orm(user)


@router.put("/users/{id}", tags=["Users"], response_model=User)
async def update_user(request: UserUpdateIn, id: int):
    user: ORMUser = await ORMUser.get(id)
    updated_fields: User = User.from_orm(request)
    await user.update(**updated_fields.dict(skip_defaults=True)).apply()
    return User.from_orm(user)


@router.delete("/users/{id}", tags=["Users"], response_model=User)
async def delete_user(id: int):
    user: ORMUser = await ORMUser.get(id)
    return await user.delete()


@router.get("/whoami", tags=["Users"], response_model=User)
async def whoami(current_user=Depends(manager)):
    return current_user
