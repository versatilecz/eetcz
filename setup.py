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
            'cryptography==1.5',
            'requests==2.11.1',
            'lxml==3.6.4',
            'pytz==2016.6.1',
            ],
      )
