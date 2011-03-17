import os

from mako.template import Template
from mako.lookup import TemplateLookup

from chula.www import controller

class Controller(controller.Controller):
    def render(self, view):
        src = os.path.join(self.config.htdocs, '..', 'view')
        lookup = TemplateLookup(directories=[src])
        view = Template(filename=src + view,
                        lookup=lookup,
                        module_directory=None)

        return view.render_unicode(model=self.model).encode('utf-8', 'replace')
