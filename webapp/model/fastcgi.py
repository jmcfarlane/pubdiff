"""
Pubdiff fastcgi server
"""

# Python imports
import os
import sys

# Third party imports
from chula.www.adapters.fcgi import adapter
try:
    from flup.server.fcgi_fork import WSGIServer
except ImportError:
    from chula.www.fcgi import WSGIServer
    print "Unable to import flup.server.fcgi import WSGIServer"
    print " >>> Falling back on old version available in Chula"

cwd = os.getcwd()
sys.path.insert(0, os.path.join(cwd, 'webapp'))

# Pubdiff imports
from model import configuration

@adapter.fcgi
def application():
    return configuration.app

class Server(WSGIServer, object):
    def error(self, req):
        if 'PUBDIFF_DEV' in os.environ:
            super(Server, self).error(req)
        else:
            return 'forcing "bad gateway" condition'

# Flup options
options = {'bindAddress':os.environ['PUBDIFF_FCGI_SOCKET'],
           'maxRequests':int(os.environ.get('PUBDIFF_FCGI_MAX', 25)),
           'maxSpare':int(os.environ.get('PUBDIFF_FCGI_SPARE', 1))}

# Start the server which will handle calls from the webserver
Server(application, **options).run()
