from ocr.www.controllers import base
from ocr import diff

class Home(base.Controller):
    def index(self):
        return self.render('/home.tmpl')

    def review(self):
        diff1 = diff.Diff('/tmp/couch.py.old', '/tmp/couch.py')
        diff2 = diff.Diff('/tmp/env.py.old', '/tmp/env.py')

        self.model = {'diffs':[diff1, diff2]}
        return self.render('/diff.tmpl')
