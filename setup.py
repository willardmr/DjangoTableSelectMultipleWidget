# -*- encoding: utf-8 -*-
"""
Python setup file for the django-table-select-widget app.

In order to register your app at pypi.python.org, create an account at
pypi.python.org and login, then register your new app like so:

    python setup.py register

If your name is still free, you can now make your first release but first you
should check if you are uploading the correct files:

    python setup.py sdist

Inspect the output thoroughly. There shouldn't be any temp files and if your
app includes staticfiles or templates, make sure that they appear in the list.
If something is wrong, you need to edit MANIFEST.in and run the command again.

If all looks good, you can make your first release:

    python setup.py sdist upload

For new releases, you need to bump the version number in
webmap/__init__.py and re-run the above command.

For more information on creating source distributions, see
http://docs.python.org/2/distutils/sourcedist.html

"""
import os
import sys

from setuptools import find_packages, setup

# Make sure the django.mo file also exists:
try:
    os.chdir('table_select_widget')
    from django.core.management.commands.compilemessages import \
        compile_messages
    compile_messages(sys.stderr)
except ImportError:
    pass
finally:
    os.chdir('..')

dev_requires = []

dependency_links = []

install_requires = []


def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ''

setup(
    name="django-table-select-widget",
    version="1.1.0",
    description=read('DESCRIPTION'),
    long_description=read('README.rst'),
    platforms=['OS Independent'],
    keywords='django, table',
    author='insin, willardmr, Petr Dlouhý',
    author_email='petr.dlouhy@email.cz',
    url="https://github.com/PetrDlouhy/DjangoTableSelectMultipleWidget",
    packages=find_packages(),
    include_package_data=True,
    dependency_links=dependency_links,
    install_requires=install_requires,
    extras_require={
        'dev': dev_requires,
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.7',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
