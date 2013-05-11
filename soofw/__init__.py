import flask # dependencies
from werkzeug.contrib.fixers import ProxyFix

# set up the app and the proxy
app = flask.Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

import soofw.filters, soofw.views # local
