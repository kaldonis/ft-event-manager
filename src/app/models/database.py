import sqlite3
import logging

from app.domain.constants import CONSTANTS


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
        attr_and_values = ((attr, getattr(self, attr)) for attr in dir(self) if not attr.startswith("__") and attr != 'db' and attr != 'id' and attr != 'EDITABLE_FIELDS')
        return {attr: value for attr, value in attr_and_values if not callable(value)}

    @classmethod
    def get_all(cls, order=None):
        db = DataInterface(CONSTANTS.DB_NAME)
        return [cls(**item) for item in db.fetch_all(cls.__name__, order) if item]

    @classmethod
    def get_multiple(cls, sql):
        db = DataInterface(CONSTANTS.DB_NAME)
        return [cls(**item) for item in db.fetch_multiple(sql) if item]

    @classmethod
    def get_single(cls, sql):
        db = DataInterface(CONSTANTS.DB_NAME)
        item = db.fetch_one(sql)
        return cls(**item) if item else None

    @classmethod
    def get_by_id(cls, id):
        if isinstance(id, basestring):
            id = int(id)
        db = DataInterface(CONSTANTS.DB_NAME)
        sql = "SELECT * FROM %s WHERE id = %d" % (cls.__name__, id)
        result = db.fetch_one(sql)
        return cls(**result) if result else None

    def delete(self):
        sql = "DELETE FROM %s WHERE id = %d" % (self.__class__.__name__, int(self.id))
        return self.db.delete(sql)

    def put(self):
        attribute_values = self.attribute_values()
        if self.id:
            sql = "UPDATE %s SET %s WHERE id = %d" \
                  % (self.__class__.__name__, ', '.join(["%s=?" % key for key in attribute_values.keys()]), int(self.id))
        else:
            sql = "INSERT INTO %s (%s) VALUES (%s)" \
                  % (self.__class__.__name__, ', '.join(attribute_values.keys()), ', '.join(["?" for _ in attribute_values.values()]))
        id = self.db.put(sql, attribute_values.values())
        if id:
            self.id = id
        else:
            return id

    def to_dict(self):
        return self.__dict__


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
        try:
            with self.database:
                cursor = self.database.cursor()
                if order:
                    order = 'order by %s' % order
                sql = "SELECT * FROM %s %s" % (entity, order)
                logging.info("Fetch all: %s" % sql)
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as e:
            logging.error(e.message)
            return e.message

    def fetch_multiple(self, sql):
        try:
            with self.database:
                cursor = self.database.cursor()
                logging.info("Fetch multiple: %s" % sql)
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as e:
            logging.error(e.message)
            return e.message

    def fetch_one(self, sql):
        try:
            with self.database:
                cursor = self.database.cursor()
                logging.info("Fetch one: %s" % sql)
                cursor.execute(sql)
                return cursor.fetchone()
        except Exception as e:
            logging.error(e.message)
            return e.message

    def put(self, sql, values=None):
        try:
            with self.database:
                cursor = self.database.cursor()
                logging.info("Execute: %s" % sql)
                logging.info("Values: %s" % values)
                cursor.execute(sql, values)
                return cursor.lastrowid
        except Exception as e:
            logging.error(e.message)
            return e.message

    def execute(self, sql):
        try:
            with self.database:
                cursor = self.database.cursor()
                logging.info("Execute: %s" % sql)
                cursor.execute(sql)
        except Exception as e:
            logging.error(e.message)
            return e.message

    def delete(self, sql):
        try:
            with self.database:
                cursor = self.database.cursor()
                logging.info("Delete: %s" % sql)
                cursor.execute(sql)
        except Exception as e:
            logging.error(e.message)
            return e.message

