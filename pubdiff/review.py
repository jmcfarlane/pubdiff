# Python imports
import os
import sys
import time

# Third party imports
from chula.nosql import couch

sys.path.insert(0, os.getcwd())

# OpenCodeReview immports
from ocr import diff

class Diff(dict):
    def __init__(self):
        self['lines'] = None
        self['before'] = {'name':None}
        self['after'] = {'name':None}

class Review(couch.Document):
    DB = 'ocr/reviews'

    def __init__(self, id=None, **kwargs):
        self['diffs'] = []

        if id is None:
            id = str(time.time())

        super(Review, self).__init__(id, **kwargs)

def upload(diffs):
    # Instantiate and clean a review model object
    review = Review('test')
    review['diffs'] = []

    # Add this review's diffs
    for pair in diffs:
        parsed = diff.Diff(pair[0], pair[1])
        d = Diff()
        d['lines'] = parsed.lines
        d['before']['name'] = parsed._before.name
        d['after']['name'] = parsed._after.name

        review['diffs'].append(d)

    review.persist()
    
def main():
    diffs = []
    diffs.append(('/tmp/couch.py.old', '/tmp/couch.py'))
    diffs.append(('/tmp/env.py.old', '/tmp/env.py'))
    
    upload(diffs)

if __name__ == '__main__':
    main()
