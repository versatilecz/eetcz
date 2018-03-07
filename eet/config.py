# -*- coding: utf-8 -*-

SOAP_NS = 'http://schemas.xmlsoap.org/soap/envelope/'
EXC_NS = 'http://www.w3.org/2001/10/xml-exc-c14n#'
DS_NS = 'http://www.w3.org/2000/09/xmldsig#'
ENC_NS = 'http://www.w3.org/2001/04/xmlenc#'
WSS_BASE = 'http://docs.oasis-open.org/wss/2004/01/'
WSSE_NS = WSS_BASE + 'oasis-200401-wss-wssecurity-secext-1.0.xsd'
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
        'eet': EET_NS,
}

DEFAULT_KEY = b'''-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCZzVD1vKwJS4ti
gMLtdltb6i49NpliIn6vyadP7VI3/QfEaZAwA9xjqg3Vbh0n8Xo/dlohKLg8u1/L
l8yA3WbuKVwN7dyp7cTPKwJbtlOkqrRd5E0fgCQncH5DOd1N8+P6qMiqnUPJRrjM
SSrO1+biI3GP1A0lzCvTk5l0YZ3Y2HF9aCC6+RdjjX9WdJFspf0vcCNHJdIENRfd
Zs6oJ5R/NLtopzJpgaeNp3UeExktZ743q+Q+925C4NO03Xqp1IOtPVsI1CTfejim
TLCl8wTM7dPTW4UHAAVpwFm0U0lYbAHQzvL35lsdgvoF1JZCL7TvvX24/NRktcXT
aAJKQEVHAgMBAAECggEAIKt1NA20uXC7ldvmDAzlERwoYEZVxHuxT2PVT2wI1+2+
laEayKg5S05XC+wM82we3JYmRP7iS7w9eACxpvngoFxWunq5MbtY3+yx3otXLxY3
o+4X18YfZ+VEXMFQ2fshhSAPJ/ap7HpCTNqJ5lAEMir3N2cCt/GrqZCjuw31OpdC
7qRr1SecK5zVv3H023Kmtnh5hwlhOd09/dZaXvp6+DMAZlobSX4xSuQ7WJvAvH9k
bTvyqjh0zldnhNEMFaxKcfh1FENQZFk6in9cO94PTb64Hr54t15lSvhC63DFroND
rVM1LwQzSSOqXQnjjg5TJC4Ja3EOgs1eAfRjOcIwoQKBgQDRt68sUYew8MG7cn+V
ugi2JvQzxgFZQI48My3w1aKwsDi68eT/l0kU6vxGBaMLfitT9rq5opfWvzGsaRWV
RUHlaA3UGYQaBhrS2uluEDKvJMJxEoPlOKSHnK4D9LJI4EsPueyhbddvWUalGWVX
07ziHR7n68yPA0MHYx51oikf8QKBgQC7vplodRNLk8leMQOru5jz9zHOvk6+jEEJ
xBJIEhgiq3AjhrFlrOsVXV4SjtPPYFe+Q4J7ZIprpAu6jhCEmIQgCj/IUIfXqLPh
hiJ/TYfIpmKhV7Lfo5Ag2piZPlHZ626HA9Ws8wS1kQWYax10dfQifr3kNJotSwPp
+p/GP/FwtwKBgQDQA98oGXJ7CkNPV2G/tLghXQAKPpNl4Qd0JNujr3Pgx9pta7PV
5UxjCDXUipDPvITjkq5hpSnwotJ1jgIPfpO/JXfZ8rk6SuXeUa8KMdzkJpULLO9Q
tN9VeA6O8+7HJFqvrZ5N/LKcyrOs3UTNWcNXkMTwC85p6DVbJXC4A3HBMQKBgCio
qW5+1FPsyJJWiRX7Ba/oG+hLPKB1nWwxA0iKaqGvgRSgifCcFzlERCg+uE5T7gyt
cCeq6XNQTp3zQE6G/S43KgMGtbSVu4ce1n+9WaexqPCKHpniQUdsL9oYLf/ExeYF
hZPz+VQc+Ro+MF3VYa7KxfMTFUSz10An38w+ctpXAoGBAJQFNPOLMr5WEOzptRWb
Kab1DmGdLIv1mThdNcrKNl6pIh2diM0imLHfu4lUSxGK1yOp7CFbuQpnwd0ZqTo3
GBLk9NuMbuWdq5/i2mnpz8yOidCdTfNivPvMBbX3hth4EEs/d7B+wKC+NQXslh4x
aBppNGFVNdI4PqmEG0Kk5Xsd
-----END PRIVATE KEY-----'''

