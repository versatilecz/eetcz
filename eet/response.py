# -*- coding: utf-8 -*-
from __future__ import print_function
import hashlib
import textwrap
import logging
from base64 import b64encode, b64decode
from lxml import etree
from dateutil import parser

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.x509 import load_pem_x509_certificate

from eet.config import *

logger = logging.getLogger(__name__)


class EETResponse(object):
    '''
    Structure, that hold all data from response
    '''

    def __init__(self, response):
        '''
        constructor that catch data from requests.post in request to soap service
        '''

        # incialize variables
        self.response = response
        self.raw = response.text.encode('utf8')
        self.root = None
        self.success = False
        self.verified = None
        self.warnings = []
        self.error = None
        self.error_code = None
        self.bkp = None
        self.uuid = None
        self.date = None
        self.fik = None
        self.test = None

        try:
            self.root = etree.fromstring(self.raw)
            self.body = self.root.find(ns(SOAP_NS, 'Body'))
            assert self.body is not None
            response = self.body.find(ns(EET_NS, 'Odpoved'))
            assert response is not None
        except Exception as e:
            self.error = str(e)
            self.error_code = 100
            return

        # find basic elements
        header = response.find(ns(EET_NS, 'Hlavicka'))
        confirmation = response.find(ns(EET_NS, 'Potvrzeni'))
        warnings = response.findall(ns(EET_NS, 'Varovani'))
        error = response.find(ns(EET_NS, 'Chyba'))

        # check basic elements for status

        # check header
        if header is not None:
            self.uuid = header.get('uuid_zpravy')
            self.bkp = header.get('bkp')

        # check positive response
        if confirmation is not None:
            self.success = True
            self.date = parser.parse(header.get('dat_prij'))
            self.fik = confirmation.get('fik')
            self.test = confirmation.get('test') == 'true'
            self.verified = self._verify()

        # check negative response
        if error is not None:
            self.success = False
            self.date = parser.parse(header.get('dat_odmit'))
            self.error = error.text
            self.error_code = error.get('kod')
            self.test = error.get('test') == 'true'

            if self.error_code == '0':
                self.success = True

        # if response contains varnings
        for warning in warnings:
            self.warnings.append((warning.get('kod_varov'), warning.text,))

    def _verify(self):
        '''
        Check, if message is wellsigned
        '''
        try:
            # canonize soap body a make sha256 digest
            body_c14n = etree.tostring(self.body, method='c14n', exclusive=True, with_comments=False)
            sha256 = hashlib.sha256(body_c14n)
            digest = b64encode(sha256.digest())

            # load cert options
            cert = self.root.find('.//wsse:BinarySecurityToken', namespaces=NSMAP)
            sig_info = self.root.find('.//ds:SignedInfo', namespaces=NSMAP)
            sig_value = self.root.find('.//ds:SignatureValue', namespaces=NSMAP)

            # check, if there is all nesesery data
            assert cert is not None
            assert sig_info is not None
            assert sig_value is not None

            # canonize signature info
            sig_info_c14n = etree.tostring(sig_info, method='c14n', exclusive=True, with_comments=False)

            # transform and load cert
            cert = '\n'.join(['-----BEGIN CERTIFICATE-----'] + textwrap.wrap(cert.text, 64) + ['-----END CERTIFICATE-----\n'])
            cert = load_pem_x509_certificate(cert.encode('utf-8'), default_backend())
            key = cert.public_key()

            # verify digest
            verifier = key.verifier(b64decode(sig_value.text), padding.PKCS1v15(), hashes.SHA256())
            verifier.update(sig_info_c14n)
            # if verify fail, raise exception
            verifier.verify()

            return True

        except Exception as e:
            logger.exception(e)

        # probably error, return false
        return False
