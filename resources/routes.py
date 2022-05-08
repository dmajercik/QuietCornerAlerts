from .auth import auth
from cad.cad import cad
from website.web import web


def initialize_routes(app):
    app.register_blueprint(auth)
    app.register_blueprint(cad)
    app.register_blueprint(web)
