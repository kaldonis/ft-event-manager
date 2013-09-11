from src.app.models.database import DBObject


class Event(DBObject):
    name = None
    location = None
    start_date = None
    end_date = None

