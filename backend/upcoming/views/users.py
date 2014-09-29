from pyramid.view import view_config
from pyramid.httpexceptions import *

from ..models import *
from ..models.forms import *
from . import *

import logging
import json
log = logging.getLogger(__name__)

from pyramid.httpexceptions import HTTPUnauthorized

from colander import Invalid

import jwt


@view_config(route_name='login', renderer='json')
@cors
def login(request):
    try:
        appstruct = login_schema.deserialize(request.json_body)
    except Invalid:
        return {
            'success': False,
            'message': 'invalid data'
        }
    except ValueError:
        return HTTPUnauthorized()

    try:
        u = User.authenticate(appstruct.get('username'),
                              appstruct.get('password'))
    except WrongUsername:
        return {
            'success': False,
            'message': 'wrong username'
        }
    except WrongPassword:
        return {
            'success': False,
            'message': 'wrong password'
        }

    str = jwt.encode({"username": u.username}, "secret_pass").decode()
    log.debug(jwt.decode(str, "secret_pass"))

    return {
        'success': True,
        'token': jwt.encode({"username": u.username}, "secret_pass").decode()
    }
