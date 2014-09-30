from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.orm.exc import NoResultFound

from . import Base, DBSession

from datetime import datetime
from passlib.apps import custom_app_context as pwd_context

from pyramid.security import Allow, Everyone, Authenticated

import logging
log = logging.getLogger(__name__)


class RootFactory(object):
    __acl__ = [
        (Allow, Everyone, 'everybody'),
        (Allow, 'users', 'logged'),
        (Allow, 'admin', ('edit', 'admin'))]

    def __init__(self, request):
        pass


def groupfinder(username, request):
    """Placeholder groupfinder"""
    user = User.get(username)
    return ["users"]


class WrongUsername(Exception):
    pass


class WrongPassword(Exception):
    pass


class User(Base):
    __tablename__ = 'users'

    username = Column(Unicode(), primary_key=True)
    password = Column(Unicode(), nullable=True)

    created = Column(DateTime, default=datetime.utcnow())

    def __init__(self, username, password):
        self.username = username

        if password is not None:
            self.password = pwd_context.encrypt(password)

    @classmethod
    def get(cls, username):
        return DBSession.query(User).filter(User.username==username).one()

    @classmethod
    def authenticate(cls, username, password):
        try:
            u = User.get(username)
        except NoResultFound:
            raise WrongUsername()

        if pwd_context.verify(password, u.password):
            return u
        else:
            raise WrongPassword()
