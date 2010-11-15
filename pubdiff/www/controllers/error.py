import sys
import traceback
import re

from chula import collection
from chula.www import http

from pubdiff.www.controllers import base

RE_STATIC_FILE = re.compile(r'.*\.(css|gif|jpg|js|png|txt|xsl|ico|json)$')

class Error(base.Controller):
    def _crappy_static_server(self, path):
        """
        Fetch a static file from disk, changing headers and HTTP
        status as appropriate.
        """

        self.env.status = http.HTTP_OK
        if path.endswith('.css'):
            self.content_type = 'text/css'
        elif path.endswith('.js'):
            self.content_type = 'text/javascript'
        elif path.endswith('.gif'):
            self.content_type = 'image/gif'
        elif path.endswith('.jpg'):
            self.content_type = 'image/jpg'
        elif path.endswith('.xsl'):
            self.content_type = 'text/xsl'
        elif path.endswith('.json'):
            self.content_type = 'text/json'
            
        static = self.config.local.root + '/www' + path
        with open(static, 'r') as data:
            return data.read()

    def index(self):
        return self.render('/maintenance.tmpl')

    def e404(self):
        request_uri = self.env.REQUEST_URI

        # Support standalone mode and serve static content ourselves
        if not RE_STATIC_FILE.match(self.env.REQUEST_URI) is None:
            try:
                return self._crappy_static_server(self.env.REQUEST_URI)
            except IOError:
                raise

        # The url doesn't seem to be supported
        self.env.status = http.HTTP_NOT_FOUND

        return self.render('/error/e404.tmpl')

    def e500(self):
        exception = collection.Collection()
        try:
            context = self.model.exception
            exception.summary = context.exception
            exception.env = context.env
        except Exception, ex:
            print ex
            pass

        # Harvest additional context on the error
        try:
            etype, value, tb = sys.exc_info()
            error_context = traceback.format_tb(tb)
            error_msg = traceback.format_exception_only(etype, value)

            exception.traceback = error_context
            exception.message = error_msg
        except Exception, ex:
            print ex
            pass

        # Hack:
        try:
            if exception.message[0].startswith('None'):
                exception.message = str(exception.summary)
        except Exception, ex:
            print ex
            pass

        # Add the message to the view if debugging
        if self.config.debug:
            self.model.exception = exception
        else:
            self.model.exception = None

        return self.render('/error/e500.tmpl')
