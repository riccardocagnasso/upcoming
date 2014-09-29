from pyramid.view import view_config
from pyramid.httpexceptions import *

from ..models import *
from . import *

import logging
log = logging.getLogger(__name__)

@view_config(route_name='upcomings', renderer='json')
@cors
def uploadimage(request):
    return {
        'upcomings': list(map(dict, Upcoming.list()))
    }
