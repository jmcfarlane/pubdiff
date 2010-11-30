from setuptools import setup, find_packages

# Attributes
AUTHOR = 'John McFarlane'
EMAIL = 'john.mcfarlane@rockfloat.com'
NAME = 'Pubdiff'
URL = 'http://www.pubdiff.com'

setup(
    author = AUTHOR,
    author_email = EMAIL,
    entry_points = """
        [console_scripts]
        pubdiff = pubdiff.client:main
    """,
    name = NAME,
    packages = find_packages(),
    url = URL,
)
