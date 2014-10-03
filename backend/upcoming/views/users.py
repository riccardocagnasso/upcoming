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

from oauth2client.client import *
import httplib2

from sqlalchemy.orm.exc import NoResultFound


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


@view_config(route_name='login.google', renderer='json')
@cors
def loginGoogle(request):
    access_token = request.json_body.get('access_token')
    credentials = AccessTokenCredentials(access_token,
                                         'upcoming-user-agent/0.1')
    log.debug(credentials)
    http = httplib2.Http()
    http = credentials.authorize(http)
    resp, cred = http.request('https://www.googleapis.com/oauth2/v1/userinfo')
    log.debug(resp)
    cred = json.loads(cred.decode())
    #cred = json.loads(cred)

    email = cred.get('email')

    try:
        user = User.get(email)
    except NoResultFound:
        user = User.create({
            'username': email
        })

    jwt_secret = request.registry.settings.get('jwt_secret')
    return {
        'success': True,
        'token': jwt.encode({"username": user.username}, jwt_secret).decode(),
        'username': user.username
    }
