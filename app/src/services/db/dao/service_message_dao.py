from app.src.services.db.dao.base_dao import BaseDao
from app.src.services.db.models import Settings


class ServiceMessageDao(BaseDao[Settings]):
    model = Settings
