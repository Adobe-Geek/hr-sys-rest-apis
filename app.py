import os
from flask import Flask
from flask_smorest import Api
from db import db
from flask_migrate import Migrate
import models

from resources.department import blp as DepartmentBlueprint
from resources.employee import blp as EmployeeBlueprint
from resources.vacation import blp as VacationBlueprint
from resources.user import blp as UserBlueprint


def create_app(db_url=None):
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "HR System API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config["JWT_TOKEN_LOCATION"] = ["headers"]
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = (
        "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    )

    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv(
        "DATABASE_URL",  # "sqlite:///data.db"
    )
    app.config["SQLALCHEMY__TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    migrate = Migrate(app, db)

    api = Api(app)

    api.register_blueprint(DepartmentBlueprint)
    api.register_blueprint(EmployeeBlueprint)
    api.register_blueprint(VacationBlueprint)
    app.register_blueprint(UserBlueprint)

    return app
