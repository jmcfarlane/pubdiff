# Python imports
import os

# Third party imports
from chula import config

# Pubdiff imports
from model import review

# App configuration
app = config.Config()
app.classpath = 'controller'
app.construction_controller = 'error'
app.construction_trigger = '/tmp/pubdiff/site.stop'
app.debug = False
app.error_controller = 'error'
app.session = False
app.local.root = os.path.join(os.getcwd(), 'webapp')

# App url routes
app.mapper = (
    # Home controller
    (r'^$', 'home.index'),
    (review.RE_REVIEW.pattern, 'home.review'),

    # API controllers
    (r'^/api/upload/?$', 'home.upload'),
)