DEFAULT_CERT = b'''-----BEGIN CERTIFICATE-----
MIIEmDCCA4CgAwIBAgIEdHOXJzANBgkqhkiG9w0BAQsFADB3MRIwEAYKCZImiZPy
LGQBGRYCQ1oxQzBBBgNVBAoMOsSMZXNrw6EgUmVwdWJsaWthIOKAkyBHZW5lcsOh
bG7DrSBmaW5hbsSNbsOtIMWZZWRpdGVsc3R2w60xHDAaBgNVBAMTE0VFVCBDQSAx
IFBsYXlncm91bmQwHhcNMTYwOTMwMDkwMzU5WhcNMTkwOTMwMDkwMzU5WjBDMRIw
EAYKCZImiZPyLGQBGRYCQ1oxEzARBgNVBAMTCkNaMDAwMDAwMTkxGDAWBgNVBA0T
D3ByYXZuaWNrYSBvc29iYTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEB
AJnNUPW8rAlLi2KAwu12W1vqLj02mWIifq/Jp0/tUjf9B8RpkDAD3GOqDdVuHSfx
ej92WiEouDy7X8uXzIDdZu4pXA3t3KntxM8rAlu2U6SqtF3kTR+AJCdwfkM53U3z
4/qoyKqdQ8lGuMxJKs7X5uIjcY/UDSXMK9OTmXRhndjYcX1oILr5F2ONf1Z0kWyl
/S9wI0cl0gQ1F91mzqgnlH80u2inMmmBp42ndR4TGS1nvjer5D73bkLg07TdeqnU
g609WwjUJN96OKZMsKXzBMzt09NbhQcABWnAWbRTSVhsAdDO8vfmWx2C+gXUlkIv
tO+9fbj81GS1xdNoAkpARUcCAwEAAaOCAV4wggFaMAkGA1UdEwQCMAAwHQYDVR0O
BBYEFL/0b0Iw6FY33UT8iJEy1V7nZVR6MB8GA1UdIwQYMBaAFHwwdqzM1ofR7Mkf
4nAILONf3gwHMA4GA1UdDwEB/wQEAwIGwDBjBgNVHSAEXDBaMFgGCmCGSAFlAwIB
MAEwSjBIBggrBgEFBQcCAjA8DDpUZW50byBjZXJ0aWZpa8OhdCBieWwgdnlkw6Fu
IHBvdXplIHBybyB0ZXN0b3ZhY8OtIMO6xI1lbHkuMIGXBgNVHR8EgY8wgYwwgYmg
gYaggYOGKWh0dHA6Ly9jcmwuY2ExLXBnLmVldC5jei9lZXRjYTFwZy9hbGwuY3Js
hipodHRwOi8vY3JsMi5jYTEtcGcuZWV0LmN6L2VldGNhMXBnL2FsbC5jcmyGKmh0
dHA6Ly9jcmwzLmNhMS1wZy5lZXQuY3ovZWV0Y2ExcGcvYWxsLmNybDANBgkqhkiG
9w0BAQsFAAOCAQEAvXdWsU+Ibd1VysKnjoy6RCYVcI9+oRUSSTvQQDJLFjwn5Sm6
Hebhci8ERGwAzd2R6uqPdzl1KCjmHOitypZ66e+/e9wj3BaDqgBKRZYvxZykaVUd
tQgG0819JZmiXTbGgOCKiUPIXO80cnP7U1ZPkVNV7WZwh0I2k/fg1VLTI5HA/x4B
eD77wiEOExa7eqePJET0jpTVK3LxSW59LLIJROh4/kfKQbTvDL5Ypw8WagAMVCPv
WnGJIcUru+ApLU4pZD9bdHSa1Ib4LpFhtWrkHYM/XqKbj2bNKKjTo5T3sU0Bf2QD
3QzkmcjlNVG0V+qAgimwTdPueU/mtExw+7z1/A==
-----END CERTIFICATE-----'''

