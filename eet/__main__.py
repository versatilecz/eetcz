#!/usr/bin/env python

from __future__ import print_function
import argparse
import json
import sys
from dateutil.parser import parse
from eet import EETRequest, EETConfig, config


def eet_file():
    parser = argparse.ArgumentParser(description='EET request through file')
    dic = 'CZ00000019'
    id_shop = 237
    id_register = '/5546/RO24'

    config_kwargs = {
        'url': config.DEFAULT_URL,
        'key': config.DEFAULT_KEY,
        'cert': config.DEFAULT_CERT,
        'dic_commission': None,
        'simple': False,
        'debug': False,
    }

    data = {
        'price_sum': 34113.00,
        'price_sum_normal_vat': 100,
        'normal_vat_sum': 21,
        'number': '0/6460/ZQ42',
    }

    parser.add_argument(
        '-c', '--config',
        help='Config file',
        type=argparse.FileType('r'),
        dest='config',
        default=None
    )

    parser.add_argument(
        '-d', '--dic',
        help='DIC',
        type=str,
        dest='dic',
        default=None
    )

    parser.add_argument(
        '--dic2',
        help='DIC commision',
        type=str,
        dest='dic2',
        default=None
    )

    parser.add_argument(
        '-s', '--shop',
        help='Shop id',
        type=str,
        dest='shop',
        default=None
    )

    parser.add_argument(
        '-r', '--register',
        help='Register id',
        type=str,
        dest='register',
        default=None
    )

    parser.add_argument(
        '-u', '--url',
        help='File with public key',
        type=str,
        dest='url',
        default=None
    )

    parser.add_argument(
        '-e', '--simple',
        help='If is in simple mode',
        type=bool,
        dest='simple',
        default=None
    )

    parser.add_argument(
        '--date',
        help='Datetime of transaction',
        type=str,
        dest='date',
        default=None
    )

    parser.add_argument(
        '-g', '--debug',
        help='Debug mode',
        type=str,
        dest='debug',
        default=None
    )

    parser.add_argument(
        '--key_file',
        help='File with private key',
        type=argparse.FileType('r'),
        dest='key_file',
        default=None
    )

    parser.add_argument(
        '--cert_file',
        help='File with public key',
        type=argparse.FileType('r'),
        dest='cert_file',
        default=None
    )

    parser.add_argument(
        '-o', '--output',
        help='File for output',
        dest='output',
        nargs='?',
        type=argparse.FileType('w'),
        default=sys.stdout
    )

    parser.add_argument(
        '-v', '--verbose',
        help='Verbose',
        default=False,
        dest='verbose',
        action='store_true'
    )

    parser.add_argument(
        '-t', '--test',
        help='Test',
        default=False,
        dest='test',
        action='store_true'
    )

    parser.add_argument(
        'data_file',
        help='File with data',
        nargs='?',
        type=argparse.FileType('r'),
        default=sys.stdin
    )

    args = parser.parse_args()
    if args.config:
        config_kwargs = json.load(args.config)
        if 'dic' in config_kwargs:
            dic = config_kwargs['dic']

        if 'shop' in config_kwargs:
            id_shop = config_kwargs['shop']

        if 'register' in config_kwargs:
            id_register = config_kwargs['register']

        if 'key' in config_kwargs:
            key = config_kwargs['key']

        if 'cert' in config_kwargs:
            cert = config_kwargs['cert']

    if args.dic:
        dic = args.dic

    if args.dic2:
        config_kwargs['dic_commission'] = args.dic2

    if args.shop:
        id_shop = args.shop

    if args.register:
        id_register = args.register

    if args.url:
        config_kwargs['url'] = args.url

    if args.key_file:
        config_kwargs['key'] = args.key_file.read().encode('utf8')

    if args.cert_file:
        config_kwargs['cert'] = args.cert_file.read().encode('utf8')

    if args.simple:
        config_kwargs['simple'] = args.simple

    if args.debug:
        config_kwargs['debug'] = args.debug

    if not args.test:
        data = json.load(args.data_file)

    if args.verbose:
        print("Config: ", {
            'dic': dic,
            'id_shop': id_shop,
            'id_register': id_register,
            'kwargs': config_kwargs
        }, file=sys.stderr)
        print("Data: ", data, file=sys.stderr)

    c = EETConfig(
        dic, id_shop, id_register,
        **config_kwargs
    )
    request = EETRequest(c, **data)
    if args.verbose:
        print(request.serialize(), file=sys.stderr)

    response = request.send()
    if args.verbose:
        print(response.raw, file=sys.stderr)

    json.dump({
        'fik': response.fik,
        'bkp': response.bkp,
        'pkp': str(request.code.pkp),
        'error': response.error,
        'warnings': response.warnings
    }, args.output)


if __name__ == '__main__':
    eet_file()
