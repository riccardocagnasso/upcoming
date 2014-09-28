from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from pyramid.authorization import ACLAuthorizationPolicy
from pyramid_jwtauth import JWTAuthenticationPolicy

from .models import DBSession, Base, groupfinder, RootFactory

import logging
log = logging.getLogger(__name__)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)

    authentication = JWTAuthenticationPolicy(master_secret='secret_pass',
                                             find_groups=groupfinder)
    authorization = ACLAuthorizationPolicy()

    config = Configurator(settings=settings, root_factory=RootFactory,
                          authentication_policy=authentication,
                          authorization_policy=authorization)

    config.add_route('upcomings', '/api/upcomings')
    config.add_route('login', '/api/login')

    config.scan()

    return config.make_wsgi_app()

from pyramid.events import NewResponse
from pyramid.events import subscriber

@subscriber(NewResponse)
def access_control_allow_origin_enable(event):
    event.response.headers['Access-Control-Allow-Origin'] = '*'
    event.response.headers['Access-Control-Allow-Methods'] = '*'
