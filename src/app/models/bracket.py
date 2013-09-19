from app.models.database import DBObject


class Bracket(DBObject):
    event_id = None
    match_length = None
    format_code = None
    weightclass_code = None