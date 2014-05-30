
from cgi import parse_header
import json

from django.http import HttpResponse, Http404

RPC_MARKER = '_rpc'


class Resource(object):

    def __init__(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs

    @classmethod
    def as_view(cls):
        def view(request, *args, **kwargs):
            self = cls(request, *args, **kwargs)
            return self.dispatch(request)
        return view

    def dispatch(self, request):
        method = request.META['HTTP_X_RPC_ACTION']
        func = getattr(self, method, None)
        if not getattr(func, RPC_MARKER, True):
            raise Http404

        data = self.get_request_data(request)

        resp = func(data)

        return HttpResponse(json.dumps(resp), content_type='application/json')

    def get_request_data(self, default=None):
        '''Retrieve data from request'''
        c_type, _ = parse_header(self.request.META.get('CONTENT_TYPE', ''))
        if c_type in ['application/json', 'text/json']:
            if not self.request.body:
                return default
            return self.loads(self.request.body)
        if self.request.method == 'GET':
            return self.request.GET
        return self.request.POST


def rpc(view):
    '''Mark a view as accessible via RPC'''
    setattr(view, '_rpc', True)
    return view
