from deform import Form, ValidationFailure
from ..models import *
from ..models.forms import *
from pyramid.httpexceptions import HTTPNotFound, HTTPOk
import json
import transaction

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from colander import Invalid

import logging
log = logging.getLogger(__name__)


class cors(object):
    def __init__(self, f):
        self.f = f

    def __call__(self, request):
        if request.method == 'OPTIONS':
            return HTTPOk()
        else:
            return self.f(request)

class RESTView(object):

    def __init__(self, request):
        self.request = request

    def __call__(self):
        if self.request.method == 'GET':
            return self.get(self.request)
        elif self.request.method == 'PUT':
            return self.put(self.request)
        elif self.request.method == 'POST':
            return self.post(self.request)
        elif self.request.method == 'DELETE':
            return self.delete(self.request)
        else:
            return HTTPNotFound()

    def get(self, request):
        pass

    def put(self, request):
        pass

    def post(self, request):
        pass

    def delete(self, request):
        pass


class AutomaticRESTView(RESTView):
    #placeholder, to be overridden
    model = None
    #colander schema
    schema = None

    def get(self, request):
        id = request.matchdict.get('id')

        if id is not None and id != 'undefined':
            data = [dict(self.model.get(id))]
            count = 1
        else:
            filters = json.loads(request.params.get('filter', '[]'))
            order = json.loads(request.params.get('sort', '[]'))
            v = filter_page_schema.deserialize(request.params)
            v['filter'] = filters
            v['order'] = order
            result_query = self.model.list(v['filter'], v['order'])

            if v['limit'] > 0:
                data = list(
                    map(dict, result_query[v['start']:v['page']*v['limit']]))
            else:
                data = list(map(dict, result_query.all()))

            count = result_query.count()

        return {'success': True,
                'message': 'data loaded',
                'data': data,
                'total': count}

    def put(self, request):
        id = request.matchdict.get('id')
        obj = self.model.get(id)

        try:
            obj.edit(self.schema.deserialize(request.json_body))
        except Invalid as i:
            request.response.status_int = 400
            return {'success': False,
                    'message': ", ".join([k + ": " + v
                                         for k, v in i.asdict().items()])}
        try:
            transaction.commit()
        except IntegrityError as e:
            request.response.status_int = 400
            transaction.abort()
            return {'success': False,
                    'message': e.message}

        return {'success': True}

    def post(self, request):
        try:
            appstruct = self.schema.deserialize(request.json_body)
        except Invalid as i:
            return {'success': False,
                    'message': ", ".join([k + ": " + v
                                         for k, v in i.asdict().items()])}

        self.model.create(appstruct, authenticated_userid(request))

        try:
            transaction.commit()
        except IntegrityError as e:
            request.response.status_int = 400
            transaction.abort()
            return {'success': False,
                    'message': e.message}

        return {'success': True}

    def delete(self, request):
        id = request.matchdict.get('id')
        u = self.model.get(id)
        DBSession.delete(u)
        transaction.commit()
        return {'success': True}
