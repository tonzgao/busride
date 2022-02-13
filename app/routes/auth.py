from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
from passlib.context import CryptContext

from ..models.orm.user import User as ORMUser

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
manager = LoginManager("secret", "/login", use_cookie=True)

router = APIRouter()


@manager.user_loader()
async def query_user(email: str):
    return await ORMUser.get_by_email(email)


@router.get("/ping")
async def ping(current_user=Depends(manager)):
    return {"pong": True}


@router.post("/login")
async def login(data: OAuth2PasswordRequestForm = Depends()):
    email = data.username
    password = data.password

    user = await query_user(email)
    if not user:
        raise InvalidCredentialsException
    if not pwd_context.verify(password, user.password):
        raise InvalidCredentialsException

    access_token = manager.create_access_token(data={"sub": email})
    return {"token": access_token}
