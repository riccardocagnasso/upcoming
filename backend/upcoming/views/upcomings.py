from pyramid.view import view_config
from pyramid.httpexceptions import *

import short_url

from ..models import *
from . import *

import logging
log = logging.getLogger(__name__)


@view_config(route_name='upcomings', renderer='json')
@cors
def upcomings(request):
    return {
        'upcomings': list(map(dict, Upcoming.list()))
    }


@view_config(route_name='my_upcomings', renderer='json')
@cors
def myUpcomings(request):
    userid = request.authenticated_userid
    user = User.get(userid)

    return {
        'upcomings': [u.rich_to_dict(userid) for u in user.subscriptions]
    }


@view_config(route_name='search_upcomings', renderer='json')
@cors
def searchUpcomings(request):
    userid = request.authenticated_userid
    searchquery = request.json_body.get('searchquery', '')

    return {
        'upcomings': [u.rich_to_dict(userid)
                      for u in Upcoming.list(searchquery)]
    }


@view_config(route_name='associate', renderer='json')
@cors
def associate(request):
    upcoming_id = request.json_body.get('id')
    upcoming = Upcoming.get(upcoming_id)

    userid = request.authenticated_userid
    user = User.get(userid)

    user.subscriptions.append(upcoming)

    return {
        'success': True
    }


@view_config(route_name='disassociate', renderer='json')
@cors
def disassociate(request):
    upcoming_id = request.json_body.get('id')
    upcoming = Upcoming.get(upcoming_id)

    userid = request.authenticated_userid
    del upcoming.suscribed_users[userid]

    return {
        'success': True
    }


@view_config(route_name='create_upcoming', renderer='json')
@cors
def create_upcoming(request):
    try:
        appstruct = new_upcoming_schema.deserialize(request.json_body)
    except Invalid as i:
        log.debug(i)
        return {
            'success': False,
            'message': 'invalid data'
        }

    userid = request.authenticated_userid
    user = User.get(userid)

    appstruct['username'] = user.username
    u = Upcoming.create(appstruct)
    u.suscribed_users[userid] = user

    return {
        'success': True
    }


@view_config(route_name="upcoming", renderer="json")
@cors
def upcoming(request):
    userid = request.authenticated_userid

    eid = request.json_body.get('shortUrl', '')
    upcoming = Upcoming.get(short_url.decode_url(eid))

    return {
        'success': True,
        'upcoming': dict(upcoming.rich_to_dict(userid))
    }
