import json
from app.models.database import DBObject


class Bot(DBObject):
    bid = None
    registered_ind = None
    event_id = None
    name = None
    team_name = None
    team_email = None
    team_city = None
    team_state = None
    category = None
    weightclass = None
    primary_freq = None
    secondary_freq = None
    multibot_ind = None
    notes = None
    photo_url = None
    seed_number = None
    bracket_id = None

    def register(self):
        """
        registers the bot
        """
        sql = "UPDATE %s SET registered_ind = 'Y' WHERE id = %d" % (self.__class__.__name__, self.id)
        return self.db.execute(sql)

    def unregister(self):
        """
        unregisters the bot
        """
        sql = "UPDATE %s SET registered_ind = 'N' WHERE id = %d" % (self.__class__.__name__, self.id)
        return self.db.execute(sql)
    
    def to_dict(self):
        return {
                'id': self.id,
                'botName': self.name,
                'teamName': self.team_name,
                'teamEmail': self.team_email,
                'teamCity': self.team_city,
                'teamState': self.team_state,
                'category': self.category,
                'weightclass': self.weightclass,
                'photoUrl': self.photo_url,
                'multibot': True if self.multibot_ind == 'Y' else False,
                'isRegistered': True if self.registered_ind == 'Y' else False
        }