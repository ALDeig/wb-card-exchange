import sqlalchemy as sa

from app.src.services.db.dao.base_dao import BaseDao
from app.src.services.db.models import User


class UserDao(BaseDao[User]):
    model = User

    async def count(self, **filter_by) -> int:
        query = sa.select(sa.func.count(self.model.id)).filter_by(**filter_by)
        response = await self._session.execute(query)
        return response.scalar_one()
