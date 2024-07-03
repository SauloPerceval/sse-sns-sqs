from flask import Flask

from app.views.sse import bp_sse


def create_app() -> Flask:
    app = Flask(__name__)
    
    app.register_blueprint(bp_sse)

    return app


app = create_app()
