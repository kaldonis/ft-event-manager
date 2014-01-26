from app.domain.constants import CONSTANTS
from app.models import CodeSearchMixin
from app.models.database import DBObject, DataInterface


class Weightclass(DBObject, CodeSearchMixin):
    code = None
    name = None
    description = None
    default_match_length = None

    EDITABLE_FIELDS = ['code', 'default_match_length', 'description', 'name']

    @classmethod
    def get_by_event(cls, event_id, order=None):
        db = DataInterface(CONSTANTS.DB_NAME)
        sql = "SELECT distinct w.* FROM weightclass w, bot b WHERE b.event_id = %d AND b.weightclass = w.code AND b.registered_ind = 'Y' ORDER BY w.code ASC" % int(event_id)

        results = db.fetch_multiple(sql)
        return [cls(**(item)) for item in results if item]

    def to_dict(self):
        """
        to dict
        """
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'description': self.description,
            'default_match_length': self.default_match_length
        }