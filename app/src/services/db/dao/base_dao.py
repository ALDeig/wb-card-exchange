from typing import Generic, Sequence, TypeVar


import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.sqlite import insert

from app.src.services.db.base import Base


TypeModel = TypeVar("TypeModel", bound=Base)


class BaseDao(Generic[TypeModel]):
    model: type[TypeModel]

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_all(self, **filter_by) -> Sequence[TypeModel]:
        query = sa.select(self.model).filter_by(**filter_by)
        response = await self._session.scalars(query)
        return response.all()

    async def find_one_or_none(self, **filter_by) -> TypeModel | None:
        query = sa.select(self.model).filter_by(**filter_by)
        return await self._session.scalar(query)

    async def find_one(self, **filter_by) -> TypeModel:
        query = sa.select(self.model).filter_by(**filter_by)
        response = await self._session.execute(query)
        return response.scalar_one()

    async def add(self, model_instanse: TypeModel) -> TypeModel:
        self._session.add(model_instanse)
        await self._session.commit()
        return model_instanse

    async def insert_or_update(
        self, index_element: str, update_fields: set[str], **data
    ):
        query = (
            insert(self.model)
            .values(**data)
            .on_conflict_do_update(
                index_elements=[index_element],
                set_={
                    key: data["key"] for key in update_fields if key in update_fields
                },
            )
        )
        await self._session.execute(query)
        await self._session.commit()

    async def insert_or_nothing(self, index_element: str, **data):
        query = (
            insert(self.model)
            .values(**data)
            .on_conflict_do_nothing(index_elements=[index_element])
        )
        await self._session.execute(query)
        await self._session.commit()

    async def update(self, update_fields: dict, **filter_by) -> None:
        query = sa.update(self.model).values(**update_fields).filter_by(**filter_by)
        await self._session.execute(query)
        await self._session.commit()

    async def delete(self, **filter_by) -> None:
        query = sa.delete(self.model).filter_by(**filter_by)
        await self._session.execute(query)
        await self._session.commit()
