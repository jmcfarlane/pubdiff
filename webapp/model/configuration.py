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
app.debug = 'debug' in os.environ
app.error_controller = 'error'
app.session = False
app.local.root = os.path.join(os.getcwd(), 'webapp')

# App url routes
app.mapper = (
    # Common
    (r'^$', 'home.index'),
    (review.RE_REVIEW.pattern, 'home.review'),
    (r'^/recent/?$', 'home.recent_reviews'),

    # API
    (r'^/api/upload/?$', 'home.upload'),
    (r'^/api/comment/persist/?$', 'home.comment'),

    # About
    (r'^/about/?$', 'about.index'),
    (r'^/r/your-unique-review/?$', 'about.smarty_pants'),
)
