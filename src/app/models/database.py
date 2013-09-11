import sqlite3
import logging

from src.app.constants import CONSTANTS


class DBObject(object):
    """
    parent class for all database based objects
    """
    rowid = None
    db = None

    def __init__(self):
        self.db = DataInterface(CONSTANTS.DB_NAME)

    def attribute_values(self):
        attr_and_values = ((attr, getattr(self, attr)) for attr in dir(self) if not attr.startswith("__") and attr != 'db' and attr != 'rowid')
        return {attr: value for attr, value in attr_and_values if not callable(value)}

    @classmethod
    def get_all(cls, **kwargs):
        db = DataInterface(CONSTANTS.DB_NAME)
        return [cls(**item) for item in db.fetch_all(cls.__name__, kwargs.get('order')) if item]

    @classmethod
    def get_by_id(cls, rowid):
        db = DataInterface(CONSTANTS.DB_NAME)
        sql = "SELECT * FROM %s WHERE id = %d" % (cls.__name__, rowid)
        result = db.fetch_one(sql)
        return cls(**result) if result else None

    def put(self):
        attribute_values = self.attribute_values()
        if self.rowid:
            sql = "UPDATE %s SET %s WHERE id = %d" \
                  % (self.__class__.__name__, ', '.join(["%s=?" % key for key in attribute_values.keys()]), self.rowid)
        else:
            sql = "INSERT INTO %s (%s) VALUES (%s)" \
                  % (self.__class__.__name__, ', '.join(attribute_values.keys()), ', '.join(["?" for _ in attribute_values.values()]))
        rowid = self.db.execute(sql, attribute_values.values())
        if rowid:
            self.rowid = rowid


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
            return cursor.lastrowid