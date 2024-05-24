from app.src.services.db.dao.base_dao import BaseDao
from app.src.services.db.models import Card


class CardDao(BaseDao[Card]):
    model = Card
