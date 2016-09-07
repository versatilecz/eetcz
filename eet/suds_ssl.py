import requests
from suds.transport.http import HttpAuthenticated
from suds.transport import Reply, TransportError

class RequestsTransport(HttpAuthenticated):
    def __init__(self, **kwargs):
        self.cert = kwargs.pop('cert', None)
        # super won't work because not using new style class
        HttpAuthenticated.__init__(self, **kwargs)

    def send(self, request):
        self.addcredentials(request)
        resp = requests.post(request.url, data=request.message,
                             headers=request.headers, cert=self.cert)
        result = Reply(resp.status_code, resp.headers, resp.content)
        return result
