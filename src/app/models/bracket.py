from app.domain.constants import CONSTANTS
from app.models import EventSearchMixin
from app.models.database import DBObject, DataInterface


class Bracket(DBObject, EventSearchMixin):
    event_id = None
    match_length = None
    format_code = None
    weightclass_code = None

    @classmethod
    def get_by_event_and_class(cls, event_id, weightclass_code):
        db = DataInterface(CONSTANTS.DB_NAME)
        sql = "SELECT * FROM %s WHERE event_id = %d AND weightclass_code = '%s'" % (cls.__name__, int(event_id), weightclass_code)
        result = db.fetch_one(sql)

        return cls(**(result)) if result else None