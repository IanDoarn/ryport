try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='ryport',
    version='1.0.15',
    install_requires=['psycopg2', 'lxml', 'XlsxWriter', 'mysql-connector-python'],
    packages=['ryport', 'ryport.pgsql',
              'ryport.xml_builder', 'ryport.report',
              'ryport.mysql'],
    url='https://github.com/IanDoarn/ryport',
    license='MIT',
    author='Ian Doarn',
    author_email='ian.doarn@zimmerbiomet.com',
    description='Reporting tool for PostgreSQL and MySQL'
)
