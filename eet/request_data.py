from lxml import etree
from eet.utils import *

class EETRequestData(object):
    def __init__(self, config, **kwargs):
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
        self.normal_vat_sum = kwargs.get('normal_vat_sum')
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

    def getNormalVatSum(self):
        return u'%.2f' % self.normal_vat_sum

    def getSimple(self):
        if self.simple:
            return u'1'
        return u'0'

    def validate():
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

        if self.normal_vat_sum:
            attrib[u'dan1'] = self.getNormalVatSum()

        if self.simple:
            attrib[u'rezim'] = self.getSimple()

        return etree.Element(ns(EET_NS, 'Data'), attrib=attrib, nsmap=NSMAP)


