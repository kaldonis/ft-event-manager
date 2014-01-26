from app.models.database import DBObject


class BotCategory(DBObject):
    code = None
    name = None

    EDITABLE_FIELDS = ['code', 'name']

    def to_dict(self):
        """
        to dict
        """
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name
        }