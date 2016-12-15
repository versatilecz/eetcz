# -*- coding: utf-8 -*-
#
# MIT License
#
# Copyright (c) 2016 Martin
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import pytz
import datetime
import hashlib
import requests

from lxml import etree
from uuid import uuid4
from base64 import b64encode, b64decode
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding

from eet.response import EETResponse
from eet.config import *

__all__ = ['EETRequest']

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

def get_unique_id():
    return 'id-{0}'.format(uuid4())

class EETRequestHeader(object):
    '''
    Helper class that provide Header request field
    '''

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
                                            'overeni': self.getDebug(),
                                        },
                                nsmap=NSMAP
                            )



class EETRequestData(object):
    '''
    '''
    def __init__(self, config, **kwargs):
        '''
        '''
        self.config = config
        self.dic = kwargs.get('dic', config.dic)
        self.dic_commission = kwargs.get('dic_commission', config.dic_commission)
        self.id_shop = kwargs.get('id_shop', config.id_shop)
        self.id_register = kwargs.get('id_register', config.id_register)
        self.number = kwargs.get('number')
        self.date = kwargs.get('date')
        self.price_sum = kwargs.get('price_sum')
        self.price_sum_non_vat = kwargs.get('price_sum_non_vat')
        self.price_sum_normal_vat = kwargs.get('price_sum_normal_vat')
        self.price_sum_first_vat = kwargs.get('price_sum_first_vat')
        self.normal_vat_sum = kwargs.get('normal_vat_sum')
        self.first_vat_sum = kwargs.get('first_vat_sum')
        #another field with specific vat
        self.simple = kwargs.get('simple', config.simple)

    def getSignData(self):
        return u'%s|%s|%s|%s|%s|%s' % (self.getDic(), self.getIdShop(), self.getIdRegister(), self.getNumber(), self.getDate(), self.getPriceSum())

    def getDic(self):
        return unicode(self.dic)

    def getDicCommision(self):
        return unicode(self.dic_commission)

    def getIdShop(self):
        return unicode(self.id_shop)

    def getIdRegister(self):
        return unicode(self.id_register)

    def getNumber(self):
        return unicode(self.number)

    def getDate(self):
        return formatDate(self.date)

    def getPriceSum(self):
        return u'%.2f' % self.price_sum

    def getPriceSumNonVat(self):
        return u'%.2f' % self.price_sum_non_vat

    def getPriceSumNormalVat(self):
        return u'%.2f' % self.price_sum_normal_vat

    def getPriceSumFirstVat(self):
        return u'%.2f' % self.price_sum_first_vat

    def getNormalVatSum(self):
        return u'%.2f' % self.normal_vat_sum

    def getFirstVatSum(self):
        return u'%.2f' % self.first_vat_sum

    def getSimple(self):
        if self.simple:
            return u'1'
        return u'0'

    def validate(self):
        return True

    def element(self):
        attrib = {
                    u'dic_popl': self.getDic(),
                    u'id_provoz': self.getIdShop(),
                    u'id_pokl': self.getIdRegister(),
                    u'porad_cis': self.getNumber(),
                    u'dat_trzby': self.getDate(),
                    u'celk_trzba': self.getPriceSum(),
                }
        if self.dic_commission:
            attrib[u'dic_poverujiciho'] = self.getDicCommision()

        if self.price_sum_non_vat:
            attrib[u'zakl_nepodl_dph'] = self.getPriceSumNonVat()

        if self.price_sum_normal_vat:
            attrib[u'zakl_dan1'] = self.getPriceSumNormalVat()

        if self.price_sum_first_vat:
            attrib[u'zakl_dan2'] = self.getPriceSumFirstVat()

        if self.normal_vat_sum:
            attrib[u'dan1'] = self.getNormalVatSum()

        if self.first_vat_sum:
            attrib[u'dan2'] = self.getFirstVatSum()()

        attrib[u'rezim'] = self.getSimple()

        return etree.Element(ns(EET_NS, 'Data'), attrib=attrib, nsmap=NSMAP)

class EETRequestControl(object):
    '''
    '''
    def __init__(self, config, data):
        self.config = config
        self.data = data
        self.sign = self._signByKey()
        self.pkp = self._encodeSign()
        self.bkp = self._hashSign()


    def _signByKey(self):
        private_key = serialization.load_pem_private_key(self.config.key, password=self.config.password, backend=default_backend())
        signer = private_key.signer(padding.PKCS1v15(), hashes.SHA256())

        signer.update(self.data.encode('utf8'))
        return signer.finalize()

    def _encodeSign(self):
        return b64encode(self.sign)

    def _hashSign(self):
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

