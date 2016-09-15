import base64
import hashlib

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding

from lxml import etree

from eet.utils import *

class EETRequestControl(object):
    def __init__(self, config, data):
        self.config = config
        self.data = data
        self.sign = self.signByKey()
        self.pkp = self.encodeSign()
        self.bkp = self.hashSign()


    def signByKey(self):
        private_key = serialization.load_pem_private_key(self.config.key, password=self.config.password, backend=default_backend())
        signer = private_key.signer(padding.PKCS1v15(), hashes.SHA256())

        signer.update(self.data.encode('utf8'))
        return signer.finalize()

    def encodeSign(self):
        return base64.encodestring(self.sign).replace('\n', '')

    def hashSign(self):
        sha1 = hashlib.sha1(self.sign)
        digest = sha1.hexdigest()
        return ('%s-%s-%s-%s-%s' % (digest[0:8], digest[8:16], digest[16:24], digest[24:32], digest[32:])).upper()

    def element(self):
        codes = etree.Element(ns(EET_NS, 'KontrolniKody'))
        pkp = etree.SubElement(codes, ns(EET_NS, 'pkp'), attrib={'cipher': 'RSA2048', 'digest': 'SHA256', 'encoding': 'base64'})
        pkp.text = self.pkp

        bkp = etree.SubElement(codes, ns(EET_NS, 'bkp'), attrib={'digest': 'SHA1', 'encoding': 'base16'})
        bkp.text = self.bkp
        return codes
