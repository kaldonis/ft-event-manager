from app.models import BracketSearchMixin
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