from pyramid.view import view_config
from pyramid.httpexceptions import *

from ..models import *
from ..models.forms import *

import logging
log = logging.getLogger(__name__)

from pyramid.httpexceptions import HTTPUnauthorized

from colander import Invalid

import jwt


@view_config(route_name='login', renderer='json')
def login(request):
    print(request.params)
    try:
        appstruct = login_schema.deserialize(request.params)
    except Invalid:
        log.debug('invalid')
        return HTTPUnauthorized()
    except ValueError:
        return HTTPUnauthorized()

    log.debug(appstruct)

    try:
        u = User.authenticate(appstruct.get('username'),
                              appstruct.get('password'))
    except WrongUsername:
        log.debug('wrong username')
        return HTTPUnauthorized()
    except WrongPassword:
        log.debug('wrong password')
        return HTTPUnauthorized()

    str = jwt.encode({"username": u.username}, "secret_pass").decode()
    log.debug(jwt.decode(str, "secret_pass"))

    return jwt.encode({"username": u.username}, "secret_pass").decode()
