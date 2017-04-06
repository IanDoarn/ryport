try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='ryport',
    version='1.0.6',
    install_requires=['psycopg2', 'lxml', 'XlsxWriter'],
    packages=['ryport', 'ryport.pgsql', 'ryport.xml_builder', 'ryport.xlsx_writer'],
    url='https://github.com/IanDoarn/ryport',
    license='MIT',
    author='Ian Doarn',
    author_email='ian.doarn@zimmerbiomet.com',
    description='Reporting tool for PostgreSQL'
)
