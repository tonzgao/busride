from fastapi import APIRouter

from ..models.orm.entity import Entity as ORMUser
from ..models.pydantic.entity import Entity, EntityCreateIn
from ..utils.wikidata import list_entities, get_entity

router = APIRouter()

@router.get("/entities/list/{name}")
async def get_entities_by_name(name: str):
    result = list_entities(name)
    return result

@router.post("/entities", tags=["Entities"], response_model=Entity)
async def create_entity(request: EntityCreateIn):
    data = get_entity(request.identifier)
    new_entity: ORMUser = await ORMUser.create(
        identifier=request.identifier,
        data=data
    )
    return Entity.from_orm(new_entity)


@router.get("/entities/{id}", tags=["Entities"], response_model=Entity)
async def retrieve_entity(id: int):
    entity: ORMUser = await ORMUser.get(id)
    return Entity.from_orm(entity)

# TODO: allow updating entity

@router.delete("/entities/{id}", tags=["Entities"], response_model=Entity)
async def delete_entity(id: int):
    entity: ORMUser = await ORMUser.get(id)
    return await entity.delete()
