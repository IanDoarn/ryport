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
# update pip automatically
print("Updating pip")
subprocess.call(['python',
                 '-m',
                 'pip',
                 'install',
                 '--upgrade',
                 'pip'],
                shell=True)

# Descriptions
long_desc = """Softwrapper and reporting tool for Postgres
Ryport can run queries and write the data straight to readable formats
such as Excel and CSV. 
"""
short_desc = "Softwrapper and reporting tool for Postgres"


# Get required packages by checking if
# the user has them first, then adding them
# to the list of required if they don't.

install_requires = []
modules_to_update = []
# Pull required modules from requirements.txt
with open(os.path.join(file_path, 'requirements.txt'), 'r')as req_file:
    req_modules = req_file.readlines()
req_file.close()

# Attempt to import each module
for mod in req_modules:
    _mod = mod.replace('\n', '').split('>=')
    try:
        print('Attempting to import {}'.format(_mod[0]))
        # Try to import
        if _mod[0] == 'mysql-connector-python':
            module = importlib.import_module('mysql.connector')
        else:
            module = importlib.import_module(_mod[0])
        # Check version of module
        mod_dist = get_distribution(_mod[0])

        if len(set(list(mod_dist.version)).intersection(list(ascii_letters))) > 0:
            # module version has letters in it, attempt to upgrade it
            print('Could not verify version of {}'.format(_mod[0]))
            modules_to_update.append(_mod[0])
        else:
            mod_version = int(''.join(mod_dist.version.split('.')))
            req_mod_version = int(''.join(_mod[1].split('.')))
            if  mod_version < req_mod_version:
                print("{} is installed but is not the required version:"
                      "Installed [{}] Required [{}]".format(_mod[0],
                                                            str(mod_version),
                                                            str(req_mod_version)))
                modules_to_update.append(_mod[0])
            else:
                print("{} is installed and is the correct version [>={}]".format(_mod[0],
                                                                               _mod[1]))
        # delete from memory if successful
        del module
    except ModuleNotFoundError as error:
        # could not import so add to install requires
        print('Could not import {}'.format(_mod[0]))
        install_requires.append(mod.replace('\n', ''))


# Attempt to update modules
def update_modules():
    if len(modules_to_update) != 0:
        for mod in modules_to_update:
            try:
                subprocess.call(['pip',
                                 'install',
                                 mod,
                                 '--upgrade'], shell=True)
            except Exception as error:
                print('Unable to update {} to the required / latest version. '
                      'Please resolve this issue to ensure stability. '
                      'Error: [{}]'.format(mod, str(error)))


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
    # Required packages
    install_requires=install_requires,
    # Directories located in the module
    packages=create_package_list('ryport'),
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