from src.app.models.database import DBObject


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