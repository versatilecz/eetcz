import datetime
import pytz
from uuid import uuid4

__all__ = ['timezone', 'now', 'formatDate', 'SOAP_NS', 'EXC_NS', 'DS_NS', 'ENC_NS', 'WSS_BASE', 'WSSE_NS', 'WSU_NS', 'BASE64B', 'X509TOKEN', 'RSA_SHA256', 'SHA256', 'EET_NS', 'NSMAP', 'ns', 'get_unique_id', 'ensure_id', 'ID_ATTR']

SOAP_NS = 'http://schemas.xmlsoap.org/soap/envelope/'
EXC_NS = 'http://www.w3.org/2001/10/xml-exc-c14n#'
# xmldsig
DS_NS = 'http://www.w3.org/2000/09/xmldsig#'
# xmlenc
ENC_NS = 'http://www.w3.org/2001/04/xmlenc#'

WSS_BASE = 'http://docs.oasis-open.org/wss/2004/01/'
# WS-Security
WSSE_NS = WSS_BASE + 'oasis-200401-wss-wssecurity-secext-1.0.xsd'
# WS-Utility
WSU_NS = WSS_BASE + 'oasis-200401-wss-wssecurity-utility-1.0.xsd'

BASE64B = WSS_BASE + 'oasis-200401-wss-soap-message-security-1.0#Base64Binary'
X509TOKEN = WSS_BASE + 'oasis-200401-wss-x509-token-profile-1.0#X509v3'
RSA_SHA256 = 'http://www.w3.org/2001/04/xmldsig-more#rsa-sha256'
SHA256 = 'http://www.w3.org/2001/04/xmlenc#sha256'
EET_NS = 'http://fs.mfcr.cz/eet/schema/v3'

NSMAP = {
        'soap': SOAP_NS,
        'ec': EXC_NS,
        'ds': DS_NS,
        'wsse': WSSE_NS,
        'wsu': WSU_NS,
        None: EET_NS,
    }

timezone = timezone = pytz.timezone('Europe/Prague')

def now():
    return datetime.datetime.now(tz=timezone)

def formatDate(date):
    if date is None:
        date = now()

    if date.tzinfo is None:
        date = datetime.datetime(date.year, date.month, date.day, date.hour, date.minute, date.second, 0)

    if False:
        return date.strftime('%Y-%m-%dT%H:%M:%S+01:00')
    else:
        return date.strftime('%Y-%m-%dT%H:%M:%S+02:00')

def ns(namespace, tagname):
    return '{%s}%s' % (namespace, tagname)

def get_unique_id():
    return 'id-{0}'.format(uuid4())

def ensure_id(node):
    """Ensure given node has a wsu:Id attribute; add unique one if not.
    Return found/created attribute value.
    """
    id_val = node.get(ID_ATTR)
    if not id_val:
        id_val = get_unique_id()
        node.set(ID_ATTR, id_val)
    return id_val

ID_ATTR = ns(WSU_NS, 'Id')

