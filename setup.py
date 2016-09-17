from setuptools import setup

setup(
        name='eet-cz',
        version='0.1',
        description='Library to comunicate with czech tax office',
        url='https://git.profires.cz/webapp/authapp',
        author='Martin Miksanik',
        author_email='martin@miksanik.net',
        license='GNUGPL',
        packages=['eet'],
        zip_safe=False,
        install_requires=[
            'cryptography',
            'requests',
            'lxml',
            'pytz',
            'python-dateutil',
            ],
      )
