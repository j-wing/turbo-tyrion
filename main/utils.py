import json
from django.http import HttpResponse

class JSONResponse(HttpResponse):
    def __init__(self, data, *args, **kwargs):
        kwargs['content_type'] = kwargs.get('content_type', 'application/json')
        super(JSONResponse, self).__init__(json.dumps(data), *args, **kwargs)