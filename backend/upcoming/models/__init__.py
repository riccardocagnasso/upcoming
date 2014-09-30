from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension
from datetime import *

from sqlalchemy_searchable import make_searchable


DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))


class Base(object):
    @classmethod
    def list(cls):
        query = DBSession.query(cls)

        return query

    @classmethod
    def get_all_columns(cls):
        if cls == Base:
            return []
        else:
            return cls.__table__.columns + cls.__bases__[0].get_all_columns()

    def __iter__(self):
        def convert_datetime(value):
            return value.strftime("%Y-%m-%d %H:%M:%S")

        def convert_date(value):
            return value.strftime("%Y-%m-%d")

        columns = self.__class__.get_all_columns()

        for c in columns:
            if getattr(self, c.name) is None:
                value = None
            elif isinstance(c.type, DateTime):
                value = convert_datetime(getattr(self, c.name))
            elif isinstance(c.type, Date):
                value = convert_date(getattr(self, c.name))
            else:
                value = getattr(self, c.name)

            yield(c.name, value)

    @classmethod
    def create(cls, data, user=None, add=True):
        import inspect
        argspec = inspect.getargspec(cls.__init__)
        args = argspec.args

        if argspec.defaults is not None:
            defaults = list(argspec.defaults)
        else:
            defaults = []

        callarguments = {}
        while True:
            try:
                arg = args.pop()
            except IndexError:
                break

            if arg != 'self':
                try:
                    callarguments[arg] = data.get(arg, defaults.pop())
                except IndexError:
                    callarguments[arg] = data[arg]

        obj = cls(**callarguments)

        if add:
            DBSession.add(obj)
        return obj

    def edit(self, data):
        for prop in class_mapper(self.__class__).iterate_properties:
            if isinstance(prop, ColumnProperty):
                if prop.key in data:
                    setattr(self, prop.key, data[prop.key])
            elif isinstance(prop, RelationshipProperty):
                if prop.key in data:
                    r = getattr(self, prop.key)
                    r.clear()
                    for child in data[prop.key]:
                        r.set(prop.argument.create(child, add=False))

Base = declarative_base(cls=Base)

make_searchable()

from .upcomings import *
from .users import *
