from sqlalchemy import *
from sqlalchemy.orm import relationship

from . import Base, DBSession

from datetime import datetime, timedelta

import logging
log = logging.getLogger(__name__)


class Upcoming(Base):
    __tablename__ = 'upcomings'

    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(Unicode)
    description = Column(Unicode)
    date = Column(DateTime)

    created = Column(DateTime, default=datetime.utcnow())
    username = Column(Unicode, ForeignKey('users.username',
                      onupdate="CASCADE", ondelete="CASCADE"),
                      nullable=False)
    user = relationship('User', backref='upcomings')

    def __init__(self, name, description, date, username):
        self.name = name
        self.description = description
        self.date = date
        self.username = username
