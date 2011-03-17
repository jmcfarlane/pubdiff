# Python imports
import os

# Third party imports
from chula import config

# Pubdiff imports
from model import review

# App configuration
app = config.Config()
app.auto_reload = 'debug' in os.environ
app.classpath = 'controller'
app.construction_trigger = '/tmp/pubdiff/site.stop'
app.debug = 'debug' in os.environ
app.htdocs = os.path.join(os.path.dirname(__file__), '..', 'www')
app.session = False

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
