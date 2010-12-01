# Python imports
import hashlib
import json
import os
import re
import shutil
import sys
import time

# Third party imports
from chula.nosql import couch

sys.path.insert(0, os.getcwd())

# Pubdiff immports
from model import diff

RE_REVIEW = re.compile(r'^/r/([a-z0-9]+)$')

class Diff(dict):
    def __init__(self):
        self['lines'] = None
        self['before'] = {'name':None}
        self['after'] = {'name':None}

class Review(couch.Document):
    DB = 'pubdiff/reviews'

    def __init__(self, id=None, **kwargs):
        self['diffs'] = []

        if id is None:
            id = str(time.time())

        super(Review, self).__init__(id, **kwargs)

class UploadedReview(list):
    def __init__(self, json_string):
        self.review_id = None

        if json_string:
            self.fill(json_string)

    def path2hash(self, path):
        return path.replace(os.path.sep, '^')

    def hash2path(self, name):
        canonical = name.replace('^', os.path.sep)
        return canonical.split(self.temp_dir).pop()

    def fill(self, json_string):
        review_id = hashlib.sha1(json_string).hexdigest()
        self.temp_dir = os.path.join('/tmp/pubdiff_upload', review_id)

        try:
            diffs = json.loads(json_string)
            os.makedirs(self.temp_dir)
            for diff in diffs:
                # Reconstitute the source files on disk
                paths = []
                for state in ['before', 'after']:
                    source = diff[state]
                    name = self.path2hash(source['name']) + ':' + state
                    fq_path = os.path.join(self.temp_dir, name)

                    paths.append(fq_path)
                    with open(fq_path, 'w') as fh:
                        fh.write(source['contents'])

                # Append the (now on disk) paths to be uploaded
                self.append(paths)

            # Upload/persist to the db
            self.persist(review_id)

        except Exception, ex:
            raise
        finally:
            shutil.rmtree(self.temp_dir)

    def persist(self, review_id):
        # Instantiate and clean a review model object
        review = Review(review_id)
        review['diffs'] = []

        # Add this review's diffs
        for pair in self:
            parsed = diff.Diff(pair[0], pair[1])
            d = Diff()
            d['lines'] = parsed.lines
            d['before']['name'] = self.hash2path(parsed._before.name)
            d['after']['name'] = self.hash2path(parsed._after.name)

            review['diffs'].append(d)

        if review.persist():
            self.review_id = review_id
