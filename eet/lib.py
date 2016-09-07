from suds.client import Client
from suds_ssl import RequestsTransport
import logging
logging.basicConfig(level=logging.DEBUG)

class EET(object):

    def __init__(self, config):
        self.transport = RequestsTransport(cert=('01000003.pem', '01000003.key'))
        self.client = Client(url=config.getURL(), transport=self.transport)

