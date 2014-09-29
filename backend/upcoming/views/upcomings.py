from pyramid.view import view_config
from pyramid.httpexceptions import *

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


@view_config(route_name='my_upcomings', renderer='json', permission='user')
@cors
def myUpcomings(request):
    userid = request.authenticated_userid
    user = User.get(userid)

    log.debug(user)

    return {}


@view_config(route_name='search_upcomings', renderer='json')
@cors
def searchUpcomings(request):
    return {
        'upcomings': list(map(dict, Upcoming.list()))
    }


@cors
def associate(request):
    upcoming_id = request.params.get('id')
    upcoming = Upcoming.get(upcoming_id)