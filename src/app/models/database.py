import sqlite3
import logging

from src.app.constants import CONSTANTS


class DBObject(object):
    """
    parent class for all database based objects
    """
    id = None
    db = None

    def __init__(self, **kwargs):
        self.db = DataInterface(CONSTANTS.DB_NAME)
        self.__dict__.update(kwargs)

    def attribute_values(self):
        attr_and_values = ((attr, getattr(self, attr)) for attr in dir(self) if not attr.startswith("__") and attr != 'db' and attr != 'id')
        return {attr: value for attr, value in attr_and_values if not callable(value)}

    @classmethod
    def get_all(cls, **kwargs):
        db = DataInterface(CONSTANTS.DB_NAME)
        return [cls(**item) for item in db.fetch_all(cls.__name__, kwargs.get('order')) if item]

    @classmethod
    def get_multiple(cls, sql, **kwargs):
        db = DataInterface(CONSTANTS.DB_NAME)
        return [cls(**item) for item in db.fetch_multiple(sql) if item]

    @classmethod
    def get_by_id(cls, id):
        db = DataInterface(CONSTANTS.DB_NAME)
        sql = "SELECT * FROM %s WHERE id = %d" % (cls.__name__, id)
        result = db.fetch_one(sql)
        return cls(**result) if result else None

    @classmethod
    def get_by_event(cls, event_id, order):
        sql = "SELECT * FROM %s WHERE event_id = %d" % (cls.__name__, event_id)
        if order:
            sql = "%s ORDER BY %s" % (sql, order)
        return cls.get_multiple(sql)

    def put(self):
        attribute_values = self.attribute_values()
        if self.id:
            sql = "UPDATE %s SET %s WHERE id = %d" \
                  % (self.__class__.__name__, ', '.join(["%s=?" % key for key in attribute_values.keys()]), self.id)
        else:
            sql = "INSERT INTO %s (%s) VALUES (%s)" \
                  % (self.__class__.__name__, ', '.join(attribute_values.keys()), ', '.join(["?" for _ in attribute_values.values()]))
        id = self.db.execute(sql, attribute_values.values())
        if id:
            self.id = id


def dict_factory(cursor, row):
    d = {}
    for idx,col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class DataInterface(object):
    """
    class that interacts with the database
    """
    database = None

    def __init__(self, db_name):
        self.database = sqlite3.connect(db_name)
        self.database.row_factory = dict_factory

    def fetch_all(self, entity, order):
        with self.database:
            cursor = self.database.cursor()
            if order:
                order = 'order by %s' % order
            sql = "SELECT * FROM %s %s" % (entity, order)
            logging.info("Fetch all: %s" % sql)
            cursor.execute(sql)
            return cursor.fetchall()

    def fetch_multiple(self, sql):
        with self.database:
            cursor = self.database.cursor()
            logging.info("Fetch multiple: %s" % sql)
            cursor.execute(sql)
            return cursor.fetchall()

    def fetch_one(self, sql):
        with self.database:
            cursor = self.database.cursor()
            logging.info("Fetch one: %s" % sql)
            cursor.execute(sql)
            return cursor.fetchone()

    def execute(self, sql, values):
        with self.database:
            cursor = self.database.cursor()
            logging.info("Execute: %s" %sql)
            cursor.execute(sql, values)
            return cursor.lastid