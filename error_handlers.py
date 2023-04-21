import flask
from flask import url_for, redirect

blueprint = flask.Blueprint('error_handlers', __name__)


@blueprint.app_errorhandler(404)
def handle404(e):
    return redirect(url_for('login'))
