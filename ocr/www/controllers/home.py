from ocr import review
from ocr.www.controllers import base

class Home(base.Controller):
    def index(self):
        return self.render('/home.tmpl')

    def review(self):
        r = review.Review('test')

        self.model = r
        return self.render('/diff.tmpl')
