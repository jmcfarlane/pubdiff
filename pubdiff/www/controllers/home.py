# Third party imports
from chula import webservice

# Pubdiff imports
from pubdiff import review
from pubdiff.www.controllers import base

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
        uploaded = review.UploadedReview(self.env.form_raw)
        url = '%s/r/%s' % (self.env['ajax_uri'], uploaded.review_id)

        return {'url':url}
