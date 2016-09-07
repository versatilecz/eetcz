
class Config(object):

    def __init__(self, **kwargs):
        self.debug = kwargs.get('debug', True)


    def getURL(self):
        if self.debug:
            return 'https://pg.eet.cz/eet/services/EETServiceSOAP/v3/?wsdl'

        return None