class EETRequest(object):
    '''
    Basic object, that get request
    '''

    @staticmethod
    def test():
        '''
        Function,
        '''
        return EETRequest(EETConfig.test(), date=now(), price_sum=34113.00, price_sum_normal_vat=100, normal_vat_sum=21, number='0/6460/ZQ42')


    def __init__(self, config, **kwargs):
        '''
        Construct. there is one mandatory argument config. all kwargs is add to data
        '''
        self.config = config
        self.header = EETRequestHeader(config)
        self.data = EETRequestData(config, **kwargs)
        self.code = EETRequestControl(config, self.data.getSignData())


    def element(self):
        envelope = etree.Element(ns(SOAP_NS, 'Envelope'), nsmap=NSMAP)

        header = etree.SubElement(envelope, ns(SOAP_NS, 'Header'), nsmap=NSMAP)
        body_id = get_unique_id()
        body = etree.SubElement(envelope, ns(SOAP_NS, 'Body'), attrib={ns(WSU_NS, 'Id'): body_id}, nsmap=NSMAP)

        trzba = etree.SubElement(body, ns(EET_NS, 'Trzba'), nsmap=NSMAP)
        trzba.append(self.header.element())
        trzba.append(self.data.element())
        trzba.append(self.code.element())

        security = etree.SubElement(header, ns(WSSE_NS, 'Security'), attrib={ns(SOAP_NS, 'mustUnderstand'): '1'}, nsmap=NSMAP)

        token_id = get_unique_id()
        token = etree.SubElement(security, ns(WSSE_NS, 'BinarySecurityToken'), attrib={
            'EncodingType': BASE64B,
            'ValueType': X509TOKEN,
            ns(WSU_NS, 'Id'): token_id
            })
        token.text = self.config.cert[28:-26].replace('\n', '')

        signature_id = get_unique_id()
        signature = etree.SubElement(security, ns(DS_NS, 'Signature'), attrib={'Id': signature_id})
        signed_info = etree.SubElement(signature, ns(DS_NS, 'SignedInfo'))
        canonicalization_method = etree.SubElement(signed_info, ns(DS_NS, 'CanonicalizationMethod'), attrib={'Algorithm': EXC_NS})
        cm_in = etree.SubElement(canonicalization_method, ns(EXC_NS,'InclusiveNamespaces'))
        signature_method = etree.SubElement(signed_info, ns(DS_NS, 'SignatureMethod'), attrib={'Algorithm': RSA_SHA256})
        ds_reference = etree.SubElement(signed_info, ns(DS_NS, 'Reference'), attrib={'URI': '#%s' % body_id})
        ds_transforms = etree.SubElement(ds_reference, ns(DS_NS, 'Transforms'))
        ds_transform = etree.SubElement(ds_transforms, ns(DS_NS, 'Transform'), attrib={'Algorithm': EXC_NS})
        cm_in = etree.SubElement(ds_transform, ns(EXC_NS,'InclusiveNamespaces'), attrib={'PrefixList': ''})
        digest_method = etree.SubElement(ds_reference, ns(DS_NS, 'DigestMethod'), attrib={'Algorithm': SHA256})
        digest_value = etree.SubElement(ds_reference, ns(DS_NS, 'DigestValue'))
        signature_value = etree.SubElement(signature, ns(DS_NS, 'SignatureValue'))
        key_info_id = get_unique_id()
        key_info = etree.SubElement(signature, ns(DS_NS, 'KeyInfo'), attrib={'Id': key_info_id})
        security_token_reference_id = get_unique_id()
        security_token_reference = etree.SubElement(key_info, ns(WSSE_NS, 'SecurityTokenReference'), attrib={ns(WSU_NS, 'Id'): security_token_reference_id})
        wsse_reference = etree.SubElement(security_token_reference, ns(WSSE_NS, 'Reference'), attrib={'URI': '#%s' % token_id, 'ValueType': X509TOKEN})

        # generate digest
        payload = etree.tostring(body, method='c14n', exclusive=True, with_comments=False)
        sha256 = hashlib.sha256(payload)
        digest = b64encode(sha256.digest())
        digest_value.text = digest

        # sign structure
        payload = etree.tostring(signed_info, method='c14n', exclusive=True, with_comments=False)
        private_key = serialization.load_pem_private_key(self.config.key, password=self.config.password, backend=default_backend())
        signer = private_key.signer(padding.PKCS1v15(), hashes.SHA256())
        signer.update(payload)
        signature_value.text = b64encode(signer.finalize())

        return envelope

    def serialize(self):
        '''
        return serialized request
        '''
        element = self.element()
        return etree.tostring(element, encoding="UTF-8", xml_declaration=True)

    def send(self):
        '''
        send request
        '''
        response = requests.post(self.config.url, data=self.serialize())
        response.raise_for_status()
        return EETResponse(response)
