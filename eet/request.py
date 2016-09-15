# -*- coding: utf-8 -*-
import re
import datetime
from base64 import b64encode, b64decode
import hashlib
import requests

from lxml import etree
from uuid import uuid4

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding

from eet.request_header import EETRequestHeader
from eet.request_data import EETRequestData
from eet.request_control import EETRequestControl
from eet.response import EETResponse
from eet.utils import *
from eet.config import Config


class EETRequest(object):

    @staticmethod
    def test():
        config = Config()
        return EETRequest(config, date=now(), price_sum=34113.00, price_sum_normal_vat=100, normal_vat_sum=21, number='0/6460/ZQ42')


    def __init__(self, config, **kwargs):
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
        element = self.element()
        return etree.tostring(element, encoding="UTF-8", xml_declaration=True)

    def send(self):
        return EETResponse(requests.post(self.config.getURL(), data=self.serialize()))
