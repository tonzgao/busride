from fastapi import APIRouter

from ..models.orm.entity import Entity as ORMEntity
from ..models.pydantic.entity import Entity, EntityCreateIn
from ..utils.wikidata import list_entities, get_entity

router = APIRouter()

# TODO: allow non-wikidata datasources


@router.get("/entities/list/{name}")
async def get_entities_by_name(name: str):
    result = list_entities(name)
    return result


@router.post("/entities", tags=["Entities"], response_model=Entity)
async def create_entity(request: EntityCreateIn):
    data = get_entity(request.identifier)
    new_entity: ORMEntity = await ORMEntity.create(
        identifier=request.identifier, data=data
    )
    return Entity.from_orm(new_entity)


@router.get(
    "/entities/id/{identifier}", tags=["Entities"], response_model=Entity
)
async def retrieve_entity_by_identifier(identifier: str):
    entity: ORMEntity = await ORMEntity.query.where(
        ORMEntity.identifier == identifier
    ).gino.first()
    return Entity.from_orm(entity)


@router.put(
    "/entities/id/{identifier}", tags=["Entities"], response_model=Entity
)
async def update_entity(identifier: str):
    entity: ORMEntity = await ORMEntity.query.where(
        ORMEntity.identifier == identifier
    ).gino.first()
    data = get_entity(identifier)
    await entity.update(data=data).apply()
    return Entity.from_orm(entity)


@router.get("/entities/{id}", tags=["Entities"], response_model=Entity)
async def retrieve_entity(id: int):
    entity: ORMEntity = await ORMEntity.get(id)
    return Entity.from_orm(entity)


# TODO: allow updating entity


@router.delete("/entities/{id}", tags=["Entities"], response_model=Entity)
async def delete_entity(id: int):
    entity: ORMEntity = await ORMEntity.get(id)
    return await entity.delete()
