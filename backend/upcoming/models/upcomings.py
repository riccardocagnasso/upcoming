from sqlalchemy import *
from sqlalchemy.orm import relationship

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

    created = Column(DateTime, default=datetime.utcnow())
    username = Column(Unicode, ForeignKey(
        'users.username',
        onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False)
    user = relationship('User', backref='upcomings')

    suscribed_users = relationship('User', secondary=subscriptions_table,
                                   backref='subscriptions')

    def __init__(self, name, description, date, username):
        self.name = name
        self.description = description
        self.date = date
        self.username = username

    @classmethod
    def get(cls, id):
        return DBSession.query(Upcoming).filter(Upcoming.id==id).one()
