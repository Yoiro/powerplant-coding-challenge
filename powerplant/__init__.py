from pathlib import Path

from flask import Flask


def load_blueprints(app):
    from powerplant.productionplan import bp_productionplan
    app.register_blueprint(bp_productionplan)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        Path(app.instance_path).mkdir()
    except OSError:
        pass

    load_blueprints(app)

    return app