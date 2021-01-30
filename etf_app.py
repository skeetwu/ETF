# -*- coding: utf-8 -*-

import os

from flask import Blueprint
from flask import Flask
from flask_restplus import Api

from eastmoney.crawler import index
from eastmoney.utils.flask_failsafe import failsafe

api = Api(version='1.0', title='ETF API', description='ETF restful API')

app = Flask(__name__)
app.secret_key = os.urandom(12)  # Generic key for dev purposes only
app.config['JSON_SORT_KEYS'] = False
app.config['SWAGGER_UI_DOC_EXPANSION'] = 'list'
app.config['RESTPLUS_VALIDATE'] = False
app.config['RESTPLUS_MASK_SWAGGER'] = False
app.config['ERROR_404_HELP'] = False


@failsafe
def create_app():
    # note that the import is *inside* this function so that we can catch
    # errors that happen at import time

    base_url = "/api/v1"
    blueprint = Blueprint('api', __name__, url_prefix=base_url)
    api.init_app(blueprint)

    # api.add_namespace(user_namespace)

    app.register_blueprint(blueprint)

    app.register_blueprint(index)
    return app

if __name__ == "__main__":
    create_app().run(debug=True, use_reloader=True, host="0.0.0.0")
