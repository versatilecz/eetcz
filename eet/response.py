import hashlib
import textwrap
from base64 import b64encode, b64decode
from lxml import etree
from eet.utils import *
from dateutil import parser

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.x509 import load_pem_x509_certificate

class EETResponse(object):

    def __init__(self, response=None):
        self.raw = None
        self.root = None
        self.success = None
        self.verified = None
        self.warnings = []
        self.error = None
        self.error_code = None
        self.bkp = None
        self.uuid = None
        self.date = None
        self.fik = None
        self.test = None

        if response is None:
            f = open('out', 'r')
            self.raw = f.read()
            f.close()
        else:
            self.raw = response.text.encode('utf8')
            f = open('out', 'w')
            f.write(self.raw)
            f.close()

        self.root = etree.fromstring(self.raw)


        self.body = self.root.find(ns(SOAP_NS, 'Body'))
        assert self.body is not None

        response = self.body.find(ns(EET_NS, 'Odpoved'))
        assert response is not None

        #print etree.tostring(response)

        header = response.find(ns(EET_NS, 'Hlavicka'))
        confirmation = response.find(ns(EET_NS, 'Potvrzeni'))
        warnings = response.findall(ns(EET_NS, 'Varovani'))
        error = response.find(ns(EET_NS, 'Chyba'))

        if header is not None:
            self.uuid = header.get('uuid_zpravy')
            self.bkp = header.get('bkp')

        if confirmation is not None:
            self.success = True
            self.date = parser.parse(header.get('dat_prij'))
            self.test = confirmation.get('test')
            self.fik = confirmation.get('fik')
            self.test = confirmation.get('test') == 'true'
            self.verified = self.verify()

        if error is not None:
            self.success = False
            self.date = parser.parse(header.get('dat_odmit'))
            self.error = error.text
            self.error_code = error.get('kod')
            self.test = error.get('test') == 'true'

        for warning in warnings:
            self.warnings.append((warning.get('kod_varov'), warning.text,))

    def verify(self):
        try:
            body_c14n = etree.tostring(self.body, method='c14n', exclusive=True, with_comments=False)
            sha256 = hashlib.sha256(body_c14n)
            digest = b64encode(sha256.digest())

            cert = self.root.find('.//wsse:BinarySecurityToken', namespaces=NSMAP)
            sig_info = self.root.find('.//ds:SignedInfo', namespaces=NSMAP)
            sig_value = self.root.find('.//ds:SignatureValue', namespaces=NSMAP)

            assert cert is not None
            assert sig_info is not None
            assert sig_value is not None

            sig_info_c14n = etree.tostring(sig_info, method='c14n', exclusive=True, with_comments=False)

            cert = '\n'.join(['-----BEGIN CERTIFICATE-----'] + textwrap.wrap(cert.text, 64) + ['-----END CERTIFICATE-----\n'])
            cert = load_pem_x509_certificate(cert, default_backend())
            key = cert.public_key()
            verifier = key.verifier(b64decode(sig_value.text), padding.PKCS1v15(), hashes.SHA256())
            verifier.update(sig_info_c14n)
            verifier.verify()
            return True
        except Exception as e:
            logger.exception(e)
            
        return False
