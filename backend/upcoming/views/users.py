from pyramid.view import view_config
from pyramid.httpexceptions import *

from ..models import *
from ..models.forms import *
from . import *

import logging
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

    jwt_secret = request.registry.settings.get('jwt_secret')
    return {
        'success': True,
        'token': jwt.encode({"username": u.username}, jwt_secret).decode()
    }
