import datetime
from uuid import uuid4
from lxml import etree
from eet.utils import *

class EETRequestHeader(object):

    def __init__(self, config, **kwargs):
        self.config = config
        self.uuid = kwargs.get('uuid', uuid4()) #uuid zpravy
        self.date = kwargs.get('date', datetime.datetime.now()) #datum zaslani trzby

        self.first_send = kwargs.get('first_send', True) # pokud se posila poprve

    def getUUID(self):
        return unicode(self.uuid)

    def getDate(self):
        return formatDate(self.date)

    def getFirstSend(self):
        if self.first_send:
            return 'true'
        return 'false'

    def getDebug(self):
        if self.config.debug:
            return 'true'
        return 'false'

    def validate(self):
        return True

    def element(self):
        if self.uuid is None or self.date is None or self.first_send is None:
            raise Exception("Missing valid headers")

        return etree.Element(
                                ns(EET_NS, 'Hlavicka'),
                                attrib={
                                            'uuid_zpravy': self.getUUID(),
                                            'dat_odesl': self.getDate(),
                                            'prvni_zaslani': self.getFirstSend(),
                                        },
                                nsmap=NSMAP
                            )
