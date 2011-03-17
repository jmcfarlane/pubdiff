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

DATE_FORMAT = '%c'
RE_REVIEW = re.compile(r'^/r/([a-z0-9]+)$')
RE_BASENAME = re.compile(r':(before|after)')
LANGUAGE_MAP = {
                'bash':'sh',
                'c':'cpp',
                'c#':'csharp',
                'cpp':'cpp',
                'css':'css',
                'dash':'sh',
                'diff':'diff',
                'groovy':'groovy',
                'java':'java',
                'js':'javascript',
                'patch':'diff',
                'php':'php',
                'pl':'perl',
                'pm':'perl',
                'py':'python',
                'rb':'ruby',
                'sh':'sh',
                'sql':'sql',
                'vb':'vb',
                'xml':'xml',
                'zsh':'sh',
               }

class Comment(dict):
    def __init__(self):
        self['line_numbers'] = []
        self['msg'] = None
        self['timestamp'] = time.time()

class Diff(dict):
    def __init__(self):
        self['after'] = {'name':None}
        self['before'] = {'name':None}
        self['comments'] = []
        self['diff_stat_added'] = 0
        self['diff_stat_removed'] = 0
        self['diff_stat_total'] = 0
        self['lines'] = []

class Review(couch.Document):
    DB = 'pubdiff/reviews'

    def __init__(self, id=None, **kwargs):
        self['diffs'] = []

        if id is None:
            id = str(time.time())

        super(Review, self).__init__(id, **kwargs)

# todo: Move this class to chula:
class ReadonlyGenericDocument(dict):
    def __init__(self, id, document=None):
        if document is None:
            document = {}

        self.id = id
        self.update(document)

class Reviews(couch.Documents):
    DB = Review.DB

    def recent(self, **kwargs):
        view = 'reviews/recent'
        reviews = self.view(view, ReadonlyGenericDocument, **kwargs)
        reviews.sort(reverse=True)

        return reviews

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

    def language(self, path):
        actual_filename = os.path.basename(RE_BASENAME.sub('', path))
        extension = ''
        parts = actual_filename.rsplit('.', 1)

        if parts:
            extension = parts.pop()

        return LANGUAGE_MAP.get(extension.lower(), 'plain')

    def persist(self, review_id):
        # Instantiate and clean a review model object
        review = Review(review_id)
        review['diffs'] = []

        # Add this review's diffs
        for pair in self:
            parsed = diff.Diff(pair[0], pair[1])

            if os.environ.get('debug'):
                parsed.pretty_print()

            d = Diff()
            d['lines'] = parsed.lines
            d['after']['name'] = self.hash2path(parsed._after.name)
            d['before']['name'] = self.hash2path(parsed._before.name)

            # Calculate a (git) diff stat
            added = removed = total = 0
            for mark in [p[1].strip() for p in parsed.lines]:
                if mark in ('>', '|'):
                    added += 1
                    total += 1

                if mark in ('<', '|'):
                    removed += 1
                    total += 1

            d['diff_stat_added'] = added
            d['diff_stat_removed'] = removed
            d['diff_stat_total'] = total

            # Make any name based structure mutations
            for s in ['before', 'after']:
                d[s]['language'] = self.language(d[s]['name'])
                d[s]['label'] = d[s]['name'].replace(':%s' % s, ' (%s)' % s)

            review['diffs'].append(d)

        if review.persist():
            self.review_id = review_id
