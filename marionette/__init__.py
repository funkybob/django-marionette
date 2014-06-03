
from cgi import parse_header
import json

from django.http import HttpResponse, Http404
from django.views.decorators.http import require_POST
from django.core.serializers.json import DjangoJSONEncoder


RPC_MARKER = '_rpc'


class Resource(object):

    def __init__(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs

    @classmethod
    def as_view(cls):
        @require_POST
        def view(request, *args, **kwargs):
            self = cls(request, *args, **kwargs)
            return self.dispatch(request)
        return view

    def dispatch(self, request):
        method = request.META.get('HTTP_X_RPC_ACTION', '')
        func = getattr(self, method, None)
        if not getattr(func, RPC_MARKER, False):
            return HttpResponse(status=412)

        data = self.get_request_data(request)

        resp = self.execute(func, data)
        jsonified_resp = json.dumps(resp, cls=DjangoJSONEncoder)

        return HttpResponse(jsonified_resp, content_type='application/json')

    def execute(self, handler, data):
        '''Helpful hook to ease wrapping the handler'''
        return handler(**data)

    def get_request_data(self, default=None):
        '''Retrieve data from request'''
        c_type, _ = parse_header(self.request.META.get('CONTENT_TYPE', ''))
        if c_type in ['application/json', 'text/json']:
            if not self.request.body:
                return default
            return json.loads(self.request.body)
        return self.request.POST


def rpc(view):
    '''Mark a view as accessible via RPC'''
    setattr(view, RPC_MARKER, True)
    return view
