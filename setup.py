import os
import re
import importlib
import subprocess
from pkg_resources import get_distribution
from string import ascii_letters
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup


file_path = os.path.abspath(os.path.dirname(__file__))

__project__ = 'ryport'

# Get version from __init__.py
def get_version(project=__project__):
    result = re.search(r'{}\s*=\s*[\'"]([^\'"]*)[\'"]'.format('__version__'), open(project + '/__init__.py').read())
    return result.group(1)

__author__ = 'Ian Doarn'
__version__ = get_version()
__url__ = 'https://github.com/IanDoarn/ryport'
__license__ = 'MIT'
__email__ = 'ian.doarn@zimmerbiomet.com'
__classifiers__ = [
    'Intended Audience :: Developers',
    'License :: {} License'.format(__license__),
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6'
]

# Descriptions
long_desc = """Softwrapper and reporting tool for Postgres
Ryport can run queries and write the data straight to readable formats
such as Excel and CSV. 
"""
short_desc = "Softwrapper and reporting tool for Postgres"


# Get required packages by checking if
# the user has them first, then adding them
# to the list of required if they don't.

install_requires = ['mysql-connector-python',
                    'psycopg2',
                    'lxml',
                    'XlsxWriter']

# Create package list of packages in ryport
excluded = ['.git', '.idea', '__pycache__']

def exclude_package(pkg):
    for exclude in excluded:
        if pkg.startswith(exclude):
            return True
    return False

# create package list for module
def create_package_list(base_package):
    return ([base_package] +
            [base_package + '.' + pkg
             for pkg
             in find_packages(base_package)
             if not exclude_package(pkg)])


# Actual setup process
setup_inf = dict(
    name=__project__,
    version=__version__,
    install_requires=install_requires,
    packages=create_package_list(__project__),
    url=__url__,
    license=__license__,
    author=__author__,
    author_email=__email__,
    long_description=long_desc,
    description=short_desc,
    classifiers=__classifiers__,
    zip_safe=True
)

setup(**setup_inf)