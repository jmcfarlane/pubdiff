import os

from chula import config

# Development configuration
app = config.Config()
app.classpath = 'ocr.www.controllers'
app.construction_controller = 'error'
app.construction_trigger = '/tmp/open_code_review.stop'
app.debug = True
app.error_controller = 'error'
app.session = False
app.local.root = os.getcwd()

app.mapper = (
    # Home controller
    (r'^$', 'home.index'),
    (r'^/r/[a-z0-9]+$', 'home.review'),

    # API controllers
    (r'^/api/upload/?$', 'home.upload'),
)
