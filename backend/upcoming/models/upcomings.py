from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import TSVectorType
from sqlalchemy_searchable import search
from sqlalchemy.orm.collections import attribute_mapped_collection

import short_url

from . import Base, DBSession

from datetime import datetime

import logging
log = logging.getLogger(__name__)


subscriptions_table = Table(
    'subscriptions', Base.metadata,
    Column(
        'username', Unicode,
        ForeignKey('users.username', onupdate="CASCADE",
                   ondelete="CASCADE", primary_key=True)),
    Column(
        'upcoming_id', Integer,
        ForeignKey('upcomings.id', onupdate="CASCADE",
                   ondelete="CASCADE", primary_key=True))
)


class Upcoming(Base):
    __tablename__ = 'upcomings'

    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(Unicode)
    description = Column(Unicode)
    date = Column(DateTime)
    website = Column(Unicode)

    created = Column(DateTime, default=datetime.utcnow())
    username = Column(Unicode, ForeignKey(
        'users.username',
        onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False)
    user = relationship('User', backref='upcomings')

    suscribed_users = relationship(
        'User', secondary=subscriptions_table,
        backref='subscriptions',
        collection_class=attribute_mapped_collection('username'))

    search_vector = Column(TSVectorType('name', 'description'))

    def __init__(self, name, description, date, username, url):
        self.name = name
        self.description = description
        self.date = date
        self.username = username
        self.url = url

    @classmethod
    def get(cls, id):
        return DBSession.query(Upcoming).filter(Upcoming.id==id).one()

    @classmethod
    def list(self, searchquery=None):
        query = super(Upcoming, self).list()

        if searchquery:
            query = search(query, searchquery)

        return query

    def __iter__(self):
        for e in super(Upcoming, self).__iter__():
            yield e

        yield 'date', self.date.timestamp() * 1e3
        yield 'shortUrl', short_url.encode_url(self.id)

    def rich_to_dict(self, username=None):
        d = dict(self)

        if username:
            d['subscribed'] = username in self.suscribed_users

        return d
