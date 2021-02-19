from pathlib import Path
import os

from flask import Flask


def load_blueprints(app):
    from powerplant.productionplan import bp_productionplan
    app.register_blueprint(bp_productionplan)


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )
    
    if os.environ["FLASK_ENV"] == "dev":
        app.config.from_object('config.DevelopmentConfig')
    else:
        app.config.from_object('config.Config')

    # ensure the instance folder exists
    try:
        Path(app.instance_path).mkdir()
    except OSError:
        pass

    load_blueprints(app)

    return app
