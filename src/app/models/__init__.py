from app.domain.constants import CONSTANTS
from app.models.database import DBObject, DataInterface


class BracketSearchMixin(object):
    @classmethod
    def get_by_bracket(cls, bracket_id, order=None):
        db = DataInterface(CONSTANTS.DB_NAME)
        sql = "SELECT * FROM %s WHERE bracket_id = %d" % (cls.__name__, int(bracket_id))
        if order:
            sql = "%s ORDER BY %s" % (sql, order)
        return [cls(**(item)) for item in db.fetch_multiple(sql)]


class EventSearchMixin(object):
    @classmethod
    def get_by_event(cls, event_id, order=None):
        sql = "SELECT * FROM %s WHERE event_id = %d" % (cls.__name__, event_id)
        if order:
            sql = "%s ORDER BY %s" % (sql, order)
        return cls.get_multiple(sql)


class WeightclassEventSearchMixin(object):
    @classmethod
    def get_by_weightclass(cls, weightclass_code, event_id, order=None):
        sql = "SELECT * FROM %s WHERE weightclass = '%s' AND event_id = %d" % (cls.__name__, weightclass_code, event_id)
        if order:
            sql = "%s ORDER BY %s" % (sql, order)
        return cls.get_multiple(sql)


class CodeSearchMixin(object):
    @classmethod
    def get_by_code(cls, code, order=None):
        sql = "SELECT * FROM %s WHERE code = '%s'" % (cls.__name__, code)
        if order:
            sql = "%s ORDER BY %s" % (sql, order)
        return cls.get_single(sql)