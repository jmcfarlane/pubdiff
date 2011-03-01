# Pubdiff imports
from controller import base

class About(base.Controller):
    def index(self):
        return self.render('/about.tmpl')

    def smarty_pants(self):
        return self.render('/smarty_pants.tmpl')
