from app.domain.constants import CONSTANTS
from app.models import BracketSearchMixin, DataInterface
from app.models.database import DBObject

class Match(DBObject, BracketSearchMixin):
    number = None
    bracket_id = None
    session_id = None
    bracket_side = None
    time = None
    round = None
    bot1_id = None
    bot2_id = None
    bot1_status_code = None
    bot2_status_code = None
    winning_bot_id = None
    bot1_source_match = None
    bot2_source_match = None

    @classmethod
    def get_by_bracket_round(cls, bracket_id, round):
        db = DataInterface(CONSTANTS.DB_NAME)
        sql = "SELECT * FROM %s WHERE bracket_id = %d and round='%s' ORDER BY number" % (cls.__name__, int(bracket_id), round)

        results = db.fetch_multiple(sql)
        return [cls(**(item)) for item in results if item]

    @classmethod
    def get_by_bracket_source_match(cls, bracket_id, source_match):
        db = DataInterface(CONSTANTS.DB_NAME)
        sql = "SELECT * FROM %s WHERE bracket_id = %d AND (bot1_source_match = '%s' OR bot2_source_match = '%s')" % (cls.__name__, int(bracket_id), source_match, source_match)

        result = db.fetch_one(sql)
        return cls(**(result)) if result else None

    def populate_bot_entities(self):

        from app.models.bot import Bot
        # add bot1 and bot2 objects
        if self.bot1_id:
            self.bot1 = Bot.get_by_id(self.bot1_id)
        elif self.bot1_id == 0:
            self.bot1 = Bot.bye()
        else:
            self.bot1 = None

        if self.bot2_id:
            self.bot2 = Bot.get_by_id(self.bot2_id)
        elif self.bot2_id == 0:
            self.bot2 = Bot.bye()
        else:
            self.bot2 = None

        if self.winning_bot_id:
            self.winning_bot = Bot.get_by_id(self.winning_bot_id)
        else:
            self.winning_bot = None

    def check(self):
        """
        see if we can determine a winner based on byes
        """
        if self.bot1_id == 0 and self.bot2_id:
            self.winner(self.bot2_id)
        elif self.bot2_id == 0 and self.bot1_id:
            self.winner(self.bot1_id)
        elif self.bot1_id == 0 and self.bot2_id == 0:
            self.winner(0)

    def winner(self, winning_bot_id):
        """
        declare a bot the winner, update matches accordingly
        """
        self.winning_bot_id = int(winning_bot_id)
        self.put()

        losing_bot = self.bot2_id if self.bot1_id == self.winning_bot_id else self.bot1_id

        match_to_update = Match.get_by_bracket_source_match(self.bracket_id, "W%s%d" % (self.round, self.number))
        if match_to_update:
            if match_to_update.bot1_source_match == "W%s%d" % (self.round, self.number):
                match_to_update.bot1_id = self.winning_bot_id
            else:
                match_to_update.bot2_id = self.winning_bot_id
            match_to_update.put()
            match_to_update.check()

        match_to_update = Match.get_by_bracket_source_match(self.bracket_id, "L%s%d" % (self.round, self.number))
        if match_to_update:
            if match_to_update.bot1_source_match == "L%s%d" % (self.round, self.number):
                match_to_update.bot1_id = losing_bot
            else:
                match_to_update.bot2_id = losing_bot
            match_to_update.put()
            match_to_update.check()