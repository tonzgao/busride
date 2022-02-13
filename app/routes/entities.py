from fastapi import APIRouter

from ..models.orm.entity import Entity as ORMEntity
from ..models.pydantic.entity import Entity, EntityCreateIn
from ..utils.wikidata import get_entity, list_entities

router = APIRouter()

# TODO: allow non-wikidata datasources


@router.get("/entities/tags/{name}")
async def get_entities_by_name(name: str):
    # TODO: list entities with the name already in database
    result = list_entities(name)
    return result


@router.post("/entities", tags=["Entities"], response_model=Entity)
async def create_entity(request: EntityCreateIn):
    data = get_entity(request.identifier)
    new_entity: ORMEntity = await ORMEntity.create(
        identifier=request.identifier, data=data
    )
    return Entity.from_orm(new_entity)


@router.get("/entities/{id}", tags=["Entities"], response_model=Entity)
async def retrieve_entity(id: int):
    entity: ORMEntity = await ORMEntity.get(id)
    return Entity.from_orm(entity)


@router.delete("/entities/{id}", tags=["Entities"], response_model=Entity)
async def delete_entity(id: int):
    entity: ORMEntity = await ORMEntity.get(id)
    return await entity.delete()


@router.get(
    "/entities/tag/{identifier}", tags=["Entities"], response_model=Entity
)
async def retrieve_entity_by_identifier(identifier: str):
    entity: ORMEntity = await ORMEntity.get_by_identifier(identifier)
    if not entity:
        return
    return Entity.from_orm(entity)


@router.put(
    "/entities/tag/{identifier}", tags=["Entities"], response_model=Entity
)
async def update_entity(identifier: str):
    entity: ORMEntity = await ORMEntity.get_by_identifier(identifier)
    data = get_entity(identifier)
    await entity.update(data=data).apply()
    return Entity.from_orm(entity)
