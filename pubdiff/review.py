# Python imports
import json
import os
import shutil
import sys
import time
import uuid

# Third party imports
from chula.nosql import couch

sys.path.insert(0, os.getcwd())

# OpenCodeReview immports
from pubdiff import diff

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

class EncodedReview(list):
    def __init__(self, json_string):
        if json_string:
            self.fill(json_string)

    def fill(self, json_string):
        was_uploaded = False
        TEMP_DIR = os.path.join('/tmp/pubdiff_upload', uuid.uuid4().hex)
        paths_to_upload = []
        try:
            diffs = json.loads(self.env.form_raw)
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
                paths_to_upload.append(paths)

            # Perform actual upload to the db of all diffs
            review.upload(paths_to_upload)
            was_uploaded = True
        except Exception, ex:
            return repr(ex)
        finally:
            shutil.rmtree(TEMP_DIR)    
            

    if was_uploaded:
        return 'Diff(s) uploaded successfully'
    else:
        return 'Nothing uploaded'

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
