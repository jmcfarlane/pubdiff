# Python imports
from distutils.core import setup
import os
import sys

# Project imports
from pubdiff import client

# Attributes
SRC = os.path.dirname(sys.argv[0])
AUTHOR = 'John McFarlane'
DESCRIPTION = 'Easy, anonymous, and public code diffs'
EMAIL = 'john.mcfarlane@rockfloat.com'
NAME = 'Pubdiff'
PYPI = 'http://pypi.python.org/packages/source/P/Pubdiff'
URL = 'http://www.pubdiff.com'
CLASSIFIERS = """
Development Status :: 2 - Pre-Alpha
Intended Audience :: Developers
License :: OSI Approved :: MIT License
Operating System :: OS Independent
Programming Language :: Python
Topic :: Internet :: WWW/HTTP
Topic :: Software Development :: Version Control
"""

setup(
    author = AUTHOR,
    author_email = EMAIL,
    classifiers = [c for c in CLASSIFIERS.split('\n') if c],
    description = DESCRIPTION,
    download_url = '%s/Pubdiff-%s.tar.gz' % (PYPI, client.VERSION),
    name = NAME,
    packages = ['pubdiff'],
    scripts = ['scripts/pubdiff'],
    url = URL,
    version = client.VERSION
)
