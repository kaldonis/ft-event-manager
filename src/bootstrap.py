import os
import sqlite3
from webapp2 import redirect, uri_for
from app.domain.constants import CONSTANTS
from app.handlers.base import BaseHandler

BOOTSTRAP_CREATE_TABLES = """
    CREATE TABLE bot (
            id integer primary key autoincrement
            ,event_id not null references event(id)
            ,name text not null
            ,team_name text not null
            ,team_email text
            ,team_city text
            ,team_state text
            ,category text references botcategory(code)
            ,weightclass text references weightclass(code)
            ,primary_freq text
            ,secondary_freq text
            ,multibot_ind text not null default 'N'
            ,notes text
            ,photo_url text
            ,bid integer not null default 0
            ,registered_ind text not null default 'N'
            ,bracket_id integer references bracket(id)
            ,seed_number integer
    );
    CREATE TABLE "botcategory" (
            id integer primary key autoincrement
            ,code text not null unique
            ,name text not null
    );
    CREATE TABLE "bracket" (
            id integer primary key autoincrement
            ,event_id integer not null references event(id)
            ,match_length real not null
            ,format_code text not null references format(code)
            ,weightclass_code text not null
            ,name text not null
            ,manual_seed boolean not null default 0
            ,generated boolean not null default 0
    );
    CREATE TABLE "bracketsession" (
            bracket_id integer not null references bracket(id)
            ,session_id integer not null references session(id)
    );
    CREATE TABLE "event" (
            id integer primary key autoincrement
            ,name text not null unique
            ,start_date text not null
            ,end_date text not null
            ,location text
    );
    CREATE TABLE "match" (
            id integer primary key autoincrement
            ,round text
            ,number integer
            ,bracket_id integer
            ,bracket_side text
            ,session_id integer
            ,time text
            ,bot1_id integer
            ,bot2_id integer
            ,bot1_status_code text references botstatus(code)
            ,bot2_status_code text references botstatus(code)
            ,winning_bot_id integer
            ,bot1_source_match text
            ,bot2_source_match text
    );
    CREATE TABLE "matchjudgeresult" (
            id integer primary key autoincrement
            ,judge_criteria_code text not null references judgecriteria(code)
            ,match_id integer not null references match(id)
            ,bot1_score integer not null
            ,bot2_score integer not null
    );
    CREATE TABLE "session" (
            id integer primary key autoincrement
            ,event_id integer not null references event(id)
            ,date text not null
            ,start_time text not null
            ,end_time text not null
            ,match_gap integer not null default 180
    );
    CREATE TABLE "weightclass" (
            id integer primary key autoincrement
            ,code text not null unique
            ,name text not null
            ,description text not null
            ,default_match_length real not null
    );
"""

BOOTSTRAP_CREATE_BOT_CATEGORIES = """
    INSERT INTO botcategory (code, name) values ('Sumo', 'Sumo');
    INSERT INTO botcategory (code, name) values ('Combat', 'Combat');
"""

BOOTSTRAP_CREATE_WEIGHTCLASSES = """
    INSERT INTO weightclass (code, name, description, default_match_length)
                     VALUES ('1kg', 'Kilobot', 'Weight <= 1kg', 3.0);
    INSERT INTO weightclass (code, name, description, default_match_length)
                     VALUES ('Antweight', 'Antweight', 'Weight <= 1lb', 3.0);
    INSERT INTO weightclass (code, name, description, default_match_length)
                     VALUES ('Beetleweight', 'Beetleweight', 'Weight <= 3lb', 3.0);

"""

def bootstrap():
    if os.path.exists(CONSTANTS.DB_NAME):
        os.remove(CONSTANTS.DB_NAME)

    database = sqlite3.connect(CONSTANTS.DB_NAME)
    cursor = database.cursor()

    cursor.executescript(BOOTSTRAP_CREATE_TABLES)
    cursor.executescript(BOOTSTRAP_CREATE_BOT_CATEGORIES)
    cursor.executescript(BOOTSTRAP_CREATE_WEIGHTCLASSES)

class Bootstrap(BaseHandler):
    def get(self):
        bootstrap()
        return redirect(uri_for('home'))