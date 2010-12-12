# Python imports
import os
import sys

# Third party imports
from setuptools import setup

# Project imports
from pubdiff import client

# Attributes
SRC = os.path.dirname(sys.argv[0])
AUTHOR = 'John McFarlane'
DESCRIPTION = open(os.path.join(SRC, 'README')).readlines()[0].strip()
EMAIL = 'john.mcfarlane@rockfloat.com'
NAME = 'Pubdiff'
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
    download_url = '%s/downloads/Pubdiff-%s.tar.gz' % (URL, client.VERSION),
    entry_points = """
        [console_scripts]
        pubdiff = pubdiff.client:main
    """,
    name = NAME,
    packages = ['pubdiff'],
    url = URL,
    version = client.VERSION,
    zip_safe = True,
)
