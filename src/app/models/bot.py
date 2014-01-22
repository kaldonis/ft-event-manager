from app.domain.constants import CONSTANTS
from app.models import EventSearchMixin, WeightclassEventSearchMixin, DataInterface
from app.models.database import DBObject


class Bot(DBObject, EventSearchMixin, WeightclassEventSearchMixin):
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

    @classmethod
    def get_by_bracket_seed(cls, event_id, bracket_id, seed):
        db = DataInterface(CONSTANTS.DB_NAME)
        sql = "SELECT * FROM %s WHERE event_id = %d AND seed_number = %d AND bracket_id = %d" % (cls.__name__, int(event_id), seed, bracket_id)
        result = db.fetch_one(sql)

        return cls(**(result)) if result else None

    @classmethod
    def get_by_bracket(cls, bracket_id):
        """
        alternative to the method available in BracketSearchMixin, parses through Matches instead
        """
        from app.models.match import Match
        matches = Match.get_by_bracket_round(bracket_id, 'A')
        bots = []
        for match in matches:
            bots += [match.bot1_id, match.bot2_id]

        return [cls.get_by_id(bot_id) for bot_id in bots if bot_id]

    @classmethod
    def bye(cls):
        """
        placeholder bot object for a bye
        """
        params = {
            'name': '--bye--',
            'id': 0
        }
        return cls(**(params))

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