# Python imports
import os
import sys
import traceback

# Third party imports
from chula import webservice

# Pubdiff imports
from model import review
from controller import base

class Home(base.Controller):
    def index(self):
        return self.render('/home.tmpl')

    def review(self):
        review_id = review.RE_REVIEW.match(self.env['PATH_INFO']).group(1)
        document = review.Review(review_id)

        if document['diffs']:
            self.model = document
            return self.render('/diff.tmpl')

        return self.render('/diff_not_found.tmpl')

    @webservice.expose()
    def upload(self):
        try:
            uploaded = review.UploadedReview(self.env.form_raw)
            url = '%s/r/%s' % (self.env['ajax_uri'], uploaded.review_id)

            return {'url':url}
        except Exception, ex:
            if os.environ.get('debug'):
                etype, value, tb = sys.exc_info()
                error_context = traceback.format_tb(tb)
                error_msg = traceback.format_exception_only(etype, value)
                for line in error_context:
                    print(line)
                print(error_msg)

            raise
