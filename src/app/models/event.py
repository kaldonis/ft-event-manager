from src.app.models.database import DataInterface, DBObject


class Event(DBObject):
    name = None
    location = None
    start_date = None
    end_date = None

    def __init__(self, **kwargs):
        super(Event, self).__init__()
        self.rowid = kwargs.get('id')
        self.name = kwargs.get('name')
        self.location = kwargs.get('location')
        self.start_date = kwargs.get('start_date')
        self.end_date = kwargs.get('end_date')

