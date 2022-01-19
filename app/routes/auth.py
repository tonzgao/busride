from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
from ..models.pydantic.user import User

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class FakeUser:
    id = 1


def fake_decode_token():
    return FakeUser()


# async def get_current_user(token: str = Depends(oauth2_scheme)):
#   return user


async def get_current_user():
    user = fake_decode_token()
    return user
