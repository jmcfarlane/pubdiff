# Python imports
import os

# Third party imports
from chula import config

# Pubdiff imports
from pubdiff import review

# Development configuration
app = config.Config()
app.classpath = 'pubdiff.www.controllers'
app.construction_controller = 'error'
app.construction_trigger = '/tmp/open_code_review.stop'
app.debug = True
app.error_controller = 'error'
app.session = False
app.local.root = os.getcwd()

app.mapper = (
    # Home controller
    (r'^$', 'home.index'),
    (review.RE_REVIEW.pattern, 'home.review'),

    # API controllers
    (r'^/api/upload/?$', 'home.upload'),
)