DEFAULT_ROOT_CERT = b'''-----BEGIN CERTIFICATE-----
MIIE2TCCA8GgAwIBAgIFAIPD9YUwDQYJKoZIhvcNAQELBQAwdzESMBAGCgmSJomT
8ixkARkWAkNaMUMwQQYDVQQKDDrEjGVza8OhIFJlcHVibGlrYSDigJMgR2VuZXLD
oWxuw60gZmluYW7EjW7DrSDFmWVkaXRlbHN0dsOtMRwwGgYDVQQDExNFRVQgQ0Eg
MSBQbGF5Z3JvdW5kMB4XDTE2MDkyOTE5NTQ0MFoXDTIyMDkyOTE5NTQ0MFowdzES
MBAGCgmSJomT8ixkARkWAkNaMUMwQQYDVQQKDDrEjGVza8OhIFJlcHVibGlrYSDi
gJMgR2VuZXLDoWxuw60gZmluYW7EjW7DrSDFmWVkaXRlbHN0dsOtMRwwGgYDVQQD
ExNFRVQgQ0EgMSBQbGF5Z3JvdW5kMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIB
CgKCAQEA1IyU2zS/gm+66J9H5mL5W5071y88EF0f4X440TXuCjNvwdjvQhaQy2mw
m5+hG3RnuavQnJQOoIi532XLJNTawzP23MUtChjoa0B4ngAbnSRXXsjSscJde+eP
U8WKkxmxfd5BeuW4sHFh4CukI1UmwDs3cLy4BQ3ec0tYmn+HzQ+xzOgTO8EmDdr5
oTsoxV0TSoiIQVaeS+p5Qohx9ZUsB6H2oyg68GCSk/otZUo8wz71LW2bWNTxvDvx
R6YPpnKtQ+j9FNU9JeX76a3vEZ578DbcGrS/0iCZ4sTzrU47zBmdhn4mIJ3yAB6U
0y4dSKVd6TMqldVy5h6ep6hTQoUFdwIDAQABo4IBajCCAWYwEgYDVR0TAQH/BAgw
BgEB/wIBADAgBgNVHQ4BAf8EFgQUfDB2rMzWh9HsyR/icAgs41/eDAcwDgYDVR0P
AQH/BAQDAgEGMB8GA1UdIwQYMBaAFHwwdqzM1ofR7Mkf4nAILONf3gwHMGMGA1Ud
IARcMFowWAYKYIZIAWUDAgEwATBKMEgGCCsGAQUFBwICMDwMOlRlbnRvIGNlcnRp
Zmlrw6F0IGJ5bCB2eWTDoW4gcG91emUgcHJvIHRlc3RvdmFjw60gw7rEjWVseS4w
gZcGA1UdHwSBjzCBjDCBiaCBhqCBg4YpaHR0cDovL2NybC5jYTEtcGcuZWV0LmN6
L2VldGNhMXBnL2FsbC5jcmyGKmh0dHA6Ly9jcmwyLmNhMS1wZy5lZXQuY3ovZWV0
Y2ExcGcvYWxsLmNybIYqaHR0cDovL2NybDMuY2ExLXBnLmVldC5jei9lZXRjYTFw
Zy9hbGwuY3JsMA0GCSqGSIb3DQEBCwUAA4IBAQBHieHV+n7agbBRYYzHbWruqi1i
F7dX1g8cotPPg590FfQEAhK+Nwef8/sPNeo8gT99idzyRSq60c2f1nVlca+5W7YV
jUV2KrVqbE+1Ku4GT9K/ZFW6yyIOSeHBkCCjjoNJYLVBFgJMeepSoHFYsNk0pzzZ
g7Amemh0kxxd4YcxcxZHe0o2tNzdcUJ6pQxgwOYI67uepsBSor30qXTneAouMqLY
QHHc8v6JsMXFzrvg2tDAtQzNC3Ibsquw+Sur6ItgYMmkmOk9WfK33q7lUfXx34X5
F9OTF6UdKfXkvt+NmW7ayYwd+F4+3pfFr3wvBNdrG6tm/SUZBQ41Tt4OTKWg
-----END CERTIFICATE-----'''

DEFAULT_URL = 'https://pg.eet.cz/eet/services/EETServiceSOAP/v3/'


class EETConfig(object):

    @staticmethod
    def test():
        return EETConfig(
            'CZ00000019', 237, '/5546/RO24', debug=False,
            key=DEFAULT_KEY, cert=DEFAULT_CERT, root_cert=DEFAULT_ROOT_CERT
        )

    def __init__(
        self, dic, id_shop, id_register, key=None, key_file=None, key_password=None,
        cert=None, cert_file=None, root_cert=None, root_cert_file=None,
        url=None, simple=False, debug=False, dic_commission=None
    ):
        self.debug = debug
        self.dic = dic
        self.dic_commission = dic_commission
        self.id_shop = id_shop
        self.id_register = id_register
        self.simple = simple
        self.password = None
        self.key = self._loadKey(key, key_file)
        self.cert = self._loadCert(cert, cert_file)
        self.root_crt = self._loadRootCert(cert, cert_file)
        self.url = url or DEFAULT_URL

    def _loadKey(self, key, key_file):
        if key is not None:
            return key

        elif key_file is not None and isinstance(key_file, str):
            key_file = open(key_file, 'r')

        key = key_file.read()
        key_file.close()
        return key

    def _loadCert(self, cert, cert_file):
        if cert is not None:
            return cert

        elif cert_file is not None and isinstance(cert_file, str):
            cert_file = open(cert_file, 'r')

        cert = cert_file.read()
        cert_file.close()
        return cert

    def _loadRootCert(self, cert, cert_file):
        if cert is not None:
            return cert

        elif cert_file is not None and isinstance(cert_file, str):
            cert_file = open(cert_file, 'r')

        cert = cert_file.read()
        cert_file.close()
        return cert


def ns(namespace, tagname):
    return '{%s}%s' % (namespace, tagname)
