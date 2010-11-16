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
from pubdiff import diff

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

    def fill(self, json_string):
        review_id = hashlib.sha1(json_string).hexdigest()
        TEMP_DIR = os.path.join('/tmp/pubdiff_upload', review_id)

        try:
            diffs = json.loads(json_string)
            os.makedirs(TEMP_DIR)
            for diff in diffs:
                # Reconstitute the source files on disk
                paths = []
                for state in ['before', 'after']:
                    source = diff[state]
                    name = os.path.basename(source['name'])
                    fq_path = os.path.join(TEMP_DIR, name)
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
            shutil.rmtree(TEMP_DIR)    

    def persist(self, review_id):
        # Instantiate and clean a review model object
        review = Review(review_id)
        review['diffs'] = []

        # Add this review's diffs
        for pair in self:
            parsed = diff.Diff(pair[0], pair[1])
            d = Diff()
            d['lines'] = parsed.lines
            d['before']['name'] = parsed._before.name
            d['after']['name'] = parsed._after.name

            review['diffs'].append(d)

        if review.persist():
            self.review_id = review_id
