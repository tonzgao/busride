from fastapi import APIRouter

from ..models.orm.entity import Entity as ORMEntity
from ..models.pydantic.entity import Entity, EntityCreateIn
from ..utils.wikidata import get_entity, list_entities
from ..libs.redis import get_redis

router = APIRouter()
# TODO: allow non-wikidata datasources


async def check_entity(entity):
    redis = await get_redis()
    await redis.enqueue_job("check_entity", entity)


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
    entity = Entity.from_orm(new_entity)
    await check_entity(entity)
    return entity


@router.get("/entities/{id}", tags=["Entities"], response_model=Entity)
async def retrieve_entity(id: int):
    entity: ORMEntity = await ORMEntity.get(id)
    return Entity.from_orm(entity)


@router.post(
    "/entities/{id}/force_check", tags=["Entities"], response_model=Entity
)
async def retrieve_entity(id: int):
    # TODO: add auth requirements
    entity: ORMEntity = await ORMEntity.get(id)
    await check_entity(entity)
    return entity


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
